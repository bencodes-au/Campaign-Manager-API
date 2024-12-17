from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.campaigns import PlayerCampaign, player_campaigns_schema, player_campaign_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
player_campaigns_bp = Blueprint(
    "player_campaigns", __name__, url_prefix="/player_campaigns")

# CREATE A PLAYER CAMPAIGN

# This function assosciates a Player and a Campaign
# To do this, the application:
# - Uses the POST method to create a new record
# - Loads in the schema
# - Turns the entry fields for the entry into an object
# - Adds, commits and returns the new entry
# - Checks for conflicts


@player_campaigns_bp.route("/", methods=["POST"])
def create_player_campaign():

    try:
        # This loads in the player_campaign schema
        body_data = player_campaign_schema().load(request.get_json())

        # This creates a new object with the required criteria
        new_player_campaign = PlayerCampaign(
            player_id=body_data.get("player_id"),
            campaign_id=body_data.get("campaign_id")
        )

        # This adds and commits the entry
        db.session.add(new_player_campaign)
        db.session.commit()

        # This returns the new entry
        return player_campaign_schema().dump(new_player_campaign), 201
    # This checks for conflicts between requests and conditions ie unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # # This checks for breaches of UNIQUE
        # if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        #     return {"message": err.orig.diag.message_detail}, 409
