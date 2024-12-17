import os

from flask import Flask


from init import db, ma
from controllers.cli_controller import db_commands
from controllers.campaigns_controller import db_campaigns
from controllers.characters_controller import db_characters
from controllers.game_masters_controller import db_game_masters
from controllers.played_games_controller import db_played_games
from controllers.player_campaigns_controller import db_player_campaigns
from controllers.players_controller import db_players


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(db_campaigns)
    app.register_blueprint(db_characters)
    app.register_blueprint(db_game_masters)
    app.register_blueprint(db_played_games)
    app.register_blueprint(db_player_campaigns)
    app.register_blueprint(db_players)
