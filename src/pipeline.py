import os
import argparse
import glob
import json
import logging
import re
from pathlib import Path

from src.extractor.pdf_extractor import process_single_pdf_to_context
from src.extractor.prompt_builder import build_prompt
from src.extractor.llm_client import run_llm_call
from src.evaluation.deterministic_evaluator import DeterministicEvaluator
from src.db.database_handler import (
    write_trl_evaluation,
    write_trl_specific_data,
    write_paper_metadata,
    get_unprocessed_paper_ids,
    get_paper_id_by_title,
    create_new_paper_record,
    get_paper_metadata
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SafeLoggingFilter(logging.Filter):
    def filter(self, record):
        if record.pathname and 'pix2tex' in record.pathname:
            if record.args:
                record.msg = f"{record.msg} {record.args}"
                record.args = ()
        return True

logging.getLogger().addFilter(SafeLoggingFilter())

def clean_json_response(response_text: str) -> dict:
    """Cleans potential markdown wrapping from LLM JSON response and parses it."""
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def process_paper(paper_id=None, pdf_path=None, force=False):
    """
    Runs the pipeline for a single paper.
    Either paper_id or pdf_path must be provided.
    """
    if not paper_id and not pdf_path:
        logging.error("Must provide either paper_id or pdf_path.")
        return

    title = None
    if paper_id and not pdf_path:
        # Fetch title to locate PDF
        metadata = get_paper_metadata(paper_id)
        title = metadata.get("title")
        if not title:
            logging.error(f"Paper {paper_id} has no title in DB.")
            return
        
        # Look for PDF in papers/ directory
        papers_dir = os.path.join("d:/projects/trl-project", "papers")
        potential_pdf_path = os.path.join(papers_dir, f"{title}.pdf")
        if os.path.exists(potential_pdf_path):
            pdf_path = potential_pdf_path
        else:
            # Fallback to see if any PDF matches title loosely
            all_pdfs = glob.glob(os.path.join(papers_dir, "*.pdf"))
            for p in all_pdfs:
                if title.lower() in os.path.basename(p).lower():
                    pdf_path = p
                    break
            if not pdf_path:
                logging.error(f"Could not find PDF for paper '{title}' in {papers_dir}")
                return

    if pdf_path and not paper_id:
        # We have a PDF, check if it exists in DB by title
        file_name = os.path.basename(pdf_path)
        base_name = os.path.splitext(file_name)[0]
        title = base_name
        
        found_id = get_paper_id_by_title(title)
        if found_id:
            paper_id = found_id
            logging.info(f"Matched PDF '{title}' to existing DB paper_id: {paper_id}")
        else:
            logging.info(f"PDF '{title}' not found in DB. Creating new record.")
            paper_id = create_new_paper_record(title)

    # At this point we have both paper_id and pdf_path
    file_name = os.path.basename(pdf_path)
    base_name = os.path.splitext(file_name)[0]

    text_base_dir = "d:/projects/trl-project/text_extracted"
    images_base_dir = "d:/projects/trl-project/images"
    metadata_dir = "d:/projects/trl-project/metadata"
    os.makedirs(metadata_dir, exist_ok=True)

    text_file_path = os.path.join(text_base_dir, f"{base_name}.md")
    metadata_file_path = os.path.join(metadata_dir, f"{base_name}_metadata.json")

    # Step 1: Extraction
    if force or not os.path.exists(text_file_path):
        logging.info(f"Extracting text from {pdf_path}...")
        extracted_path = process_single_pdf_to_context(pdf_path, images_base_dir, text_base_dir)
        if not extracted_path:
            logging.error("Text extraction failed. Aborting pipeline for this paper.")
            return
        text_file_path = extracted_path
    else:
        logging.info(f"Using cached text extraction: {text_file_path}")

    # Get page count from PDF
    page_count = 0
    if pdf_path and os.path.exists(pdf_path):
        try:
            import fitz
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()
        except Exception as e:
            logging.error(f"Failed to read page count from PDF: {e}")

    # Step 2: LLM Inference
    trl_specific_data = None
    if force or not os.path.exists(metadata_file_path):
        logging.info("Running LLM inference...")
        with open(text_file_path, "r", encoding="utf-8") as f:
            paper_text = f.read()

        prompt = build_prompt(paper_text=paper_text)
        try:
            llm_response = run_llm_call(prompt)
            parsed_json = clean_json_response(llm_response)
            
            metadata = parsed_json.get("metadata", {})
            trl_specific_data = parsed_json.get("trl_specific", {})

            # Fallback if the response didn't nested structured properly
            if not metadata and not trl_specific_data:
                if "trl_specific" in parsed_json:
                    trl_specific_data = parsed_json["trl_specific"]
                else:
                    trl_specific_data = parsed_json

            # Ensure page count is set
            metadata["page_count"] = page_count

            # Save to metadata folder
            with open(metadata_file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "metadata": metadata,
                    "trl_specific": trl_specific_data
                }, f, indent=2)
            
            # Write to DB
            if paper_id:
                write_paper_metadata(paper_id, metadata)
                write_trl_specific_data(paper_id, trl_specific_data)
                logging.info(f"Saved general metadata and trl_specific data to DB for paper {paper_id}")
                
        except Exception as e:
            logging.error(f"LLM call or JSON parsing failed: {e}")
            return
    else:
        logging.info(f"Using cached metadata: {metadata_file_path}")
        with open(metadata_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            trl_specific_data = data.get("trl_specific", data)

    # Step 3: Evaluation
    if trl_specific_data:
        logging.info("Running deterministic evaluator...")
        evaluator = DeterministicEvaluator(confidence_threshold=0.7)
        final_trl = evaluator.evaluate_paper(paper_id, trl_specific_data)
        
        if final_trl > 0:
            logging.info(f"Final TRL for {base_name}: {final_trl}")
            if paper_id:
                write_trl_evaluation(paper_id, final_trl)
                logging.info(f"Wrote TRL {final_trl} to DB for paper {paper_id}")
        else:
            logging.info(f"Paper {base_name} did not qualify for any TRL level (TRL 0).")
            write_trl_evaluation(paper_id, 0)
    else:
        logging.error("No trl_specific_data available for evaluation.")

def main():
    parser = argparse.ArgumentParser(description="End-to-end TRL extraction and evaluation pipeline.")
    parser.add_argument("--paper-id", type=str, help="Run pipeline for a specific paper UUID in DB.")
    parser.add_argument("--pdf-path", type=str, help="Run pipeline for a specific PDF file.")
    parser.add_argument("--all-db", action="store_true", help="Run pipeline for all unprocessed papers in DB.")
    parser.add_argument("--all-pdfs", action="store_true", help="Run pipeline for all PDFs in papers/ directory.")
    parser.add_argument("--force", action="store_true", help="Force re-run extraction and LLM inference.")

    args = parser.parse_args()

    if args.paper_id:
        process_paper(paper_id=args.paper_id, force=args.force)
    elif args.pdf_path:
        process_paper(pdf_path=args.pdf_path, force=args.force)
    elif args.all_db:
        paper_ids = get_unprocessed_paper_ids(force=args.force)
        logging.info(f"Found {len(paper_ids)} papers to process from DB.")
        for pid in paper_ids:
            process_paper(paper_id=pid, force=args.force)
    elif args.all_pdfs:
        papers_dir = "d:/projects/trl-project/papers"
        pdf_files = glob.glob(os.path.join(papers_dir, "*.pdf"))
        logging.info(f"Found {len(pdf_files)} PDFs to process.")
        for p in pdf_files:
            process_paper(pdf_path=p, force=args.force)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
