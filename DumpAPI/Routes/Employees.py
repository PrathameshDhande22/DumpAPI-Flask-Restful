from flask import Blueprint
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import Delete, Select, Update
from sqlalchemy.exc import NoResultFound, DataError
from DumpAPI.Auth.token import token_required
from DumpAPI.database import Employee, db
from DumpAPI.utils import checkArgs, checkisNone, searchUsername, hashPassword

emp = Blueprint("emps", __name__, url_prefix="/emp")
api = Api(emp)

employee_args = RequestParser()
employee_args.add_argument(
    "id",
    type=str,
    location="forms",
    help="To get The Employee Detail Id is Necessary",
    required=True,
)
resource_fields = {
    "id": fields.Integer,
    "firstname": fields.String,
    "lastname": fields.String,
    "address": fields.String,
    "salary": fields.Integer,
    "age": fields.Integer,
    "deptid": fields.Integer,
}

update_emp_args = RequestParser()
update_emp_args.add_argument("firstname")
update_emp_args.add_argument("lastname")
update_emp_args.add_argument("address")
update_emp_args.add_argument("salary")
update_emp_args.add_argument("age")
update_emp_args.add_argument("username")
update_emp_args.add_argument("password")


class Emp(Resource):
    @marshal_with(resource_fields)
    @token_required
    def get(self, id):
        stmt = Select(Employee).where(Employee.id == id)
        result = db.session.execute(stmt).scalars().all()
        if result:
            return result[0]
        else:
            abort(404, message=f"Employee With ID {id} Not Found")

    @token_required
    def delete(self, id):
        stmt = Delete(Employee).where(Employee.id == id)
        db.session.execute(stmt)
        db.session.commit()
        return {"message": f"Successfully Deleted Employee with ID = {id}"}

    @token_required
    def post(self, id):
        args = update_emp_args.parse_args()
        if checkArgs(args):
            try:
                haspss = None
                usern = None
                if args.get("username"):
                    if searchUsername(args.get("username")):
                        abort(
                            409,
                            message=f"Username {args.get('username')} is Already Taken",
                        )
                    usern = args.get("username")
                if args.get("password"):
                    haspss = hashPassword(str(args.get("password")).strip())
                res = db.session.execute(Select(Employee).where(Employee.id == id)).scalar_one()
                stmt = (
                    Update(Employee)
                    .where(Employee.id == id)
                    .values(
                        firstname=checkisNone(args.get("firstname"), res.firstname),
                        lastname=checkisNone(args.get("lastname"), res.lastname),
                        address=checkisNone(args.get("address"), res.address),
                        salary=checkisNone(args.get("salary"), res.salary),
                        age=checkisNone(args.get("age"), res.age),
                        username=checkisNone(usern, res.username),
                        password=checkisNone(haspss, res.password),
                    )
                )

                db.session.execute(stmt)
                db.session.commit()
                return {"message": f"Employee With Id={id} Updated Successfully"}
            except DataError as e:
                abort(
                    401,
                    message="One or more Field is Invalid Make sure that salary and age should be integer not string.",
                )
        else:
            abort(401, message="You left One or More Field Empty Correct It.")


class EmpAll(Resource):
    @token_required
    def get(self):
        stmt = Select(Employee)
        try:
            result = db.session.execute(stmt).scalars().all()
            datas = []
            for res in result:
                jsondata = {
                    "id": res.id,
                    "firstname": res.firstname,
                    "lastname": res.lastname,
                    "address": res.address,
                    "salary": res.salary,
                    "age": res.age,
                    "deptid": res.deptid,
                }
                datas.append(jsondata)
            return {"employees": datas}
        except NoResultFound as es:
            abort(404, message="There are no Employees")


api.add_resource(Emp, "/<int:id>")
api.add_resource(EmpAll, "/all")
