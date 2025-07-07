# db/client.py
# 책임: get_mongo_client(uri: Optional[str]=None) -> MongoClient
# Notes: reads MONGO_URI, pings, raises on error

import os
import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    """
    Creates and returns a MongoDB client using the given URI or the
    MONGO_URI environment variable. Pings the server to verify connection.
    Raises RuntimeError if the URI is missing or connection fails.
    """
    mongo_uri = uri or os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI environment variable is not set")
    try:
        client = MongoClient(mongo_uri)
        # Verify the connection
        client.admin.command("ping")
        logger.info("Successfully connected to MongoDB")
        return client
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise RuntimeError(f"Failed to connect to MongoDB: {e}")
