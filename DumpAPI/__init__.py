import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_YUGA")
    from .database import db

    db.init_app(app)

    # uncomment these two lines to create all the database the comment these lines.
    # with app.app_context():
    #     db.create_all()

    # registering routes
    from .Routes import hello, emp, dept
    from .Auth import auth

    app.register_blueprint(hello)
    app.register_blueprint(emp)
    app.register_blueprint(dept)
    app.register_blueprint(auth)

    # registering error page
    from .error import errorpage, errorpage1, error400

    app.register_error_handler(404, errorpage)
    app.register_error_handler(500, errorpage1)
    app.register_error_handler(400, error400)
    app.register_error_handler(415, error400)

    return app
