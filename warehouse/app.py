from flask import Flask, jsonify, request
from flask_restful import Api
from flasgger import Swagger, swag_from
from typing import Dict, List
from warehouse.storage_place import StoragePlace
from warehouse.error import ApiError
from warehouse.specs import (
    read_storage_places_spec,
)
from warehouse.resources import StoragePlaceResource

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

storage: Dict[str, StoragePlace] = {}


@app.errorhandler(ApiError)
def handle_api_error(error: ApiError):
    return error.to_response()


api.add_resource(
    StoragePlaceResource,
    "/storagePlace",
    resource_class_args=tuple([storage])
)


@app.route("/storagePlaces", methods=["GET"])
@swag_from(read_storage_places_spec())
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
