# processing/local_upload.py
# 책임: process_folder(database_dir: Path, repo: PropertyRepository, analytics: ScraperAnalytics)
# Notes: scan all JSON, process safely, archive on success

import logging
from pathlib import Path
from typing import List
import json
from config import DATABASE_DIR, MONGO_DATABASE, MONGO_COLLECTION
from db.client import get_mongo_client
from analytics.uploader import ScraperAnalytics, print_success_summary
from models.mapper import map_raw_imovel
from db.repository import PropertyRepository

logger = logging.getLogger(__name__)

def find_json_files(folder: Path) -> List[Path]:
    return list(folder.glob("*.json"))

def process_file(path: Path, repo: PropertyRepository, analytics: ScraperAnalytics):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        analytics.increment_identified(len(data))
        for raw in data:
            try:
                doc = map_raw_imovel(raw)
                result = repo.upsert(doc)
                if result.get("success"):
                    analytics.increment_success()
                else:
                    analytics.increment_failure()
                    analytics.add_error("upsert_failure", result.get("details", ""), doc.get("link_imovel"))
            except Exception as e:
                analytics.increment_failure()
                analytics.add_error("processing_error", str(e), raw.get("link_imovel"))
                logger.error(f"Error processing record: {e}")
        # archive or delete file to avoid re-processing
        archive_dir = path.parent / "processed"
        archive_dir.mkdir(exist_ok=True)
        path.replace(archive_dir / path.name)
    except Exception as e:
        logger.error(f"Failed to process file {path.name}: {e}")

def process_folder(
    database_dir: Path,
    repo: PropertyRepository,
    analytics: ScraperAnalytics
):
    files = find_json_files(database_dir)
    if not files:
        logger.info("No JSON to process.")
        return

    for f in files:
        logger.info(f"Processing file: {f.name}")
        process_file(f, repo, analytics)

if __name__ == "__main__":
    # example main usage
    from config import DATABASE_DIR
    from db.client import get_mongo_client

    logging.basicConfig(level=logging.INFO)
    client = get_mongo_client()
    repo = PropertyRepository(client[MONGO_DATABASE][MONGO_COLLECTION])
    with ScraperAnalytics("local_to_mongodb") as analytics:
        process_folder(DATABASE_DIR, repo, analytics)
        print_success_summary("local_to_mongodb", analytics.total_items_identified, {"json": None})
