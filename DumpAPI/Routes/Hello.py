from flask_restful import Api, Resource
from flask import Blueprint, jsonify

hello = Blueprint("hello", __name__, url_prefix="/")
api = Api(hello)


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}


class Test(Resource):
    def get(self):
        return {"Result": "The API is Working Correctfully"}


api.add_resource(HelloWorld, "/")
api.add_resource(Test, "/test")

