from flask import Blueprint

from init import db
from models.players import Player, players_schema, player_schema

players_bp = Blueprint("players", __name__, url_prefix="/players")

# Create


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
