from dataclasses import dataclass


@dataclass
class StoragePlace:
    name: str
    article_id: int
    stock: int
