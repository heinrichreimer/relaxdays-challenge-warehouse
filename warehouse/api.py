from flask import jsonify, request
from typing import Dict, List
from warehouse.storage_place import StoragePlace
from warehouse.parsers import (
    parse_storage_place,
    parse_storage_place_name,
    format_storage_place,
)
from warehouse.error import ApiError, AuthError
from warehouse.version import Version
from datetime import datetime


def _success():
    return jsonify({"message": "Success."})


def _log_legacy_request(version: Version):
    if version >= Version.V3:
        return
    now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    forward = forward = request.headers.get("X-Forwarded-For", default="")
    print(
        "DeprecatedCall@CC-VOL1: "
        "{ip} {time} {verb} {url} "
        "X-Forwarded-For={forward}".format(
            ip=request.remote_addr,
            time=now,
            verb=request.method,
            url=request.url,
            forward=forward,
        )
    )


def _auth(version: Version):
    if version < Version.V3:
        return
    if (request.authorization and
            "username" in request.authorization and
            request.authorization["username"] == "user" and
            "password" in request.authorization and
            request.authorization["password"] == "pass"):
        return
    raise AuthError()


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
        _log_legacy_request(self.version)
        _auth(self.version)

        name = parse_storage_place_name(request.json, self.version)
        if name in self.storage:
            raise ApiError("Storage place already exists.")
        storage_place = parse_storage_place(request.json, self.version)
        self.storage[storage_place.name] = storage_place
        return _success()

    def get(self):
        _log_legacy_request(self.version)
        _auth(self.version)

        if "x" not in request.args:
            raise ApiError("Must specify name.")
        name = request.args["x"]
        if name not in self.storage:
            raise ApiError("Storage place does not exist.")
        storage_place = self.storage[name]
        return jsonify(format_storage_place(storage_place, self.version))

    def put(self):
        _log_legacy_request(self.version)
        _auth(self.version)

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
        _log_legacy_request(self.version)
        _auth(self.version)

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
        _log_legacy_request(self.version)
        _auth(self.version)

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


class StoragePlacesForArticleApi:
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
        _log_legacy_request(self.version)
        _auth(self.version)

        article_id = int(request.args["x"])

        result: List[StoragePlace] = list(self.storage.values())

        # Filter storage places that have at least one item
        # of the article in stock.
        result = list(filter(
            lambda storage_place:
                storage_place.article_id == article_id and
                storage_place.stock > 0,
            result
        ))

        result = list(map(
            lambda storage_place: format_storage_place(
                storage_place,
                self.version
            ),
            result
        ))
        return jsonify(result)


class StoragePlacesAtLocationApi:
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
        _log_legacy_request(self.version)
        _auth(self.version)

        location = request.args["l"]
        count = int(request.args["n"])
        name = request.args["x"] if "x" in request.args else None

        result: List[StoragePlace] = list(self.storage.values())

        # Filter location.
        result = list(filter(
            lambda storage_place: storage_place.name.split("-")[0] == location,
            result
        ))

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
