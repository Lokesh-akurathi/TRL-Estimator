import os
import glob
import fitz  # PyMuPDF
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

# Attempt to load pix2tex (LaTeX OCR) for robust formula extraction
try:
    # pyrefly: ignore [missing-import]
    from pix2tex.cli import LatexOCR
    latex_ocr_model = LatexOCR()
    # LatexOCR internally overrides the root logging level to CRITICAL (50).
    # Reset it back to INFO to ensure project logs are visible.
    logging.getLogger().setLevel(logging.INFO)
    logger.info("Successfully loaded pix2tex (LatexOCR) for formula extraction.")
except ImportError:
    latex_ocr_model = None
    logger.warning("pix2tex is not installed. Formula extraction to LaTeX will be disabled. Install with: pip install pix2tex")

def get_column_sorted_blocks(page):
    """
    Extract text blocks and sort them logically to handle multi-column layouts.
    Filters out repeating headers and footers based on page margins.
    """
    blocks = page.get_text("blocks")
    page_height = page.rect.height
    
    valid_blocks = []
    for b in blocks:
        y0, y1 = b[1], b[3]
        
        # Heuristic: Remove headers (top 50px) and footers (bottom 50px)
        if y0 < 50 or y1 > page_height - 50:
            continue
            
        valid_blocks.append(b)
        
    # Group x0 into ~100 pixel columns to prevent mixing left and right columns
    # Then sort vertically (y0) within the column
    valid_blocks.sort(key=lambda b: (round(b[0] / 100), b[1]))
    return valid_blocks

def process_single_pdf_to_context(pdf_path: str, images_base_dir: str = "d:/projects/trl-project/images", text_base_dir: str = "d:/projects/trl-project/text_extracted") -> str:
    """
    Reads a single PDF file, extracts structured text and embedded images.
    Returns the path to the extracted markdown file.
    """
    file_name = os.path.basename(pdf_path)
    base_name = os.path.splitext(file_name)[0]
    logger.info(f"Parsing: {file_name}...")
    
    pdf_images_dir = os.path.join(images_base_dir, base_name)
    os.makedirs(pdf_images_dir, exist_ok=True)
    os.makedirs(text_base_dir, exist_ok=True)
    
    try:
        doc = fitz.open(pdf_path)
        markdown_lines = []
        
        for page_num, page in enumerate(doc):
            # 1. Page separator
            markdown_lines.append(f"\n====page_{page_num+1}========\n")
            
            # 2. Extract text blocks in robust reading order (ignoring header/footers)
            blocks = get_column_sorted_blocks(page)
            
            for b in blocks:
                block_text = b[4].strip()
                if block_text:
                    markdown_lines.append(block_text + "\n")
            
            # 3. Extract embedded images (and attempt formula extraction)
            image_list = page.get_images(full=True)
            for img_idx, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Save image
                    img_filename = f"page_{page_num+1}_fig_{img_idx+1}.{image_ext}"
                    img_path = os.path.join(pdf_images_dir, img_filename)
                    
                    with open(img_path, "wb") as f:
                        f.write(image_bytes)
            
                        
                    # 4. Robust Formula Extraction via pix2tex
                    if latex_ocr_model is not None:
                        try:
                            pil_img = Image.open(io.BytesIO(image_bytes))
                            if pil_img.width < 1500 and pil_img.height < 600:
                                latex_text = latex_ocr_model(pil_img)
                                if latex_text and len(latex_text.strip()) > 2:
                                    markdown_lines.append(f"\n**Extracted Formula:**\n$$\n{latex_text}\n$$\n")
                        except Exception as ocr_err:
                            logger.debug(f"LaTeX OCR skipped or failed for {img_filename}: {ocr_err}")

                except Exception as img_err:
                    logger.warning(f"Failed to save image {img_idx+1} on page {page_num+1}: {img_err}")
        
        # Save the final text output
        output_text_file = os.path.join(text_base_dir, f"{base_name}.md")
        markdown_text = "\n".join(markdown_lines)
        with open(output_text_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)
            
        logger.info(f"Finished parsing {file_name}. Text saved to '{output_text_file}'. Images saved to '{pdf_images_dir}'.")
        return output_text_file
        
    except Exception as e:
        logger.error(f"Failed to parse {file_name}. Error: {e}")
        return ""

def process_pdfs_to_context(papers_dir="d:/projects/trl-project/papers", images_base_dir="d:/projects/trl-project/images", text_base_dir="d:/projects/trl-project/text_extracted"):
    """
    Reads all PDFs in a folder, extracts structured text and embedded images.
    Organizes outputs and supports robust formula extraction.
    """
    logger.info(f"Scanning for PDFs in '{papers_dir}'...")
    pdf_files = glob.glob(os.path.join(papers_dir, "*.pdf"))
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{papers_dir}'. Please add some files.")
    
    for pdf_path in pdf_files:
        process_single_pdf_to_context(pdf_path, images_base_dir, text_base_dir)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    class SafeLoggingFilter(logging.Filter):
        def filter(self, record):
            if record.pathname and 'pix2tex' in record.pathname:
                if record.args:
                    record.msg = f"{record.msg} {record.args}"
                    record.args = ()
            return True

    logging.getLogger().addFilter(SafeLoggingFilter())
    process_pdfs_to_context()
