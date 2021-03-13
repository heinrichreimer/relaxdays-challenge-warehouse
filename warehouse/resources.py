from flask import jsonify, request
from flask_restful import Resource
from flasgger import swag_from
from typing import Dict
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
)


def _success():
    return jsonify({"message": "Success."})


class StoragePlaceResource(Resource):
    storage: Dict[str, StoragePlace]

    def __init__(
        self,
        storage: Dict[str, StoragePlace],
    ):
        self.storage = storage

    @swag_from(create_storage_place_spec(), validation=True)
    def post(self):
        name = parse_storage_place_name(request.json)
        if name in self.storage:
            raise ApiError("Storage place already exists.")
        storage_place = parse_storage_place(request.json)
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
        return jsonify(format_storage_place(storage_place))

    @swag_from(update_storage_place_spec(), validation=True)
    def put(self: str):
        name = parse_storage_place_name(request.json)
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        old_storage_place = self.storage[name]
        storage_place = parse_storage_place(request.json, old_storage_place)
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
