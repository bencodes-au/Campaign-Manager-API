from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.player_campaigns import PlayerCampaign, player_campaigns_schema, player_campaign_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the PlayerCampaign Controller.
player_campaigns_bp = Blueprint(
    "player_campaigns", __name__, url_prefix="/player_campaigns")

# CREATE A PLAYER CAMPAIGN

# This function creates a new player campaign
# To do this, the application:
# - Loads in the schema
# - Turns the player campaign fields into an object
# - Adds, commits and returns the new player campaign
# - Checks for conflicts


# This defines the route for the request. It is shortened by the above blueprint.
@player_campaigns_bp.route("/", methods=["POST"])
def create_player_campaign():

    try:
        # This loads in the player campaign schema
        body_data = player_campaign_schema.load(request.get_json())

        # This creates a new object with the required criteria
        new_player_campaign = PlayerCampaign(
            player_id=body_data.get("player_id"),
            campaign_id=body_data.get("campaign_id")
        )

        # This adds and commits the player campaign
        db.session.add(new_player_campaign)
        db.session.commit()

        # This returns the new player campaign
        return player_campaign_schema.dump(new_player_campaign), 201

    # This checks for conflicts between requests and conditions ie unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409


# READ ALL PLAYER CAMPAIGNS

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retrieves the result as a list
# - converts the data to JSON
# - returns the data


# This defines the route for the request. It is shortened by the above blueprint.
@player_campaigns_bp.route("/")
def get_player_campaigns():
    # This statement selects all inputs from the PlayerCampaign Table
    stmt = db.select(PlayerCampaign)
    # This retrieves the results as a list. Scalars will provide multiple results.
    player_campaigns_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = player_campaigns_schema.dump(player_campaigns_list)
    # This returns the list
    return data


# READ A SELECT PLAYER CAMPAIGN

# This function finds a select player campaign and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via its id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message


# This defines the route for a GET request. It is shortened by the above blueprint.
@player_campaigns_bp.route("/<int:player_id>/<int:campaign_id>")
def get_player_campaign(player_id, campaign_id):
    # This statement selects the entity based on the id and filters it using filter.by
    stmt = db.select(PlayerCampaign).filter_by(
        player_id=player_id, campaign_id=campaign_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    player_campaign = db.session.scalar(stmt)
    # Check if the player campaign matching the ids was found
    if player_campaign:
        # if so, convert into a json using .dump
        data = player_campaign_schema.dump(player_campaign)
        # return the data
        return data
    else:
        # return a 404 error message with the ids
        return {"message": f"Player campaign with player_id {player_id} and campaign_id {campaign_id} does not exist"}, 404


# UPDATE A PLAYER CAMPAIGN
# This function finds an object with the matching ids and replaces the contents with the new data
# To do this, the application:
# - Finds the player campaign (select), with the player and campaign ids (filter by) and loads it (.load)
# - If it exists, overwrite the data with the new request
# - Commits and returns the data
# - Integrity checks for Non Nullable and Unique constraints


# This defines the route for the UPDATE request. It is shortened by the above blueprint.
@player_campaigns_bp.route("/<int:player_id>/<int:campaign_id>", methods=["PUT", "PATCH"])
def update_player_campaign(player_id, campaign_id):
    try:
        # This finds the player campaign to be updated
        stmt = db.select(PlayerCampaign).filter_by(
            player_id=player_id, campaign_id=campaign_id)
        player_campaign = db.session.scalar(stmt)

        # This loads the data from the request
        body_data = player_campaign_schema.load(
            request.get_json(), partial=True)

        # If the player campaign exists
        if player_campaign:
            # Update the player campaign data using the data from the request body
            player_campaign.player_id = body_data.get(
                "player_id") or player_campaign.player_id
            player_campaign.campaign_id = body_data.get(
                "campaign_id") or player_campaign.campaign_id

            # Commit the changes
            db.session.commit()

            # Return the data
            return player_campaign_schema.dump(player_campaign)

        # If the player campaign doesn't exist
        else:
            # Return a 404 error message with the ids
            return {"message": f"Player campaign with player_id {player_id} and campaign_id {campaign_id} doesn't exist"}, 404

    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409


# DELETE A PLAYER CAMPAIGN
# This function deletes a player campaign by filtering for the player and campaign ids.
# To do so, the application:
# - Selects an entity (select and filter.by)
# - Retrieves the result
# - Deletes it
# - Commits the change


# This defines the route for the DELETE request. It is shortened by the above blueprint.
@player_campaigns_bp.route("/<int:player_id>/<int:campaign_id>", methods=["DELETE"])
def delete_player_campaign(player_id, campaign_id):
    # This statement selects the entity based on the player_id and campaign_id and filters it using filter.by
    stmt = db.select(PlayerCampaign).filter_by(
        player_id=player_id, campaign_id=campaign_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    player_campaign = db.session.scalar(stmt)
    # if it exists:
    if player_campaign:
        # delete the player campaign
        db.session.delete(player_campaign)
        # commit the changes
        db.session.commit()
        # Return success message
        return {"message": f"Player campaign with player_id {player_id} and campaign_id {campaign_id} was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 error message with the ids
        return {"message": f"Player campaign with player_id {player_id} and campaign_id {campaign_id} does not exist"}, 404
