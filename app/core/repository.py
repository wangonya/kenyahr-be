import abc
from typing import Any, Dict, List, Optional

from app.core.db import db


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def filter(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, _id, data):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, _id):
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    def __init__(self, collection) -> None:
        self.collection: str = collection

    def add(self, data: Dict[str, Any]) -> Dict[str, Any]:
        created = db[self.collection].insert_one(data)
        return self.get(_id=created.inserted_id)

    def get(self, **kwargs) -> Optional[Dict[str, Any]]:
        return db[self.collection].find_one(kwargs)

    def filter(self, filter_parameters: dict) -> List[Optional[Dict[str, Any]]]:
        return db[self.collection].find(filter_parameters)

    def list(self) -> List[Optional[Dict[str, Any]]]:
        return db[self.collection].find()

    def update(self, _id, data: dict) -> Dict[str, Any]:
        db[self.collection].update_one({"_id": _id}, {"$set": data})
        return self.get(_id=_id)

    def delete(self, _id):
        db[self.collection].delete_one({"_id": _id})
