# -*- coding: utf-8 -*-

"""
Module for creating application and configuring database and routes.
"""

import json
from flask import Flask, request, abort
from flask_restful import Api
from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()


class Encoder(json.JSONEncoder):
    """
    Custom encoder for proper serialization of ObjectId and date
    """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return obj


def create_app():
    app = Flask(__name__)
    app.config['RESTFUL_JSON'] = {'cls': Encoder}

    @app.before_request
    def before_request():
        if not request.is_json:
            abort(400)

    # Change next line if you want to use other collection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/todo"
    mongo.init_app(app)
    api = Api(app)
    from resources.todo_item import TodoItem, TodoItemCollection
    from resources.todo_list import TodoList, TodoListCollection
    api.add_resource(TodoListCollection, "/todolists")
    api.add_resource(TodoList, "/todolists/<string:list_id>")
    api.add_resource(TodoItemCollection, "/todolists/<string:list_id>/items")
    api.add_resource(TodoItem, "/todolists/<string:list_id>/items/<string:item_id>")
    return app
