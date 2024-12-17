from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.players import Player, players_schema, player_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the player Controller.
players_bp = Blueprint("players", __name__, url_prefix="/players")

# CREATE A PLAYER

# This function creates a new player
# To do this, the application:
# - Loads in the schema
# - Turns the entry fields for the entry into an object
# - Adds, commits and returns the new player
# - Checks for conflicts


# This defines the route for the request. It is shortened by the above blueprint.
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
    except DataError as err:
        # This handles invalid data (email and phone format)
        return {"message": err.orig.diag.message_primary}, 400

# READ ALL playerS

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retreives the result as a list
# - converts the data to JSON
# - returns the data


# This defines the route for the request. It is shortened by the above blueprint.
@players_bp.route("/")
def get_players():
    # This statement selects all inputs from the players table using the Player Class
    stmt = db.select(Player)
    # This retrieves the results as a list. Scalars will provide multiple results.
    players_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = players_schema.dump(players_list)
    # This returns the list
    return data

# READ A SELECT PLAYER

# This function finds a select player and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via it's id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message


# This defines the route for a GET request. It is shortened by the above blueprint.
@players_bp.route("/<int:player_id>")
def get_player(player_id):
    # This statement selects the player based on the id and filters it using filter.by
    stmt = db.select(Player).filter_by(id=player_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    player = db.session.scalar(stmt)
    # Check if the player matching the idea was found
    if player:
        # if so, convert into a json using .dump
        data = player_schema.dump(player)
        # return the data
        return data
    else:
        # else return a 404 error message with the id
        return {"message": f"Player with id {player_id} does not exist"}, 404

# UPDATE A PLAYER
# This function finds a Player object with the matching id and updates its data
# To do this, the application:
# - Finds the Player (select), with the player id (filter by) and loads it (.load)
# - If it exists, overwrite the data with the new request
# - Commits and returns the data
# - Integrity checks for Non Nullable and Unique constraints


@players_bp.route("/<int:player_id>", methods=["PUT", "PATCH"])
def update_player(player_id):
    try:
        # This finds the Player to be updated based on player_id
        stmt = db.select(Player).filter_by(id=player_id)
        player = db.session.scalar(stmt)

        # This loads the data from the request body
        body_data = player_schema.load(request.get_json(), partial=True)

        # If the Player exists
        if player:
            # Update the player data using the data from the request body
            player.first_name = body_data.get(
                "first_name") or player.first_name
            player.last_name = body_data.get("last_name") or player.last_name
            player.email = body_data.get("email") or player.email
            player.phone = body_data.get("phone") or player.phone

            # Commit the changes
            db.session.commit()

            # Return the updated data
            return player_schema.dump(player)

        # If the Player doesn't exist
        else:
            # Return a 404 error message with the player_id
            return {"message": f"Player with id {player_id} doesn't exist"}, 404

    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # This checks breaches of UNIQUE
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409

    except DataError as err:
        # This handles invalid data (email and phone)
        return {"message": err.orig.diag.message_primary}, 400

# DELETE A PLAYER
# This function deletes a player by filtering for the id.
# To do so, the application:
# - Selects an entity (select and filter.by)
# - Retrieves the result
# - Deletes it
# - Commits the change

# This defines the route for the DELETE request. It is shortened by the above blueprint.


@players_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    # This statement selects the player based on the id and filters it using filter.by
    stmt = db.select(Player).filter_by(id=player_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    player = db.session.scalar(stmt)
    # if it exists:
    if player:
        # delete the player
        db.session.delete(player)
        # commit the changes
        db.session.commit()
        # Return success message
        return {"message": f"'{player.name}' was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 error message with the id
        return {"message": f"Player with id {player_id} does not exist"}, 404
