from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from typing import Dict
from warehouse.storage_place import StoragePlace
from warehouse.error import ApiError
from warehouse.resources import StoragePlaceResource, StoragePlacesResource
from warehouse.version import Version

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

storage: Dict[str, StoragePlace] = {}


@app.errorhandler(ApiError)
def handle_api_error(error: ApiError):
    return error.to_response()


@api.resource('/storagePlace')
class StoragePlaceVO(StoragePlaceResource):
    def __init__(self):
        super().__init__(storage, Version.V0)


@api.resource('/storagePlaces')
class StoragePlacesVO(StoragePlacesResource):
    def __init__(self):
        super().__init__(storage, Version.V0)


@api.resource('/v1/storagePlace')
class StoragePlaceV1(StoragePlaceResource):
    def __init__(self):
        super().__init__(storage, Version.V1)


@api.resource('/v1/storagePlaces')
class StoragePlacesV1(StoragePlacesResource):
    def __init__(self):
        super().__init__(storage, Version.V1)
