from flask import Blueprint

from init import db
from models.characters import Character, characters_schema, character_schema

characters_bp = Blueprint("characters", __name__, url_prefix="/characters")

# Create


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
