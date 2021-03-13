from pathlib import Path
from warehouse.version import Version


def _base(version: Version):
    base = Path(__file__).parent
    if version == Version.V0:
        pass
    elif version == Version.V1:
        base = base / "v1"
    elif version == Version.V2:
        base = base / "v2"
    elif version == Version.V3:
        base = base / "v3"
    else:
        raise "Can't find API spec."
    return base


def create_storage_place_spec(version: Version):
    return _base(version) / "create_storage_place.yml"


def read_storage_place_spec(version: Version):
    return _base(version) / "read_storage_place.yml"


def update_storage_place_spec(version: Version):
    return _base(version) / "update_storage_place.yml"


def delete_storage_place_spec(version: Version):
    return _base(version) / "delete_storage_place.yml"


def read_storage_places_spec(version: Version):
    return _base(version) / "read_storage_places.yml"


def read_storage_places_for_article_spec(version: Version):
    if version < Version.V2:
        raise "Endpoint not available"
    return _base(version) / "read_storage_places_for_article.yml"
