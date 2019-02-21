# -*- coding: utf-8 -*-
# pylint: disable=R0201

"""
Module providing todo list resource.
"""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from bson import json_util, ObjectId
from application import mongo
from common.utils import validate_id


list_parser = RequestParser()
list_parser.add_argument("name", type=str, required=True, location="json")

db = mongo.db.todo


class TodoList(Resource):
    """
    Provides methods for retrieving, updating and deleting specific todo lists.

    Usage::
    For retrieving todo list:
        curl http://127.0.0.1:5000/todolists/<list_id> \
        -H "Content-Type: application/json"

    For updating todo list:
        curl -X PUT http://127.0.0.1:5000/todolists/<list_id> \
        -H "Content-Type: application/json" \
        -d '{"name": "somename"}'

    For deleting todo list:
        curl -X DELETE http://127.0.0.1:5000/todolists/<list_id> \
        -H "Content-Type: application/json"
    """
    def get(self, list_id):
        """
        Returns todo list.
        :param list_id: ID of todo list.
        """
        if not validate_id(list_id):
            return {"msg": "Invalid id, it should be 24-character string"}, 400
        result = db.find_one({"_id": ObjectId(list_id)})
        if result is None:
            return {"msg": "No such list found"}, 404
        return result

    def put(self, list_id):
        """
        Updates todo list.
        :param list_id: ID of todo list.
        """
        if not validate_id(list_id):
            return {"msg": "Invalid id, it should be 24-character string"}, 400
        name = list_parser.parse_args().get("name")
        result = db.update_one({"_id": ObjectId(list_id)}, {"$set": {"name": name}})
        if result.matched_count == 0:
            return {"msg": "No such list found"}, 404
        return {"msg": "Successfuly updated"}

    def delete(self, list_id):
        """
        Deletes todo list.
        :param list_id: ID of todo list.
        """
        if not validate_id(list_id):
            return {"msg": "Invalid id, it should be 24-character string"}, 400
        result = db.delete_one({"_id": ObjectId(list_id)})
        if result.matched_count == 0:
            return {"msg": "No such list found"}, 404
        return None, 204


class TodoListCollection(Resource):
    """
    Provides methods for retrieving and creating todo list.

    Usage::
    For retrieving all todo lists:
        curl http://127.0.0.1:5000/todolists \
        -H "Content-Type: application/json"

    For creating todo list:
        curl -X POST http://127.0.0.1:5000/todolists \
        -H "Content-Type: application/json" \
        -d '{"name": "somename"}'
    """
    def get(self):
        """
        Returns collection of todo lists.
        """
        return [item for item in db.find({})]

    def post(self):
        """
        Creates todo list.
        """
        name = list_parser.parse_args().get("name")
        db.insert_one({"name": name})
        return {"msg": "Successfuly added"}, 201
