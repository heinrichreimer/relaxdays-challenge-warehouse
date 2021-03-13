from typing import Dict
from warehouse.storage_place import StoragePlace


def parse_storage_place(
    storage_place: Dict,
    default: StoragePlace = None
) -> StoragePlace:
    return StoragePlace(
        storage_place["name"]
        if "name" in storage_place
        else default.name,
        storage_place["articleID"]
        if "articleID" in storage_place
        else default.article_id,
        storage_place["bestand"]
        if "bestand" in storage_place
        else default.stock,
    )


def parse_storage_place_name(
    storage_place: Dict,
) -> str:
    return storage_place["name"]


def format_storage_place(storage_place: StoragePlace) -> Dict:
    return {
        "name": storage_place.name,
        "articleID": storage_place.article_id,
        "bestand": storage_place.stock,
    }
