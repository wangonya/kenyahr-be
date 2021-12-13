from typing import Any, Dict, List, Optional

import mongomock
import pytest

from app.core.repository import AbstractRepository


class MongoDBTestRepository(AbstractRepository):
    def __init__(self):
        self.collection = mongomock.MongoClient().db.collection

    def add(
        self,
        data: Dict[str, Any],
    ):
        created_id = self.collection.insert_one(data).inserted_id
        created_data = self.collection.find_one({"_id": created_id})
        return created_data

    def get(self, **kwargs) -> Optional[Dict[str, Any]]:
        reference = [*kwargs][0]
        return self.collection.find_one({reference: kwargs.get(reference)})

    def filter(self, filter_parameters: dict) -> List[Optional[Dict[str, Any]]]:
        return self.collection.find(filter_parameters)

    def list(self) -> List[Optional[Dict[str, Any]]]:
        return self.collection.find()

    def update(self, _id, data: dict) -> Dict[str, Any]:
        self.collection.update_one({"_id": _id}, {"$set": data})
        return self.get(_id=_id)

    def delete(self, _id):
        self.collection.delete_one({"_id": _id})


@pytest.fixture
def mongodb_test_repository():
    return MongoDBTestRepository()
