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


# This defines the route for the request. It is shortened by the above blueprint.
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

# READ ALL PLAYED GAMES

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retreives the result as a list
# - converts the data to JSON
# - returns the data


# This defines the route for the request. It is shortened by the above blueprint.
@played_games_bp.route("/")
def get_played_games():
    # This statement selects all inputs from the Played Games table using the Played Games Class
    stmt = db.select(PlayedGame)
    # This retrieves the results as a list. Scalars will provide multiple results.
    played_games_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = played_games_schema.dump(played_games_list)
    # This returns the list
    return data

# READ A SELECT PLAYED GAME
# This function finds a select campaign and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via it's id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message

# This defines the route for the request. It is shortened by the above blueprint.


@played_games_bp.route("/<int:played_game_id>")
def get_played_game(played_game_id):
    stmt = db.select(PlayedGame).filter_by(id=played_game_id)
    played_game = db.session.scalar(stmt)
    if played_game:
        data = played_game_schema.dump(played_game)
        return data
    else:
        return {"message": f"Played Game with id {played_game_id} does not exist"}, 404

# UPDATE A PLAYED GAME
# This function finds a PlayedGame object with the matching id and updates the data
# To do this, the application:
# - Finds the PlayedGame (select), with the played game id (filter by) and loads it (.load)
# - If it exists, overwrite the data with the new request
# - Commits and returns the data
# - Integrity checks for Non Nullable and Unique constraints


# This defines the route for the request. It is shortened by the above blueprint.
@played_games_bp.route("/<int:played_game_id>", methods=["PUT", "PATCH"])
def update_played_game(played_game_id):
    try:
        # This finds the played game to be updated
        stmt = db.select(PlayedGame).filter_by(id=played_game_id)
        played_game = db.session.scalar(stmt)

        # This loads the data from the request body
        body_data = played_game_schema.load(request.get_json(), partial=True)

        # If the played game exists
        if played_game:
            # Update the played game data using the data from the request body
            played_game.synopsis = body_data.get(
                "synopsis") or played_game.synopsis
            played_game.campaign_id = body_data.get(
                "campaign_id") or played_game.campaign_id

            # Commit the changes
            db.session.commit()

            # Return the updated data
            return played_game_schema.dump(played_game)

        # If the played game doesn't exist
        else:
            # Return a 404 error message with the id
            return {"message": f"Played Game with id {played_game_id} doesn't exist"}, 404

    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409

# DELETE A PLAYED GAME
# This function deletes a campaign by filtering for the id.
# To do so, the application:
# - Selects an entity (select and filter.by)
# - Retrieves the result
# - Deletes it
# - Commits the change


# This defines the route for the DELETE request. It is shortened by the above blueprint.
@played_games_bp.route("/<int:played_game_id>", methods=["DELETE"])
def delete_played_game(played_game_id):
    # This statement selects the played game based on the id and filters it using filter.by
    stmt = db.select(PlayedGame).filter_by(id=played_game_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    played_game = db.session.scalar(stmt)
    # if it exists
    if played_game:
        # delete the played game
        db.session.delete(played_game)
        # commit the changes
        db.session.commit()
        # return a success message
        return {"message": f"'{played_game.name}' was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 error message with the id
        return {"message": f"Played Game with id {played_game_id} does not exist"}, 404
