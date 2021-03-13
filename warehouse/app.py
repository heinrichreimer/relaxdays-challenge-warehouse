from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from typing import Dict
from warehouse.storage_place import StoragePlace
from warehouse.error import ApiError
from warehouse.api import (
    StoragePlaceApi,
    StoragePlacesApi,
    StoragePlacesForArticleApi
)
from warehouse.version import Version
from warehouse.specs import (
    create_storage_place_spec,
    read_storage_place_spec,
    update_storage_place_spec,
    delete_storage_place_spec,
    read_storage_places_spec,
    read_storage_places_for_article_spec
)

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

storage: Dict[str, StoragePlace] = {}


@app.errorhandler(ApiError)
def handle_api_error(error: ApiError):
    return error.to_response()


@api.resource('/storagePlace')
class StoragePlaceVO(Resource):
    api = StoragePlaceApi(storage, Version.V0)

    @swag_from(create_storage_place_spec(Version.V0), validation=True)
    def post(self):
        return self.api.post()

    @swag_from(read_storage_place_spec(Version.V0))
    def get(self):
        return self.api.get()

    @swag_from(update_storage_place_spec(Version.V0), validation=True)
    def put(self):
        return self.api.put()

    @swag_from(delete_storage_place_spec(Version.V0))
    def delete(self):
        return self.api.delete()


@api.resource('/storagePlaces')
class StoragePlacesVO(Resource):
    api = StoragePlacesApi(storage, Version.V0)

    @swag_from(read_storage_places_spec(Version.V0))
    def get(self):
        return self.api.get()


@api.resource('/v1/storagePlace')
class StoragePlaceV1(Resource):
    api = StoragePlaceApi(storage, Version.V1)

    @swag_from(create_storage_place_spec(Version.V1), validation=True)
    def post(self):
        return self.api.post()

    @swag_from(read_storage_place_spec(Version.V1))
    def get(self):
        return self.api.get()

    @swag_from(update_storage_place_spec(Version.V1), validation=True)
    def put(self):
        return self.api.put()

    @swag_from(delete_storage_place_spec(Version.V1))
    def delete(self):
        return self.api.delete()


@api.resource('/v1/storagePlaces')
class StoragePlacesV1(Resource):
    api = StoragePlacesApi(storage, Version.V1)

    @swag_from(read_storage_places_spec(Version.V1))
    def get(self):
        return self.api.get()


@api.resource('/v2/storagePlace')
class StoragePlaceV2(Resource):
    api = StoragePlaceApi(storage, Version.V2)

    @swag_from(create_storage_place_spec(Version.V2), validation=True)
    def post(self):
        return self.api.post()

    @swag_from(read_storage_place_spec(Version.V2))
    def get(self):
        return self.api.get()

    @swag_from(update_storage_place_spec(Version.V2), validation=True)
    def put(self):
        return self.api.put()

    @swag_from(delete_storage_place_spec(Version.V2))
    def delete(self):
        return self.api.delete()


@api.resource('/v2/storagePlaces')
class StoragePlacesV2(Resource):
    api = StoragePlacesApi(storage, Version.V2)

    @swag_from(read_storage_places_spec(Version.V2))
    def get(self):
        return self.api.get()


@api.resource('/v2/storagePlacesForArticleID')
class StoragePlacesForArticleV2(Resource):
    api = StoragePlacesForArticleApi(storage, Version.V2)

    @swag_from(read_storage_places_for_article_spec(Version.V2))
    def get(self):
        return self.api.get()
