from flask import jsonify, request
from flask_restful import Resource
from flasgger import swag_from
from typing import Dict, List
from warehouse.storage_place import StoragePlace
from warehouse.parsers import (
    parse_storage_place,
    parse_storage_place_name,
    format_storage_place,
)
from warehouse.error import ApiError
from warehouse.specs import (
    create_storage_place_spec,
    read_storage_place_spec,
    update_storage_place_spec,
    delete_storage_place_spec,
    read_storage_places_spec,
)
from warehouse.version import Version


def _success():
    return jsonify({"message": "Success."})


class StoragePlaceResource(Resource):
    storage: Dict[str, StoragePlace]
    version: Version

    def __init__(
        self,
        storage: Dict[str, StoragePlace],
        version: Version
    ):
        self.storage = storage
        self.version = version

    @swag_from(create_storage_place_spec(), validation=True)
    def post(self):
        name = parse_storage_place_name(request.json, self.version)
        if name in self.storage:
            raise ApiError("Storage place already exists.")
        storage_place = parse_storage_place(request.json, self.version)
        self.storage[storage_place.name] = storage_place
        return _success()

    @swag_from(read_storage_place_spec())
    def get(self):
        if "x" not in request.args:
            raise ApiError("Must specify name.")
        name = request.args["x"]
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        storage_place = self.storage[name]
        return jsonify(format_storage_place(storage_place, self.version))

    @swag_from(update_storage_place_spec(), validation=True)
    def put(self: str):
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

    @swag_from(delete_storage_place_spec())
    def delete(self):
        if "x" not in request.args:
            raise ApiError("Must specify name.")
        name = request.args["x"]
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        del self.storage[name]
        return _success()


class StoragePlacesResource(Resource):
    storage: Dict[str, StoragePlace]
    version: Version

    def __init__(
        self,
        storage: Dict[str, StoragePlace],
        version: Version
    ):
        self.storage = storage
        self.version = version

    @swag_from(read_storage_places_spec())
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
