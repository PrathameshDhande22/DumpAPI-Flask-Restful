from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text

db = SQLAlchemy()


class Department(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    name = Column(String(10), nullable=False)
    head = Column(String(30), nullable=False)


class Employee(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(10), nullable=False)
    lastname = Column(String(20), nullable=False)
    address = Column(String(40), nullable=False)
    salary = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    deptid = Column(Integer, ForeignKey(Department.id, ondelete="cascade"), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(Text, nullable=False)
