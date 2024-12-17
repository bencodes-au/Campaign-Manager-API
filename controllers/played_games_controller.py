from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.played_games import PlayedGame, played_games_schema, played_game_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
played_games_bp = Blueprint(
    "played_games", __name__, url_prefix="/played_games")

# CREATE A PLAYED GAME

# This function creates a new entry
# To do this, the application:
# - Loads in the schema
# - Turns the entry fields for the entry into an object
# - Adds, commits and returns the new entry
# - Checks for conflicts


@played_games_bp.route("/", methods=["POST"])
def create_played_game():

    try:
        # This loads in the played game schema
        body_data = played_game_schema.load(request.get_json())

        # This creates a new object with the required criteria
        new_played_game = PlayedGame(
            synopsis=body_data.get("synopsis"),
            campaign_id=body_data.get("campaign_id")
        )

        # This adds and commits the entry
        db.session.add(new_played_game)
        db.session.commit()

        # This returns the new entry
        return played_game_schema.dump(new_played_game), 201

 # This checks for conflicts between requests and conditions, e.g., unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # # This checks for breaches of UNIQUE
        # if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        #     return {"message": err.orig.diag.message_detail}, 409

# Read all


@played_games_bp.route("/")
def get_played_games():
    stmt = db.select(PlayedGame)
    played_games_list = db.session.scalars(stmt)
    data = played_games_schema.dump(played_games_list)
    return data

# Read a select


@played_games_bp.route("/<int:played_game_id>")
def get_student(played_game_id):
    stmt = db.select(PlayedGame).filter_by(id=played_game_id)
    played_game = db.session.scalar(stmt)
    if played_game:
        data = played_game_schema.dump(played_game)
        return data
    else:
        return {"message": f"Played Game with id {played_game_id} does not exist"}, 404

# Update


# Delete
@played_games_bp.route("/<int:played_game_id>", methods=["DELETE"])
def delete_played_game(played_game_id):
    stmt = db.select(PlayedGame).filter_by(id=played_game_id)
    played_game = db.session.scalar(stmt)
    if played_game:
        db.session.delete(played_game)
        db.session.commit()

        return {"message": f"'{played_game.name}' was deleted successfully"}

    else:
        return {"message": f"Played Game with id {played_game_id} does not exist"}, 404
