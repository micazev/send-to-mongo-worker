# analytics/uploader.py
#책임: wrap ScraperAnalytics lifecycle

# analytics/uploader.py

import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

# psutil is optional for memory metrics
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil not available. Memory (메모리) metrics will be disabled.")

class ScraperAnalytics:
    """
    Questo modulo misura e salva metriche di scraping:
    - start_scraping(): Iniziare (to start) la raccolta metriche
    - end_scraping(): Terminare (to end) e salvare i risultati
    """
    def __init__(self, scraper_name: str):
        self.scraper_name = scraper_name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.total_items_identified: int = 0
        self.successfully_extracted: int = 0
        self.failed_extractions: int = 0
        self.errors: List[Dict] = []
        self.requests_count: int = 0
        self.initial_memory: Optional[float] = None
        self.analytics_dir = "analytics"
        
        # assicurarsi che la cartella analytics esista
        os.makedirs(self.analytics_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Context manager protocol
    # ------------------------------------------------------------------
    def __enter__(self) -> "ScraperAnalytics":
        """Start tracking metrics when entering the context."""
        self.start_scraping()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Finish tracking and persist analytics on exit."""
        self.end_scraping()
        # Propagate any exception to the caller
        return False


    def start_scraping(self) -> None:
        """Begin (iniziare) tracking of time and 메모리 (memory)"""
        self.start_time = time.time()
        if PSUTIL_AVAILABLE:
            proc = psutil.Process()
            self.initial_memory = proc.memory_info().rss / 1024 / 1024  # MB

    def end_scraping(self) -> None:
        """Stop (terminare) tracking and save metrics to file"""
        self.end_time = time.time()
        self._save_analytics()

    def increment_identified(self, count: int = 1) -> None:
        """Increment count of identified items (데이터)"""
        self.total_items_identified += count

    def increment_success(self, count: int = 1) -> None:
        """Increment count of successful extractions (성공)"""
        self.successfully_extracted += count

    def increment_failure(self, count: int = 1) -> None:
        """Increment count of failed extractions (실패)"""
        self.failed_extractions += count

    def increment_requests(self, count: int = 1) -> None:
        """Increment count of external requests made"""
        self.requests_count += count

    def add_error(self, error_type: str, error_message: str, item_id: Optional[str] = None) -> None:
        """Record an error with timestamp"""
        self.errors.append({
            "type": error_type,
            "message": error_message,
            "item_id": item_id,
            "timestamp": datetime.now().isoformat()
        })

    def _calculate_metrics(self) -> Dict:
        """Compute final metrics including duration and 성능 (performance)"""
        duration = (self.end_time - self.start_time) if (self.start_time and self.end_time) else 0
        
        metrics = {
            "scraper_name": self.scraper_name,
            "timestamp": {
                "start": datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
                "end": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
                "duration_seconds": round(duration, 2)
            },
            "data_metrics": {
                "total_items_identified": self.total_items_identified,
                "successfully_extracted": self.successfully_extracted,
                "failed_extractions": self.failed_extractions,
                "success_rate": round((self.successfully_extracted / self.total_items_identified * 100), 2)
                                if self.total_items_identified > 0 else 0
            },
            "performance_metrics": {
                "average_time_per_item": round(duration / self.successfully_extracted, 2)
                                        if self.successfully_extracted > 0 else 0,
                "requests_count": self.requests_count
            },
            "errors": self.errors
        }

        # add memory usage if available
        if PSUTIL_AVAILABLE and self.initial_memory is not None:
            proc = psutil.Process()
            final_memory = proc.memory_info().rss / 1024 / 1024
            memory_used = final_memory - self.initial_memory
            metrics["performance_metrics"]["memory_used_mb"] = round(memory_used, 2)

        return metrics

    def _save_analytics(self) -> None:
        """Salvare (to save) metrics JSON to disk"""
        metrics = self._calculate_metrics()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.analytics_dir, f"{self.scraper_name}_{timestamp}.json")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
            logging.info(f"Analytics saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save analytics: {e}")

    def get_current_metrics(self) -> Dict:
        """Retrieve current metrics without ending the session"""
        return self._calculate_metrics()


def print_success_summary(scraper_name: str, item_count: int, storage_paths: Dict[str, str]) -> None:
    """
    Print a concise success summary.
    """
    print(f"\n✅ [{scraper_name}] scraping completed successfully!")
    print(f"📊 Total items collected: {item_count}")
    print("📁 Files saved to:")
    json_path = storage_paths.get("json")
    csv_path = storage_paths.get("csv")
    if json_path:
        print(f"   - JSON: {os.path.basename(json_path)}")
    if csv_path:
        print(f"   - CSV: {os.path.basename(csv_path)}")
