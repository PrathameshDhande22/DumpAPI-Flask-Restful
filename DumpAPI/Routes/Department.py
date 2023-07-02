from flask import Blueprint
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import Delete, Select
from sqlalchemy.exc import IntegrityError, NoResultFound
from DumpAPI.Auth.token import token_required
from DumpAPI.database import Department, db
from DumpAPI.utils import checkisNone

dept = Blueprint("dept", __name__, url_prefix="/dept")
api = Api(dept)

resource_fields = {"id": fields.Integer, "name": fields.String, "head": fields.String}

dept_args = RequestParser()
dept_args.add_argument(
    "name", help="Name is required is To register the Department", type=str, required=True
)
dept_args.add_argument(
    "head", help="Head is required is To register the Department", type=str, required=True
)


class Dept(Resource):
    @marshal_with(resource_fields)
    @token_required
    def get(self, id):
        stmt = Select(Department).where(Department.id == id)
        result = db.session.execute(stmt).scalars().fetchall()
        if result:
            return result[0]
        else:
            abort(404, message=f"Department with ID={id} Not Found")

    @token_required
    def put(self, id):
        args = dept_args.parse_args()
        if (
            args.get("head") == ""
            or str(args.get("head")).isspace()
            or args.get("name") == ""
            or str(args.get("name")).isspace()
        ):
            abort(401, message="You left one or more field empty Correct IT.")
        else:
            try:
                stmt = Select(Department).where(Department.id == id)
                result = db.session.execute(stmt).scalar_one()
                if result:
                    result.name = checkisNone(args.get("name"), result.name)
                    result.head = checkisNone(args.get("head"), result.head)
                    db.session.add(result)
                    db.session.commit()
                    return {"message": f"Department ID={id} Updated Successfully."}, 200
                else:
                    deptobj = Department(id=id, name=args.get("name"), head=args.get("head"))
                    db.session.add(deptobj)
                    db.session.commit()
                    return {"message": f"Department ID={id} Added Successfully."}, 201
            except IntegrityError as e:
                abort(409, message=f"Department id={id} already present")
            except NoResultFound as nota:
                deptobj = Department(id=id, name=args.get("name"), head=args.get("head"))
                db.session.add(deptobj)
                db.session.commit()
                return {"message": f"Department ID={id} Added Successfully."}, 201

    @token_required
    def delete(self, id):
        stmt = Delete(Department).where(Department.id == id)
        db.session.execute(stmt)
        db.session.commit()
        return {"message": f"Successfully Deleted Department id={id}."}


class DeptAll(Resource):
    @token_required
    def get(self):
        result = db.session.execute(Select(Department)).scalars().all()
        data = []
        if result:
            for res in result:
                resdict = {"id": res.id, "name": res.name, "head": res.head}
                data.append(resdict)
            return {"departments": data}
        else:
            abort(404, message="There are Departments")


api.add_resource(DeptAll, "/all")
api.add_resource(Dept, "/<int:id>")
