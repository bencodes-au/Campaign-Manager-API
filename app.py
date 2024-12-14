import os

from flask import Flask


from init import db, ma
from controllers.cli_controller import db_commands


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)

    app.register_bluebrint(db_commands)
