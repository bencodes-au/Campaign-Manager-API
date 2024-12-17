from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.characters import Character, characters_schema, character_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Character Controller.
characters_bp = Blueprint("characters", __name__, url_prefix="/characters")

# CREATE A CHARACTER

# This function creates a new entry
# To do this, the application:
# - Loads in the schema
# - Turns the entry fields for the entry into an object
# - Adds, commits and returns the new entry
# - Checks for conflicts


# This defines the route for the request. It is shortened by the above blueprint.
@characters_bp.route("/", methods=["POST"])
def create_character():

    try:
        # This loads in the character schema
        body_data = character_schema().load(request.get_json())

        # This creates a new object with the required criteria
        new_character = Character(
            name=body_data.get("name"),
            backstory=body_data.get("backstory"),
            skills=body_data.get("skills"),
            campaign_id=body_data.get("campaign_id"),
            player_id=body_data.get("player_id")
        )

        # This adds and commits the entry
        db.session.add(new_character)
        db.session.commit()

        # This returns the new entry
        return character_schema().dump(new_character), 201
    # This checks for conflicts between requests and conditions ie unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409

# READ ALL CHARACTERS

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retreives the result as a list
# - converts the data to JSON
# - returns the data

# This defines the route for the request. It is shortened by the above blueprint.


@characters_bp.route("/")
def get_characters():
    # This statement selects all inputs from the Character table using the Character Class
    stmt = db.select(Character)
    # This retrieves the results as a list. Scalars will provide multiple results.
    characters_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = characters_schema.dump(characters_list)
    # This returns the list
    return data

# READ A SELECT CHARACTER

# This function finds a select character and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via it's id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message


# This defines the route for a GET request. It is shortened by the above blueprint.
@characters_bp.route("/<int:character_id>")
def get_character(character_id):
    # This statement selects the entity based on the id and filters it using filter.by
    stmt = db.select(Character).filter_by(id=character_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    character = db.session.scalar(stmt)
    # Check if the character matching the idea was found
    if character:
        # if so, convert into a json using .dump
        data = character_schema.dump(character)
        # return the data
        return data
    else:
        # else return a 404 error message with the id
        return {"message": f"Character with id {character_id} does not exist"}, 404

# UPDATE A CHARACTER
# This function finds an object with the matching id and replaces the contents with the new data
# To do this, this application:
# - Finds the character (select), with the character id (filter by) and loads it (.load)
# - If it exists, overwrite the data with the new request
# - Commits and returns the data
# - Integrity checks for Non Nullable and Unique constraints


# This defines the route for the UPDATE request. It is shortened by the above blueprint.
@characters_bp.route("/<int:character_id>", methods=["PUT", "PATCH"])
def update_character(character_id):
    try:
        # This finds the character to be updated
        stmt = db.select(Character).filter_by(id=character_id)
        character = db.session.scalar(stmt)

        # This loads the data from the request
        body_data = character_schema.load(request.get_json(), partial=True)

        # If the character exists
        if character:
            # Update the character data using the data from the request body
            character.name = body_data.get("name") or character.name
            character.backstory = body_data.get(
                "backstory") or character.backstory
            character.skills = body_data.get("skills") or character.skills
            character.campaign_id = body_data.get(
                "campaign_id") or character.campaign_id
            character.player_id = body_data.get(
                "player_id") or character.player_id

            # Commit the changes
            db.session.commit()

            # Return the updated character data
            return character_schema.dump(character)

        # If the character doesn't exist
        else:
            # Return a 404 error message with the id
            return {"message": f"Character with id {character_id} doesn't exist"}, 404

    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409

# DELETE A CHARACTER
# This function deletes an character by filtering for the id.
# To do so, the application:
# - Selects an entity (select and filter.by)
# - Retrieves the result
# - Deletes it
# - Commits the change


# This defines the route for the DELETE request. It is shortened by the above blueprint.
@characters_bp.route("/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    # This statement selects the campaign based on the id and filters it using filter.by
    stmt = db.select(Character).filter_by(id=character_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    character = db.session.scalar(stmt)
    # if it exists:
    if character:
        # delete the character
        db.session.delete(character)
        # commit the changes
        db.session.commit()
        # return success message
        return {"message": f"'{character.name}' was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 error message with the id
        return {"message": f"Character with id {character_id} does not exist"}, 404
