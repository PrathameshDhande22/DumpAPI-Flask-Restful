import os
from flask_restful import abort
import jwt
from functools import wraps
from flask_restful.reqparse import RequestParser
from sqlalchemy import Select
from ..database import Employee, db
from ..utils import checkpassword
from sqlalchemy.exc import NoResultFound

headerargs = RequestParser()
headerargs.add_argument(
    "Token", help="Token is Missing From the header", location="headers", required=True
)


def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        args = headerargs.parse_args()
        token = args.get("Token")
        try:
            data = jwt.decode(token, key=os.getenv("JWT_KEY"), algorithms=["HS256"])
            stmt = Select(Employee).where(Employee.username == data.get("username"))
            try:
                res = db.session.execute(stmt).scalar_one()
                if checkpassword(res.password, data.get("password")) is False:
                    abort(401, message="Invalid Password")
            except NoResultFound as no:
                abort(404, message="No Username Found")

        except jwt.InvalidSignatureError as e:
            abort(401, message="Invalid Token")
        except jwt.DecodeError as d:
            abort(401, message="Invalid Token")
        return f(*args, **kwargs)

    return check_token
