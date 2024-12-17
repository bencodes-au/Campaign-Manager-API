from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.game_masters import GameMaster, game_masters_schema, game_master_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
game_masters_bp = Blueprint(
    "game_masters", __name__, url_prefix="/game_masters")

# CREATE A GAME MASTER

# This function creates a new entry
# To do this, the application:
# - Loads in the schema
# - Turns the entry fields for the entry into an object
# - Adds, commits and returns the new entry
# - Checks for conflicts

# This defines the route for the request. It is shortened by the above blueprint.


@game_masters_bp.route("/", methods=["POST"])
def create_game_master():

    try:
        # This loads in the game master schema
        body_data = game_master_schema.load(request.get_json())

        # This creates a new object with the required criteria
        new_game_master = GameMaster(
            first_name=body_data.get("first_name"),
            last_name=body_data.get("last_name"),
            email=body_data.get("email"),
            phone=body_data.get("phone")
        )

        # This adds and commits the entry
        db.session.add(new_game_master)
        db.session.commit()

        # This returns the new entry
        return game_master_schema.dump(new_game_master), 201

    # This checks for conflicts between requests and conditions, e.g., unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # This checks for breaches of UNIQUE
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409
# Read all


@game_masters_bp.route("/")
def get_game_masters():
    stmt = db.select(GameMaster)
    game_masters_list = db.session.scalars(stmt)
    data = game_masters_schema.dump(game_masters_list)
    return data

# Read a select


@game_masters_bp.route("/<int:game_master_id>")
def get_student(game_master_id):
    stmt = db.select(GameMaster).filter_by(id=game_master_id)
    game_master = db.session.scalar(stmt)
    if game_master:
        data = game_master_schema.dump(game_master)
        return data
    else:
        return {"message": f"Game master with id {game_master_id} does not exist"}, 404

# Update


# Delete
@game_masters_bp.route("/<int:game_master_id>", methods=["DELETE"])
def delete_game_master(game_master_id):
    stmt = db.select(GameMaster).filter_by(id=game_master_id)
    game_master = db.session.scalar(stmt)
    if game_master:
        db.session.delete(game_master)
        db.session.commit()

        return {"message": f"'{game_master.name}' was deleted successfully"}

    else:
        return {"message": f"Game Master with id {game_master_id} does not exist"}, 404
