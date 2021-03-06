import mongomock
import pytest

from app.core.repository import AbstractRepository


class MongoDBTestRepository(AbstractRepository):
    def __init__(self):
        self.collection = mongomock.MongoClient().db.collection

    def add(self, data):
        created_id = self.collection.insert_one(data).inserted_id
        created_data = self.collection.find_one({"_id": created_id})
        return created_data

    def get(self, **kwargs):
        reference = [*kwargs][0]
        return self.collection.find_one({reference: kwargs.get(reference)})

    def filter(self, filter_parameters):
        return self.collection.find(filter_parameters)

    def list(self):
        return self.collection.find()

    def update(self, _id, data):
        self.collection.update_one({"_id": _id}, {"$set": data})
        return self.get(_id=_id)

    def delete(self, _id):
        self.collection.delete_one({"_id": _id})


@pytest.fixture
def mongodb_test_repository():
    return MongoDBTestRepository()
