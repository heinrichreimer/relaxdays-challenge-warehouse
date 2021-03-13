from pathlib import Path
from warehouse.version import Version


def _base(version: Version = Version.V0):
    base = Path(__file__).parent
    if version == Version.V1:
        base = base / "v1"
    return base


def create_storage_place_spec(version: Version = Version.V0):
    return _base(version) / "create_storage_place.yml"


def read_storage_place_spec(version: Version = Version.V0):
    return _base(version) / "read_storage_place.yml"


def update_storage_place_spec(version: Version = Version.V0):
    return _base(version) / "update_storage_place.yml"


def delete_storage_place_spec(version: Version = Version.V0):
    return _base(version) / "delete_storage_place.yml"


def read_storage_places_spec(version: Version = Version.V0):
    return _base(version) / "read_storage_places.yml"
