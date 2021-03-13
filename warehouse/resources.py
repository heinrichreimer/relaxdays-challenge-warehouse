from flask import jsonify, request
from typing import Dict, List
from warehouse.storage_place import StoragePlace
from warehouse.parsers import (
    parse_storage_place,
    parse_storage_place_name,
    format_storage_place,
)
from warehouse.error import ApiError
from warehouse.version import Version


def _success():
    return jsonify({"message": "Success."})


class StoragePlaceApi:
    storage: Dict[str, StoragePlace]
    version: Version

    def __init__(
        self,
        storage: Dict[str, StoragePlace],
        version: Version
    ):
        self.storage = storage
        self.version = version

    def post(self):
        name = parse_storage_place_name(request.json, self.version)
        if name in self.storage:
            raise ApiError("Storage place already exists.")
        storage_place = parse_storage_place(request.json, self.version)
        self.storage[storage_place.name] = storage_place
        return _success()

    def get(self):
        if "x" not in request.args:
            raise ApiError("Must specify name.")
        name = request.args["x"]
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        storage_place = self.storage[name]
        return jsonify(format_storage_place(storage_place, self.version))

    def put(self):
        name = parse_storage_place_name(request.json, self.version)
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        old_storage_place = self.storage[name]
        storage_place = parse_storage_place(
            request.json,
            self.version,
            old_storage_place
        )
        self.storage[storage_place.name] = storage_place
        return _success()

    def delete(self):
        if "x" not in request.args:
            raise ApiError("Must specify name.")
        name = request.args["x"]
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        del self.storage[name]
        return _success()


class StoragePlacesApi:
    storage: Dict[str, StoragePlace]
    version: Version

    def __init__(
        self,
        storage: Dict[str, StoragePlace],
        version: Version
    ):
        self.storage = storage
        self.version = version

    def get(self):
        count = int(request.args["n"])
        name = request.args["x"] if "x" in request.args else None

        result: List[StoragePlace] = list(self.storage.values())

        # Filter names that come lexicographically
        # after the given name.
        if name:
            result = list(filter(
                lambda storage_place: storage_place.name > name,
                result
            ))

        result.sort(
            key=lambda storage_place: storage_place.name
        )
        result = result[0:count]
        result = list(map(
            lambda storage_place: format_storage_place(
                storage_place,
                self.version
            ),
            result
        ))
        return jsonify(result)
