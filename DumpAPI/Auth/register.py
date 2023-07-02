from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from ..database import Employee, db
from DumpAPI.utils import (
    getDeptID,
    getToken,
    hashPassword,
    searchUsername,
)
from sqlalchemy.exc import DataError

register_args = RequestParser()
register_args.add_argument(
    "firstname", help="First Name is Required to Register", required=True, type=str
)
register_args.add_argument(
    "lastname", help="Last Name is Required to Register", required=True
)
register_args.add_argument(
    "address", help="Address is Required to Register", required=True
)
register_args.add_argument(
    "salary", help="Salary is Required to Register", required=True
)
register_args.add_argument("age", help="Age is Required to Register", required=True)
register_args.add_argument(
    "username", help="Username is Required to Register", required=True
)
register_args.add_argument(
    "password", help="Password is Required to Register", required=True
)


class Register(Resource):
    def post(self):
        args = register_args.parse_args()
        deptid = getDeptID()
        if str(args.get("password")).isspace() or str(args.get("password")) == "":
            abort(401, message="Enter Password")
        elif str(args.get("username")).isspace() or str(args.get("username")) == "":
            abort(401, message="Enter Username")

        if searchUsername(args.get("username")):
            abort(409, message=f"Username {args.get('username')} is Already Taken")
        haspss = hashPassword(str(args.get("password")).strip())
        try:
            em = Employee(
                firstname=args.get("firstname"),
                lastname=args.get("lastname"),
                address=args.get("address"),
                salary=args.get("salary"),
                age=args.get("age"),
                deptid=deptid,
                username=args.get("username"),
                password=haspss,
            )
            token = getToken(args.get("password"), username=args.get("username"))
            db.session.add(em)
            db.session.commit()
            return {"message": "Register Successfully", "token": token},201
        except DataError as dt:
            abort(401,message="One or more Field is Invalid Make sure that salary and age should be integer not string.")
