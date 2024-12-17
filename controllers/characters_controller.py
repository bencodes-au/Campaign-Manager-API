from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.characters import Character, characters_schema, character_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
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

# Read all


@characters_bp.route("/")
def get_characters():
    stmt = db.select(Character)
    characters_list = db.session.scalars(stmt)
    data = characters_schema.dump(characters_list)
    return data

# Read a select


@characters_bp.route("/<int:character_id>")
def get_character(character_id):
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    if character:
        data = character_schema.dump(character)
        return data
    else:
        return {"message": f"Character with id {character_id} does not exist"}, 404

# Update


# Delete
@characters_bp.route("/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    if character:
        db.session.delete(character)
        db.session.commit()

        return {"message": f"'{character.name}' was deleted successfully"}

    else:
        return {"message": f"Character with id {character_id} does not exist"}, 404
