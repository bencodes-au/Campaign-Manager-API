import os

from flask import Flask

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.game_masters_controller import game_masters_bp
from controllers.players_controller import players_bp
from controllers.campaigns_controller import campaigns_bp
from controllers.characters_controller import characters_bp
from controllers.player_campaigns_controller import player_campaigns_bp
from controllers.played_games_controller import played_games_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Returns data in the order they've been added (instead of alphabetical)
    app.json.sort_keys = False

    # Initialises Libraries
    db.init_app(app)
    ma.init_app(app)

    # registers the controllers
    app.register_blueprint(db_commands)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(game_masters_bp)
    app.register_blueprint(played_games_bp)
    app.register_blueprint(player_campaigns_bp)
    app.register_blueprint(players_bp)

    return app
