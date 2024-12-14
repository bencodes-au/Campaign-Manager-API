from flask import Blueprint

from init import db
from models.played_games import Played_game, played_games_schema, played_game_schema

played_games_bp = Blueprint(
    "played_games", __name__, url_prefix="/played_games")

# Create


# Read all


@played_games_bp.route("/")
def get_played_games():
    stmt = db.select(Played_game)
    played_games_list = db.session.scalars(stmt)
    data = played_games_schema.dump(played_games_list)
    return data

# Read a select


@played_games_bp.route("/<int:played_game_id>")
def get_student(played_game_id):
    stmt = db.select(Played_game).filter_by(id=played_game_id)
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
    stmt = db.select(Played_game).filter_by(id=played_game_id)
    played_game = db.session.scalar(stmt)
    if played_game:
        db.session.delete(played_game)
        db.session.commit()

        return {"message": f"'{played_game.name}' was deleted successfully"}

    else:
        return {"message": f"Played Game with id {played_game_id} does not exist"}, 404
