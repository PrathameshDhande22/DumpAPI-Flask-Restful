import os
import jwt
from flask import Blueprint
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import Select
from sqlalchemy.exc import NoResultFound
from DumpAPI.utils import checkpassword, getToken
from ..database import Employee, db

auth = Blueprint("auth", __name__, url_prefix="/auth")

api = Api(auth)

login_args = RequestParser()
login_args.add_argument(
    "username",
    help="Username is Required to generate the Access Token",
    required=True,
    location="args",
)
login_args.add_argument(
    "password",
    help="Password is Required to generate the Access Token",
    required=True,
    location="args",
)


class LoginSystem(Resource):
    def get(self):
        args = login_args.parse_args()
        if str(args).isspace() or args == "":
            abort(401, message="Password should no contain any Space")
        stmt = Select(Employee).where(Employee.username == args.get("username"))
        try:
            data = db.session.execute(stmt).scalar_one()
            if checkpassword(data.password, args.get("password")):
                token = getToken(password=args.get("password"), username=args.get("username"))
                return {"message": "Login Success", "token": token}, 202
            else:
                abort(401, message="Invalid Password")
        except NoResultFound as no:
            abort(404, message="No Username Found")


header_args = RequestParser()
header_args.add_argument(
    "Token", help="Token is Required in the Header", required=True, location="headers"
)

resource_fields = {
    "id": fields.Integer,
    "firstname": fields.String,
    "lastname": fields.String,
    "address": fields.String,
    "salary": fields.Integer,
    "age": fields.Integer,
    "deptid": fields.Integer,
    "username": fields.String,
}


class YourSelf(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = header_args.parse_args()
        try:
            data = jwt.decode(args.get("Token"), key=os.getenv("JWT_KEY"), algorithms=["HS256"])
            stmt = Select(Employee).where(Employee.username == data.get("username"))
            try:
                res = db.session.execute(stmt).scalar_one()
                if checkpassword(res.password, data.get("password")):
                    return res
                else:
                    abort(401, message="Invalid Password")
            except NoResultFound as no:
                abort(404, message="No Username Found")

        except jwt.InvalidSignatureError as e:
            abort(401, message="Invalid Token")
        except jwt.DecodeError as d:
            abort(401, message="Invalid Token")


from .forget import ForgetSystem
from .register import Register

api.add_resource(ForgetSystem, "/forget")
api.add_resource(YourSelf, "/me")
api.add_resource(LoginSystem, "/login")
api.add_resource(Register, "/register")
