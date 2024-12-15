from flask import Blueprint

from init import db
from models.game_masters import GameMaster, game_masters_schema, game_master_schema

game_masters_bp = Blueprint(
    "game_masters", __name__, url_prefix="/game_masters")

# Create


# Read all


@game_masters_bp.route("/")
def get_game_masters():
    stmt = db.select(GameMaster)
    game_masters_list = db.session.scalars(stmt)
    data = game_masters_schema.dump(game_masters_list)
    return data

# Read a select


@game_masters_bp.route("/<int:game_master_id>")
def get_student(game_master_id):
    stmt = db.select(GameMaster).filter_by(id=game_master_id)
    game_master = db.session.scalar(stmt)
    if game_master:
        data = game_master_schema.dump(game_master)
        return data
    else:
        return {"message": f"Game master with id {game_master_id} does not exist"}, 404

# Update


# Delete
@game_masters_bp.route("/<int:game_master_id>", methods=["DELETE"])
def delete_game_master(game_master_id):
    stmt = db.select(GameMaster).filter_by(id=game_master_id)
    game_master = db.session.scalar(stmt)
    if game_master:
        db.session.delete(game_master)
        db.session.commit()

        return {"message": f"'{game_master.name}' was deleted successfully"}

    else:
        return {"message": f"Game Master with id {game_master_id} does not exist"}, 404
