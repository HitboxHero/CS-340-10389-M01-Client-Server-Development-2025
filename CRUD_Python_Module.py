# CRUD_Python_Module.py
# Simple reusable CRUD helper for the aac.animals collection.
# Comments are friendly so future me remembers why I did things.

from typing import Any, Dict, List, Optional
from pymongo import MongoClient, errors


class AnimalShelter:
    """CRUD operations for the AAC collection in MongoDB."""

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "127.0.0.1",
        port: int = 27017,
        db_name: str = "aac",
        col_name: str = "animals",
        auth_db: str = "admin",
    ) -> None:
        # Build a small connection string. Keep it boring and reliable.
        uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_db}"
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        try:
            # Quick handshake so bad creds fail fast.
            self.client.admin.command("ping")
        except errors.PyMongoError as exc:
            raise RuntimeError(f"Could not connect to MongoDB: {exc}") from exc

        self.db = self.client[db_name]
        self.col = self.db[col_name]

    # C = Create
    def create(self, data: Dict[str, Any]) -> bool:
        """Insert one document. True on success, False on any issue."""
        try:
            if not isinstance(data, dict) or not data:
                return False
            result = self.col.insert_one(data)
            return bool(getattr(result, "inserted_id", None))
        except errors.PyMongoError:
            return False

    # R = Read
    def read(
        self,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        limit: int = 0,
    ) -> List[Dict[str, Any]]:
        """Run a find and return a list of docs. Empty list on error."""
        try:
            q = query if isinstance(query, dict) else {}
            cur = self.col.find(q, projection)
            if isinstance(limit, int) and limit > 0:
                cur = cur.limit(limit)
            return list(cur)
        except errors.PyMongoError:
            return []
    # U = Update
    def update(self, query: Dict[str, Any], new_values: Dict[str, Any], many: bool = False) -> int:
        """
        Update document(s) that match query.
        - query: filter to select documents
        - new_values: fields to change. If you pass a plain dict, I wrap it in $set.
        - many: False -> update_one, True -> update_many
        Returns how many docs were modified.
        """
        try:
            if not isinstance(query, dict) or not query:
                return 0
            if not isinstance(new_values, dict) or not new_values:
                return 0

            # If caller did not include an operator, treat it like $set
            update_doc = new_values if any(k.startswith("$") for k in new_values) else {"$set": new_values}

            result = self.col.update_many(query, update_doc) if many else self.col.update_one(query, update_doc)
            return int(getattr(result, "modified_count", 0))
        except Exception:
            return 0

    # D = Delete
    def delete(self, query: Dict[str, Any], many: bool = False) -> int:
        """
        Delete document(s) that match query.
        - query: filter to select documents
        - many: False -> delete_one, True -> delete_many
        Returns how many docs were deleted.
        """
        try:
            if not isinstance(query, dict) or not query:
                return 0
            result = self.col.delete_many(query) if many else self.col.delete_one(query)
            return int(getattr(result, "deleted_count", 0))
        except Exception:
            return 0