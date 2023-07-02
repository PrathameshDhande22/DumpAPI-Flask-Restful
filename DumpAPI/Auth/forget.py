import os
import jwt
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from sqlalchemy import Select
from sqlalchemy.exc import NoResultFound
from DumpAPI.utils import hashPassword
from ..database import Employee, db

header_args = RequestParser()
header_args.add_argument(
    "Token", help="Token is Required in the Header", required=True, location="headers"
)


set_pass_args = RequestParser()
set_pass_args.add_argument(
    "password",
    help="Password is Required in the URL to set the password",
    type=str,
    location="args",
    required=True,
)


class ForgetSystem(Resource):
    def put(self):
        hargs = header_args.parse_args().get("Token")
        args = set_pass_args.parse_args().get("password")
        if str(args).isspace() or args=="":
            abort(401,message="Password should no contain any Space")
        try:
            data = jwt.decode(hargs, key=os.getenv("JWT_KEY"), algorithms=["HS256"])
            hasshedpass = hashPassword(args)
            stmt = Select(Employee).where(Employee.username == data.get("username"))
            try:
                result = db.session.execute(stmt).scalars().fetchall()
                result[0].password = hasshedpass
                db.session.add(result[0])
                db.session.commit()
                return {"message": "Updated Successfully"}
            except NoResultFound as es:
                abort(404, message="User Not Found")
        except jwt.InvalidSignatureError as e:
            abort(401, message="Invalid Token")
        except jwt.DecodeError as w:
            abort(401, message="Invalid Token")
