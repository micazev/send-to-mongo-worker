# db/repository.py
# 책임: all CRUD for "imóvel"
# Notes: encapsulates MongoDB operations for property documents

import logging
from typing import Dict, Optional
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, PyMongoError

logger = logging.getLogger(__name__)

class PropertyRepository:
    """
    Repository handling CRUD operations for 'imóvel' documents.
    """
    def __init__(self, collection: Collection):
        self.collection = collection

    def upsert(self, document: Dict) -> Dict:
        """
        Upserts a property document based on 'link_imovel' as unique identifier.
        Returns a summary dict with success flag and counts.
        """
        filter_criteria = {'link_imovel': document.get('link_imovel')}
        try:
            result = self.collection.replace_one(
                filter_criteria,
                document,
                upsert=True
            )
            if result.upserted_id:
                logger.info(f"Inserted new imóvel with ID: {result.upserted_id}")
            else:
                logger.info(f"Updated imóvel; modified_count={result.modified_count}")
            return {
                'success': True,
                'upserted_id': str(result.upserted_id) if result.upserted_id else None,
                'matched_count': result.matched_count,
                'modified_count': result.modified_count
            }
        except DuplicateKeyError as e:
            logger.error(f"DuplicateKeyError during upsert: {e}")
            return {'success': False, 'error': 'duplicate_key', 'details': str(e)}
        except PyMongoError as e:
            logger.error(f"PyMongoError during upsert: {e}")
            return {'success': False, 'error': 'db_error', 'details': str(e)}

    def find_by_link(self, link_imovel: str) -> Optional[Dict]:
        """
        Retrieves a single property document by its link_imovel.
        """
        try:
            return self.collection.find_one({'link_imovel': link_imovel})
        except PyMongoError as e:
            logger.error(f"Error finding imóvel by link: {e}")
            return None

    def delete_by_link(self, link_imovel: str) -> bool:
        """
        Deletes a property document by its link_imovel. Returns True if deleted.
        """
        try:
            result = self.collection.delete_one({'link_imovel': link_imovel})
            return result.deleted_count > 0
        except PyMongoError as e:
            logger.error(f"Error deleting imóvel: {e}")
            return False