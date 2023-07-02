import os
import jwt
from sqlalchemy import Select
from .database import Department, Employee, db
import random
from cryptography.fernet import Fernet


def getDeptID() -> int:
    ids = db.session.execute(Select(Department.id).select_from(Department)).fetchall()
    choice = random.choice(ids)
    return choice[0]


def searchUsername(username: str) -> bool:
    stmt = Select(Employee.username).where(Employee.username == username)
    data = db.session.execute(stmt).scalar()
    if data is None:
        return False
    else:
        return True


def hashPassword(password: str) -> str:
    key = os.getenv("ENCRYPT_KEY").encode()
    k = Fernet(key)
    return k.encrypt(password.encode()).decode()


def checkpassword(hashedPassword: str, password: str) -> bool:
    key = os.getenv("ENCRYPT_KEY").encode()
    k = Fernet(key)
    return k.decrypt(hashedPassword).decode() == password


def getToken(password, username) -> str:
    token = jwt.encode(
        {"username": username, "password": password},
        key=os.getenv("JWT_KEY"),
        algorithm="HS256",
    )
    return token


def checkArgs(args: dict) -> bool:
    firstn = str(args.get("firstname"))
    lastn = str(args.get("firstname"))
    address = str(args.get("firstname"))
    salary = str(args.get("firstname"))
    age = str(args.get("firstname"))
    username = str(args.get("firstname"))
    password = str(args.get("firstname"))
    if (
        firstn.isspace()
        or lastn.isspace()
        or address.isspace()
        or username.isspace()
        or password.isspace()
    ):
        return False
    elif firstn == "" or lastn == "" or address == "" or username == "" or password == "":
        return False
    return True


def checkisNone(first: str, second: str) -> str:
    if first is None:
        return second
    return first
