"""
Handles database interactions:
- Retrieving metadata for a paper.
- Writing TRL evaluation results to the paper_derived table.
"""
import os
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file at the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=DOTENV_PATH)

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST") or "localhost",
        database=os.getenv("DB_NAME") or "r2c",
        user=os.getenv("DB_USER") or "postgres",
        password=os.getenv("DB_PASSWORD") or "postgres"
    )
    return conn

def get_paper_metadata(paper_id: str) -> dict:
    """
    Retrieves metadata for a given paper_id from the 'papers' table.
    """
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM papers WHERE paper_id = %s;", (paper_id,))
        print(f"fetching paper {paper_id}")
        paper = cur.fetchone()
    conn.close()
    if not paper:
        raise ValueError(f"Paper with ID '{paper_id}' not found.")
    return dict(paper)

def write_trl_evaluation(paper_id: str, trl: int):
    """
    Writes the determined TRL level to the 'trl_level' column of the 'papers' table.
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE papers
            SET trl_level = %s
            WHERE paper_id = %s;
            """,
            (trl, paper_id)
        )
    conn.commit()
    conn.close()

import json

def write_trl_specific_data(paper_id: str, trl_specific_data: dict):
    """
    Writes the detailed TRL specific LLM output to the 'trl_specific' JSONB column.
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE papers
            SET trl_specific = %s::jsonb
            WHERE paper_id = %s;
            """,
            (json.dumps(trl_specific_data), paper_id)
        )
    conn.commit()
    conn.close()

def write_paper_metadata(paper_id: str, metadata: dict):
    """
    Writes general paper metadata (research_title, authors, abstract, published_year, venue, doi, language, country_of_origin, paper_type, page_count) to the database.
    """
    published_year = metadata.get("published_year")
    if published_year is not None:
        try:
            published_year = int(published_year)
        except (ValueError, TypeError):
            published_year = None

    page_count = metadata.get("page_count")
    if page_count is not None:
        try:
            page_count = int(page_count)
        except (ValueError, TypeError):
            page_count = None

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE papers
            SET research_title = %s,
                authors = %s,
                abstract = %s,
                published_year = %s,
                venue = %s,
                doi = %s,
                language = %s,
                country_of_origin = %s,
                paper_type = %s,
                page_count = %s
            WHERE paper_id = %s;
            """,
            (
                metadata.get("research_title"),
                metadata.get("authors"),
                metadata.get("abstract"),
                published_year,
                metadata.get("venue"),
                metadata.get("doi"),
                metadata.get("language"),
                metadata.get("country_of_origin"),
                metadata.get("paper_type"),
                page_count,
                paper_id
            )
        )
    conn.commit()
    conn.close()

def get_unprocessed_paper_ids(force: bool = False) -> list:
    """
    Returns a list of paper_ids that need processing.
    If force is False, only returns papers where trl_specific IS NULL OR trl_level IS NULL.
    If force is True, returns all paper_ids.
    """
    conn = get_db_connection()
    paper_ids = []
    with conn.cursor() as cur:
        if force:
            cur.execute("SELECT paper_id FROM papers;")
        else:
            cur.execute("SELECT paper_id FROM papers WHERE trl_specific IS NULL OR trl_level IS NULL;")
        rows = cur.fetchall()
        paper_ids = [row[0] for row in rows]
    conn.close()
    return paper_ids

def get_paper_id_by_title(title: str):
    """
    Attempts to find a paper_id by matching the title.
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT paper_id FROM papers WHERE title = %s LIMIT 1;", (title,))
        row = cur.fetchone()
    conn.close()
    return row[0] if row else None

import uuid

def create_new_paper_record(title: str) -> str:
    """
    Creates a new record in the papers table for a newly discovered PDF and returns the new paper_id.
    """
    new_id = str(uuid.uuid4())
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO papers (paper_id, title)
            VALUES (%s, %s);
            """,
            (new_id, title)
        )
    conn.commit()
    conn.close()
    return new_id
