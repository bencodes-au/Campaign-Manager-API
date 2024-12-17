from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.game_masters import GameMaster, game_masters_schema, game_master_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Game Master Controller.
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

    except DataError as err:
        # This handles invalid data (email and phone format)
        return {"message": err.orig.diag.message_primary}, 400

# READ ALL GAME MASTERS

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retreives the result as a list
# - converts the data to JSON
# - returns the data


# This defines the route for the request. It is shortened by the above blueprint.
@game_masters_bp.route("/")
def get_game_masters():
    # This statement selects all inputs from the game master table using the GameMaster Class
    stmt = db.select(GameMaster)
    # This retrieves the results as a list. Scalars will provide multiple results.
    game_masters_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = game_masters_schema.dump(game_masters_list)
    # This returns the list
    return data

# READ A SELECT GAME MASTER

# This function finds a select game master and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via it's id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message


# This defines the route for a GET request. It is shortened by the above blueprint.
@game_masters_bp.route("/<int:game_master_id>")
def get_game_master(game_master_id):
    # This statement selects the game master based on the id and filters it using filter.by
    stmt = db.select(GameMaster).filter_by(id=game_master_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    game_master = db.session.scalar(stmt)
    # Check if the campaign matching the idea was found
    if game_master:
        # if so, convert into a json using .dump
        data = game_master_schema.dump(game_master)
        # return the data
        return data
    else:
        # else return a 404 error message with the id
        return {"message": f"Game master with id {game_master_id} does not exist"}, 404

# UPDATE A GAME MASTER
# This function finds a GameMaster object with the matching id and updates the data
# To do this, the application:
# - Finds the GameMaster (select), with the game master id (filter by) and loads it (.load)
# - If it exists, overwrite the data with the new request
# - Commits and returns the data
# - Integrity checks for Non Nullable and Unique constraints


# This defines the route for the UPDATE request. It is shortened by the above blueprint.
@game_masters_bp.route("/<int:game_master_id>", methods=["PUT", "PATCH"])
def update_game_master(game_master_id):
    try:
        # This finds the game master to be updated
        stmt = db.select(GameMaster).filter_by(id=game_master_id)
        game_master = db.session.scalar(stmt)

        # This loads the data from the request body
        body_data = game_master_schema.load(request.get_json(), partial=True)

        # If the game master exists
        if game_master:
            # Update the game master data using the data from the request body
            game_master.first_name = body_data.get(
                "first_name") or game_master.first_name
            game_master.last_name = body_data.get(
                "last_name") or game_master.last_name
            game_master.email = body_data.get("email") or game_master.email
            game_master.phone = body_data.get("phone") or game_master.phone

            # Commit the changes
            db.session.commit()

            # Return the updated data
            return game_master_schema.dump(game_master)

        # If the game master doesn't exist
        else:
            # Return a 404 error message with the id
            return {"message": f"Game Master with id {game_master_id} doesn't exist"}, 404

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

# DELETE A GAME MASTER
# This function deletes a game master by filtering for the id.
# To do so, the application:
# - Selects an entity (select and filter.by)
# - Retrieves the result
# - Deletes it
# - Commits the change


# This defines the route for the DELETE request. It is shortened by the above blueprint.
@game_masters_bp.route("/<int:game_master_id>", methods=["DELETE"])
def delete_game_master(game_master_id):
    # This statement selects the game master based on the id and filters it using filter.by
    stmt = db.select(GameMaster).filter_by(id=game_master_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    game_master = db.session.scalar(stmt)
    # if it exists:
    if game_master:
        # delete the game master
        db.session.delete(game_master)
        # commit the changes
        db.session.commit()
        # return success message
        return {"message": f"'{game_master.name}' was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 message with the id
        return {"message": f"Game Master with id {game_master_id} does not exist"}, 404
