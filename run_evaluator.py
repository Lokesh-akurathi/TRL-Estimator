import sys
from src.evaluation.deterministic_evaluator import DeterministicEvaluator, logger
from src.db.database_handler import write_trl_evaluation

def main():
    """Main function to run the deterministic TRL evaluation for a specific paper."""
    if len(sys.argv) > 1:
        paper_id_to_evaluate = sys.argv[1]
    else:
        logger.error("No paper ID provided. Please run the script with a paper ID, e.g., 'python main.py <paper_id>'")

    evaluator = DeterministicEvaluator(confidence_threshold=0.7) # Expects a float between 0.0 and 1.0

    try:
        final_trl = evaluator.evaluate_paper(paper_id_to_evaluate)

        if final_trl > 0:
            print(f"\nFinal Determined TRL for paper {paper_id_to_evaluate}: {final_trl}")

            logger.info(f"Writing result to database: TRL level {final_trl}")
            write_trl_evaluation(paper_id_to_evaluate, final_trl)
        else:
            print(f"\nPaper {paper_id_to_evaluate} did not qualify for any TRL level (TRL 0).")

    except Exception as e:
        logger.critical(f"An unexpected error occurred during the evaluation process: {e}", exc_info=True)


if __name__ == "__main__":
    main()
