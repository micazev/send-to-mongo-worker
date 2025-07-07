# main.py
# 책임: orchestrate the scraper
# Notes: use config, client, repo, analytics, processing

import logging
from config import DATABASE_DIR, MONGO_DATABASE, MONGO_COLLECTION
from db.client import get_mongo_client
from db.repository import PropertyRepository
from analytics.uploader import ScraperAnalytics
from processing.local_upload import process_folder

if __name__ == "__main__":
    # logging already configured in config.py
    client = get_mongo_client()
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]
    db = client["busca_leiloes"]
    collection = db["tabelaDeImoveis"]
    repo = PropertyRepository(collection)

    # usa AnalyticsUploader per misurare (to measure) e salvare metriche
    with ScraperAnalytics("local_to_mongodb") as analytics:
        process_folder(DATABASE_DIR, repo, analytics)
