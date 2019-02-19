# -*- coding: utf-8 -*-
# pylint: disable=R0201

"""
Module providing todo item resource.
"""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date, boolean
from bson import ObjectId
from application import mongo
from common.utils import validate_id


item_put_parser = RequestParser()
item_put_parser.add_argument("text", type=str, location="json")
item_put_parser.add_argument("dueDate", type=date, location="json")
item_put_parser.add_argument("finished", type=boolean, location="json")

item_post_parser = item_put_parser.copy()
for arg in item_post_parser.args:
    arg.required = True

db = mongo.db.todo


class TodoItem(Resource):
    """
    Provides methods for updating and deleting todo items.

    Usage::
    For updating todo item:
        curl -X PUT http://127.0.0.1:5000/todolists/<list_id>/items/<item_id> \
        -H "Content-Type: application/json" \
        -d '{"text": "sometext", "due_date": "2019-2-12", "finished": "true" }'

    For deleting todo item:
        curl -X DELETE http://127.0.0.1:5000/todolists/<list_id>/items/<item_id> \
        -H "Content-Type: application/json"
    """
    def put(self, list_id, item_id):
        """
        Updates todo item.
        :param list_id: ID of related todo list.
        :param item_id: ID of todo item.
        """
        if not validate_id(list_id, item_id):
            return {"msg": "Invalid id, it should be 24-character string"}, 400
        args = item_put_parser.parse_args()
        result = db.update_one(
            {"_id": ObjectId(list_id), "todos._id": ObjectId(item_id)},
            {
                "$set": {
                    "todos.$." + key: args[key] for key in args if args[key] is not None
                }
            }
        )
        if result.matched_count == 0:
            return {"msg": "No such list found"}, 404
        if result.modified_count == 0:
            return {"msg": "No item found"}, 404
        return {"msg": "Successfuly updated"}

    def delete(self, list_id, item_id):
        """
        Deletes todo item.
        :param list_id: ID of related todo list.
        :param item_id: ID of todo item.
        """
        if not validate_id(list_id, item_id):
            return {"msg": "Invalid id, it should be 24-character string"}, 400
        result = db.update_one(
            {"_id": ObjectId(list_id)},
            {"$pull": {"todos": {"_id": ObjectId(item_id)}}}
        )
        if result.matched_count == 0:
            return {"msg": "No such list found"}, 404
        if result.modified_count == 0:
            return {"msg": "No item found"}, 404
        return {"msg": "Successfuly deleted"}, 204


class TodoItemCollection(Resource):
    """
    Provides method for adding new todo item.

    Usage::

    For creating new todo item:
        curl -X POST http://127.0.0.1:5000/todolists/<list_id>/items \
        -d '{"text": "sometext", "due_date": "2019-2-12", "finished": "true" }'
    """
    def post(self, list_id):
        """
        Creates todo item
        :param list_id: ID of related todo list.
        """
        if not validate_id(list_id):
            return {"msg": "Invalid id, it should be 24-character string"}, 400
        args = item_post_parser.parse_args()
        result = db.update_one(
            {"_id": ObjectId(list_id)},
            {"$push": {"todos": {"_id": ObjectId(), **args}}}
        )
        if result.matched_count == 0:
            return {"msg": "No such list found"}, 404
        return {"msg": "Successfuly added"}, 201
