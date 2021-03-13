from typing import Dict
from warehouse.storage_place import StoragePlace
from warehouse.version import Version
from re import fullmatch


def parse_storage_place(
    storage_place: Dict,
    version: Version,
    default: StoragePlace = None
) -> StoragePlace:
    article_id = (
        storage_place["articleID"]
        if "articleID" in storage_place
        else default.article_id
    )
    stock = (
        storage_place["bestand"]
        if "bestand" in storage_place
        else default.stock
    )
    if version >= Version.V2:
        capacity = (
            storage_place["kapazitaet"]
            if "kapazitaet" in storage_place
            else default.capacity
        )
    else:
        capacity = stock
    return StoragePlace(
        parse_storage_place_name(storage_place, version),
        article_id,
        stock,
        capacity
    )


def parse_storage_place_name(
    storage_place: Dict,
    version: Version,
) -> str:
    if version >= Version.V1:
        location = storage_place["standort"]
        section = storage_place["lagerabschnitt"]
        row = storage_place["reihe"]
        place = storage_place["platz"]
        height = storage_place["hoehe"]
        return "{location}-{section};{row};{place};{height}".format(
            location=location,
            section=section,
            row=row,
            place=place,
            height=height,
        )
    else:
        return storage_place["name"]


def format_storage_place(
    storage_place: StoragePlace,
    version: Version
) -> Dict:
    name = format_storage_place_name(storage_place, version)
    result = {
        "articleID": storage_place.article_id,
        "bestand": storage_place.stock,
    }
    result.update(name)

    if (version >= Version.V2):
        result["kapazitaet"] = storage_place.capacity

    return result


def format_storage_place_name(
    storage_place: StoragePlace,
    version: Version
) -> Dict:
    if version >= Version.V1:
        match = fullmatch(r"(\w+)-(\d+);(\d+);(\d+);(\d+)", storage_place.name)
        return {
            "standort": match.group(1),
            "lagerabschnitt": match.group(2),
            "reihe": match.group(3),
            "platz": match.group(4),
            "hoehe": match.group(5),
        }
    else:
        return {
            "name": storage_place.name,
        }
