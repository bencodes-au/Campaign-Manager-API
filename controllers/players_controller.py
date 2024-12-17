from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.players import Player, players_schema, player_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
players_bp = Blueprint("players", __name__, url_prefix="/players")

# CREATE A PLAYER

# This function creates a new player
# To do this, the application:
# - Loads in the schema
# - Turns the entry fields for the entry into an object
# - Adds, commits and returns the new player
# - Checks for conflicts


@players_bp.route("/", methods=["POST"])
def create_player():

    try:
        # This loads in the player schema
        body_data = player_schema.load(request.get_json())

        # This creates a new object with the required criteria
        new_player = Player(
            first_name=body_data.get("first_name"),
            last_name=body_data.get("last_name"),
            email=body_data.get("email"),
            phone=body_data.get("phone")
        )

        # This adds and commits the entry
        db.session.add(new_player)
        db.session.commit()

        # This returns the new entry
        return player_schema.dump(new_player), 201

    # This checks for conflicts between requests and conditions, e.g., unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # This checks for breaches of UNIQUE
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409

# Read all


@players_bp.route("/")
def get_players():
    stmt = db.select(Player)
    players_list = db.session.scalars(stmt)
    data = players_schema.dump(players_list)
    return data

# Read a select


@players_bp.route("/<int:player_id>")
def get_student(player_id):
    stmt = db.select(Player).filter_by(id=player_id)
    player = db.session.scalar(stmt)
    if player:
        data = player_schema.dump(player)
        return data
    else:
        return {"message": f"Player with id {player_id} does not exist"}, 404

# Update


# Delete
@players_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    stmt = db.select(Player).filter_by(id=player_id)
    player = db.session.scalar(stmt)
    if player:
        db.session.delete(player)
        db.session.commit()

        return {"message": f"'{player.name}' was deleted successfully"}

    else:
        return {"message": f"Player with id {player_id} does not exist"}, 404
