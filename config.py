# config.py
# 책임 (Responsibility): centralize paths & env vars
# Contents:
# MONGO_URI = os.getenv("MONGO_URI")
# DATABASE_DIR = Path(os.getenv("DATABASE_DIR", "database"))
# ANALYTICS_DIR = Path(os.getenv("ANALYTICS_DIR", "analytics"))
# (Optional) logging level/format

import os
import logging
from pathlib import Path

# Environment variables and default directories
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_DIR = Path(os.getenv("DATABASE_DIR", "database"))
ANALYTICS_DIR = Path(os.getenv("ANALYTICS_DIR", "analytics"))

# Ensure directories exist
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

# Optional logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "%(asctime)s - %(levelname)s - %(message)s"
)
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
