# Technology Readiness Level (TRL) Agent

## Overview
The TRL Agent is designed to automatically evaluate and assign a Technology Readiness Level (TRL) from 1 to 9 to academic research papers. It achieves this by analyzing the extracted metadata of a paper using a combination of Large Language Model (LLM) based questioning and a deterministic constraint-checking engine.

## Architecture

The system is modular and consists of the following core components:

1.  
**Database Handler (`src/db/database_handler.py`)**:
    *   Connects to a PostgreSQL database and run migrations for schema.
**Database Handler (`src/db/mongodb_handler.py`)**:
    *   Alternately Connects to a mongo database which more is suitable to store json fields of paper.
    *   **Retrieval**: Fetches paper metadata via `get_paper_metadata`.
    *   **Storage**: Updates fields within the `papers` table with the computed `trl_level` via `write_trl_evaluation`.

    can switch between postgres or mongodb by adjusting db handler import in **src/evaluation/deterministic_evaluator.py** and **src/pipeline.py**
    From:
    from src.db.database_handler import ...
    To:
    from src.db.mongodb_handler import ...


2.  **Deterministic Evaluator (`src/evaluation/deterministic_evaluator.py`)**:
    *   Applies a strict rules-based engine over the pre-evaluated metadata fields.
    *   **Top-Down Evaluation**: Iterates from TRL 9 down to 1. It finds the highest level where all "Hard" constraints are explicitly met with a confidence score equal to or above the threshold (default $\ge$ 0.7).
    *   **Bottom-Up Verification**: Iterates from TRL 1 up to 9 to verify consistency. If there's a mismatch between top-down and bottom-up approaches, the evaluator conservatively defaults to the lower TRL score.

3.  **Configuration (`config/`)**:
    *   `exhaustive_constraints.py`: Defines the specific "Hard" and "Soft" constraint questions mapped to each TRL level (1 through 9).
    *   `high_level_questions.json`: Contains summary baseline questions for each level.


## Setup Instructions

### Prerequisites
*   Python 3.10+
*   PostgreSQL database

### Installation
1. Ensure you are in the project root directory.
2. Install the necessary Python dependencies from requirments.txt

### Environment Variables
The application requires environment variables to connect to the LLM and the Database. Create a `.env` file in the project root directory from .env.example


# PostgreSQL Database Configuration
DB_HOST="localhost"
DB_NAME="trl"
DB_USER="postgres"
DB_PASSWORD="your_password"
```

## Running the Agent

The agent can be run in two ways: using the **deterministic evaluation script** ([run_evaluator.py]) for papers with existing metadata in the database, or using the **end-to-end extraction and evaluation pipeline** ([src/pipeline.py]) to process PDF files and run LLM inference.

### 1. Deterministic Evaluator Script ([run_evaluator.py])

If a paper's LLM metadata (`trl_specific` JSONB field) is already stored in the database, you can run the evaluation logic directly.

```bash
python run_evaluator.py <paper_id>
```

*   **Example:**
    ```bash
    python run_evaluator.py 88c0392a-b528-482c-bc7c-168cd41967c8
    ```

### 2. End-to-End Extraction & Evaluation Pipeline ([src/pipeline.py])

To parse PDF files, run LLM metadata extraction, save cached outputs (text/images/metadata), and run the deterministic evaluator, use the pipeline module:

*   **Process all PDFs in the `papers/` directory:**
    ```bash
    python -m src.pipeline --all-pdfs
    ```

*   **Process a single local PDF file:**
    ```bash
    python -m src.pipeline --pdf-path "papers/Your_Paper.pdf"
    ```

*   **Process a specific paper UUID in the database:**
    ```bash
    python -m src.pipeline --paper-id <paper_id>
    ```

*   **Process all unprocessed papers currently in the database:**
    ```bash
    python -m src.pipeline --all-db
    ```

*   **Force re-run (ignore cached text extraction and LLM inference):**
    Append the `--force` flag:
    ```bash
    python -m src.pipeline --all-pdfs --force
    ```

### Execution Flow
1. **Extraction (Pipeline only):** If text extraction is not cached, the pipeline parses the PDF text/images and stores them under `text_extracted/` and `images/`.
2. **LLM Inference (Pipeline only):** If the LLM metadata JSON file is not cached under `metadata/`, it builds a prompt, calls the Gemini model, parses the response, and writes the structured metadata to the database.
3. **Database Retrieval:** The evaluator fetches the paper's metadata and the `trl_specific` field.
4. **Deterministic Evaluation:** The [DeterministicEvaluator] checks the TRL specific field decisions.
5. **Consistency Checks:** It performs top-down and bottom-up consistency checks based on the `exhaustive_constraints`.
6. **Persistence:** The final determined TRL is printed to the console and updated in the `trl_level` column of the `papers` table in PostgreSQL.