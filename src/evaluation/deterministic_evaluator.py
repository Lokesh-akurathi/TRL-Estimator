import sys
from pathlib import Path
import logging
from typing import Dict, Any

# Dynamically determine the project root
current_file_path = Path(__file__).resolve()
project_root = None

# Search upwards for a directory containing both 'src' and 'config'
for parent in current_file_path.parents:
    if (parent / "src").is_dir() and (parent / "config").is_dir():
        project_root = parent
        break

if project_root is None:
    # Fallback to the original assumption if markers are not found, but log a warning.
    project_root = current_file_path.parents[2]
    logging.warning(f"Could not find project root using 'src' and 'config' markers. Falling back to parents[2]: {project_root}")
sys.path.insert(0, str(project_root))


from src.db.database_handler import get_paper_metadata, write_trl_evaluation
from config.exhaustive_constraints import trl_fields

# --- Logger Setup ---
# In a production environment, this configuration might be centralized.
logger = logging.getLogger(__name__)


class DeterministicEvaluator:
    """
    Evaluates the TRL of a paper based on pre-determined, deterministic checks
    against 'Hard' constraints for each TRL level.
    """

    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initializes the evaluator.

        Args:
            confidence_threshold (float): The minimum confidence required for a 'YES'
                                          answer to be considered valid.
        """
        self.trl_constraints = trl_fields
        self.confidence_threshold = confidence_threshold
        logger.info(f"DeterministicEvaluator initialized with confidence threshold: {self.confidence_threshold}")

    def _verify_trl_level(self, trl_level: int, evaluated_fields: Dict[str, Any]) -> bool:
        """
        Verifies if a paper meets all 'Hard' constraints for a given TRL level.

        Args:
            trl_level (int): The TRL level to verify (1-9).
            evaluated_fields (Dict[str, Any]): The pre-evaluated fields for the paper.

        Returns:
            bool: True if all hard constraints are met, False otherwise.
        """
        level_key = f"TRL_{trl_level}"
        hard_questions = self.trl_constraints.get(level_key, {}).get("Hard", {}).get("questions", {})

        if not hard_questions:
            logger.warning(f"No hard constraints defined for {level_key}. Assuming it passes.")
            return True

        for field_key, question_text in hard_questions.items():
            logger.debug(f"Checking {level_key} constraint: '{field_key}'")

            if field_key not in evaluated_fields:
                logger.warning(f"[{level_key} FAILED] Missing field in paper data: '{field_key}'. Question: '{question_text}'")
                return False

            evaluation_result = evaluated_fields[field_key]

            if not isinstance(evaluation_result, dict) or "decision" not in evaluation_result or "confidence" not in evaluation_result:
                logger.error(f"[{level_key} FAILED] Malformed evaluation data for field '{field_key}': {evaluation_result}")
                return False
            
            answer = evaluation_result.get("decision", "").upper()
            
            # Robustly parse confidence, handling floats, ints, and percentage strings
            confidence_raw = evaluation_result.get("confidence", 0.0)
            confidence = 0.0
            if isinstance(confidence_raw, (int, float)):
                confidence = float(confidence_raw)
            elif isinstance(confidence_raw, str):
                try:
                    cleaned_confidence_str = confidence_raw.replace('%', '').strip()
                    parsed_confidence = float(cleaned_confidence_str)
                    # If the parsed value is > 1.0, assume it's a percentage (e.g., "70" instead of "0.7")
                    confidence = parsed_confidence / 100.0 if parsed_confidence > 1.0 else parsed_confidence
                except ValueError:
                    logger.warning(f"Could not parse confidence string '{confidence_raw}' for field '{field_key}'. Defaulting to 0.0.")
            else:
                logger.warning(f"Unexpected type for confidence: {type(confidence_raw)} for field '{field_key}'. Defaulting to 0.0.")
            confidence = max(0.0, min(1.0, confidence)) # Ensure confidence is clamped between 0.0 and 1.0

            if answer != "YES":
                logger.info(f"[{level_key} FAILED] Constraint '{field_key}' not met. Expected 'YES', got '{answer}'.")
                return False

            if confidence < self.confidence_threshold:
                logger.info(f"[{level_key} FAILED] Constraint '{field_key}' has insufficient confidence. Expected >= {self.confidence_threshold}, got {confidence}.")
                return False

            logger.debug(f"[{level_key} PASSED] Constraint '{field_key}' met with confidence {confidence}.")

        logger.info(f"All hard constraints for {level_key} PASSED.")
        return True

    def _evaluate_paper_bottom_up(self, paper_id: str, trl_specific_fields: Dict[str, Any]) -> int:
        """
        Determines the TRL for a given paper by iterating from TRL 1 up to 9.
        This is primarily for verification purposes against the top-down approach.

        Args:
            paper_id (str): The UUID of the paper being evaluated.
            trl_specific_fields (Dict[str, Any]): The pre-evaluated fields for the paper.

        Returns:
            int: The highest TRL level (1-9) for which all hard constraints are met, or 0 if none.
        """
        logger.info(f"Starting bottom-up TRL evaluation for paper_id: {paper_id}")
        highest_trl_met = 0
        for i in range(1, 10):  # From TRL 1 to TRL 9
            logger.debug(f"--- Bottom-up: Checking TRL {i} ---")
            if self._verify_trl_level(i, trl_specific_fields):
                highest_trl_met = i
            else:
                logger.debug(f"Bottom-up: Paper {paper_id} failed TRL {i}. Stopping further checks as TRLs are cumulative.")
                break
        return highest_trl_met
    def evaluate_paper(self, paper_id: str, trl_specific_data: dict = None) -> int:
        """
        Determines the TRL for a given paper by iterating from TRL 9 down to 1.

        Args:
            paper_id (str): The UUID of the paper to evaluate.
            trl_specific_data (dict, optional): Provide this to avoid DB lookup.

        Returns:
            int: The determined TRL level (1-9), or 0 if no level is met.
        """
        logger.info(f"Starting deterministic TRL evaluation for paper_id: {paper_id}")
        
        if trl_specific_data is not None:
            trl_specific_fields = trl_specific_data
        else:
            try:
                paper_metadata = get_paper_metadata(paper_id)
                trl_specific_fields = paper_metadata.get("trl_specific")
            except ValueError as e:
                logger.error(f"Failed to retrieve metadata for paper_id {paper_id}: {e}")
                return 0

        if not trl_specific_fields or not isinstance(trl_specific_fields, dict):
            logger.error(f"Paper {paper_id} has no 'trl_specific' fields or it is malformed. Cannot perform evaluation.")
            return 0

        trl_top_down = 0
        logger.info("--- Performing Top-Down TRL Evaluation (9 to 1) ---")
        for i in range(9, 0, -1):
            logger.info(f"Top-Down: Checking TRL {i}")
            if self._verify_trl_level(i, trl_specific_fields):
                trl_top_down = i
                logger.info(f"Top-Down: Paper {paper_id} has achieved TRL {i}.")
                break
        if trl_top_down == 0:
            logger.warning(f"Top-Down: Paper {paper_id} did not meet the hard constraints for any TRL level (1-9).")

        # --- Bottom-up evaluation (1 to 9) for verification ---
        trl_bottom_up = self._evaluate_paper_bottom_up(paper_id, trl_specific_fields)

        # --- Compare results ---
        if trl_top_down == trl_bottom_up:
            logger.info(f"TRL evaluation consistency check PASSED. Both top-down ({trl_top_down}) and bottom-up ({trl_bottom_up}) evaluations match.")
            final_trl = trl_top_down
        else:
            logger.warning(f"TRL evaluation consistency check FAILED for paper {paper_id}. Top-down: {trl_top_down}, Bottom-up: {trl_bottom_up}.")
            final_trl = min(trl_top_down, trl_bottom_up)
            logger.warning(f"Defaulting to the lower TRL: {final_trl} for paper {paper_id}.")
        
        return final_trl
