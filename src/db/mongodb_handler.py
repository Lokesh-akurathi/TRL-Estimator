"""
Handles MongoDB database interactions:
- Retrieving metadata for a paper.
- Writing TRL evaluation results to the papers collection.
"""
import os
import uuid
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file at the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=DOTENV_PATH)

def get_db_connection():
    """
    Establishes a connection to the MongoDB database.
    Returns a tuple of (client, db_instance).
    """
    mongo_uri = os.getenv("MONGO_URI") or "mongodb://localhost:27017/"
    db_name = os.getenv("MONGO_DB")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    return client, db

def get_paper_metadata(paper_id: str) -> dict:
    """
    Retrieves metadata for a given paper_id from the 'papers' collection.
    """
    client, db = get_db_connection()
    try:
        paper = db.papers.find_one({"paper_id": paper_id})
        if not paper:
            raise ValueError(f"Paper with ID '{paper_id}' not found.")
        # Convert MongoDB ObjectId to string to keep serialization-friendly
        if "_id" in paper:
            paper["_id"] = str(paper["_id"])
        return paper
    finally:
        client.close()

def write_trl_evaluation(paper_id: str, trl: int):
    """
    Writes the determined TRL level to the 'trl_level' field of the 'papers' collection.
    """
    client, db = get_db_connection()
    try:
        db.papers.update_one(
            {"paper_id": paper_id},
            {
                "$set": {
                    "trl_level": trl,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    finally:
        client.close()

def write_trl_specific_data(paper_id: str, trl_specific_data: dict):
    """
    Writes the detailed TRL specific LLM output to the 'trl_specific' field.
    """
    client, db = get_db_connection()
    try:
        db.papers.update_one(
            {"paper_id": paper_id},
            {
                "$set": {
                    "trl_specific": trl_specific_data,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    finally:
        client.close()

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

    client, db = get_db_connection()
    try:
        db.papers.update_one(
            {"paper_id": paper_id},
            {
                "$set": {
                    "research_title": metadata.get("research_title"),
                    "authors": metadata.get("authors"),
                    "abstract": metadata.get("abstract"),
                    "published_year": published_year,
                    "venue": metadata.get("venue"),
                    "doi": metadata.get("doi"),
                    "language": metadata.get("language"),
                    "country_of_origin": metadata.get("country_of_origin"),
                    "paper_type": metadata.get("paper_type"),
                    "page_count": page_count,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    finally:
        client.close()

def get_unprocessed_paper_ids(force: bool = False) -> list:
    """
    Returns a list of paper_ids that need processing.
    If force is False, only returns papers where trl_specific IS NULL OR trl_level IS NULL.
    If force is True, returns all paper_ids.
    """
    client, db = get_db_connection()
    try:
        if force:
            cursor = db.papers.find({}, {"paper_id": 1, "_id": 0})
        else:
            cursor = db.papers.find(
                {
                    "$or": [
                        {"trl_specific": {"$exists": False}},
                        {"trl_specific": None},
                        {"trl_level": {"$exists": False}},
                        {"trl_level": None}
                    ]
                },
                {"paper_id": 1, "_id": 0}
            )
        return [doc["paper_id"] for doc in cursor if "paper_id" in doc]
    finally:
        client.close()

def get_paper_id_by_title(title: str):
    """
    Attempts to find a paper_id by matching the title.
    """
    client, db = get_db_connection()
    try:
        paper = db.papers.find_one({"title": title}, {"paper_id": 1, "_id": 0})
        return paper["paper_id"] if paper else None
    finally:
        client.close()

def create_new_paper_record(title: str) -> str:
    """
    Creates a new record in the papers collection for a newly discovered PDF and returns the new paper_id.
    """
    new_id = str(uuid.uuid4())
    client, db = get_db_connection()
    try:
        db.papers.insert_one({
            "paper_id": new_id,
            "title": title,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
    finally:
        client.close()
    return new_id
