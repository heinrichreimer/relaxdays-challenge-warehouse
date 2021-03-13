from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from typing import Dict, List
from warehouse.storage_place import StoragePlace

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

storage: Dict[str, StoragePlace] = {}


def parse_storage_place(
    storage_place: Dict,
    default: StoragePlace = None
) -> StoragePlace:
    return StoragePlace(
        storage_place["name"] or default.name,
        storage_place["articleID"] or default.article_id,
        storage_place["bestand"] or default.stock,
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


class ApiError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        result = dict()
        result['message'] = self.message
        return result


@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


class StoragePlaceResource(Resource):
    @swag_from("specs/create_storage_place.yml", validation=True)
    def post(self):
        name = parse_storage_place_name(request.json)
        if name in storage:
            raise ApiError("Storage place already exists.")
        storage_place = parse_storage_place(request.json)
        storage[storage_place.name] = storage_place
        return ""

    @swag_from("specs/read_storage_place.yml", validation=True)
    def get(self, name: str):
        if name not in storage:
            raise ApiError("Storage place does not exist.")
        storage_place = storage[name]
        return jsonify(format_storage_place(storage_place))

    @swag_from("specs/update_storage_place.yml", validation=True)
    def put(self: str):
        name = parse_storage_place_name(request.json)
        if name not in storage:
            raise ApiError("Storage place does not exist.")
        old_storage_place = storage[name]
        storage_place = parse_storage_place(request.json, old_storage_place)
        storage[storage_place.name] = storage_place
        return ""

    @swag_from("specs/delete_storage_place.yml", validation=True)
    def delete(self, name):
        if name not in storage:
            raise ApiError("Storage place does not exist.")
        del storage[name]
        return ""


api.add_resource(StoragePlaceResource, "/storagePlace")


@app.route("/storagePlaces", methods=["GET"])
@swag_from("read_storage_places.yml")
def read_storage_places():
    count = int(request.args["n"])
    name = request.args["x"] if "x" in request.args else None

    result: List[StoragePlace] = list(storage.values())

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
    return jsonify(result)
