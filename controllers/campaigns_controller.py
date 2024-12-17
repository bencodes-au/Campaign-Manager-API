from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.campaigns import Campaign, campaigns_schema, campaign_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
campaigns_bp = Blueprint("campaigns", __name__, url_prefix="/campaigns")

# CREATE A CAMPAIGN

# This function creates a new campaign
# To do this, the application:
# - Loads in the schema
# - Turns the campaign fields for the campaign into an object
# - Adds, commits and returns the new campaign
# - Checks for conflicts


# This defines the route for the request. It is shortened by the above blueprint.
@campaigns_bp.route("/", methods=["POST"])
def create_campaign():

    try:
        # This loads in the campaign schema
        body_data = campaign_schema().load(request.get_json())

        # This creates a new object with the required criteria
        new_campaign = Campaign(
            name=body_data.get("name"),
            genre=body_data.get("genre"),
            description=body_data.get("description"),
            game_master_id=body_data.get("game_master_id")
        )

        # This adds and commits the campaign
        db.session.add(new_campaign)
        db.session.commit()

        # This returns the new campaign
        return campaign_schema().dump(new_campaign), 201
    # This checks for conflicts between requests and conditions ie unique, null (409)
    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # This checks for breaches of UNIQUE
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409


# READ ALL CAMPAIGNS

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retreives the result as a list
# - converts the data to JSON
# - returns the data


# This defines the route for the request. It is shortened by the above blueprint.
@campaigns_bp.route("/")
def get_campaigns():
    # This statement selects all inputs from the Campaign table using the Campaign Class
    stmt = db.select(Campaign)
    # This retrieves the results as a list. Scalars will provide multiple results.
    campaigns_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = campaigns_schema.dump(campaigns_list)
    # This returns the list
    return data

# READ A SELECT CAMPAIGN

# This function finds a select campaign and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via it's id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message


# This defines the route for a GET request. It is shortened by the above blueprint.
@campaigns_bp.route("/<int:campaign_id>")
def get_campaign(campaign_id):
    # This statement selects the campaign based on the id and filters it using filter.by
    stmt = db.select(Campaign).filter_by(id=campaign_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    campaign = db.session.scalar(stmt)
    # Check if the campaign matching the idea was found
    if campaign:
        # if so, convert into a json using .dump
        data = campaign_schema.dump(campaign)
        # return the data
        return data
    else:
        # else return a 404 error message with the id
        return {"message": f"Campaign with id {campaign_id} does not exist"}, 404

# UPDATE A CAMPAIGN
# This function finds an object with the matching id and replaces the contents with the new data
# To do this, this application:
# - Finds the campaign (select), with the campaign id (filter by) and loads it (.load)
# - If it exists, overwrite the data with the new request
# - Commits and returns the data
# - Integrity checks for Non Nullable and Unique constraints

# This defines the route for the UPDATE request. It is shortened by the above blueprint.


@campaigns_bp.route("/<int:campaign_id>", methods=["PUT", "PATCH"])
def update_campaign(campaign_id):
    try:
        # This finds the campaign to be updated
        stmt = db.select(Campaign).filter_by(id=campaign_id)
        campaign = db.session.scalar(stmt)

        # This loads the data from the request
        body_data = campaign_schema.load(request.get_json(), partial=True)

        # If the campaign exists
        if campaign:
            # Update the campaign data using the data from the request body
            campaign.name = body_data.get("name") or campaign.name
            campaign.genre = body_data.get("genre") or campaign.genre
            campaign.description = body_data.get(
                "description") or campaign.description
            campaign.game_master_id = body_data.get(
                "game_master_id") or campaign.game_master_id

            # Commit the changes
            db.session.commit()

            # Return the data
            return campaign_schema.dump(campaign)

        # If the campaign doesn't exist
        else:
            # Return a 404 error message with the id
            return {"message": f"Campaign with id {campaign_id} doesn't exist"}, 404

    except IntegrityError as err:
        # This checks for breaches of NON-NULL
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}, 409
        # This checks for breaches of UNIQUE
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409

# DELETE A CAMPAIGN
# This function deletes a campaign by filtering for the id.
# To do so, the application:
# - Selects an entity (select and filter.by)
# - Retrieves the result
# - Deletes it
# - Commits the change


# This defines the route for the DELETE request. It is shortened by the above blueprint.
@campaigns_bp.route("/<int:campaign_id>", methods=["DELETE"])
def delete_campaign(campaign_id):
    # This statement selects the campaign based on the id and filters it using filter.by
    stmt = db.select(Campaign).filter_by(id=campaign_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    campaign = db.session.scalar(stmt)
    # if it exists:
    if campaign:
        # delete the campaign
        db.session.delete(campaign)
        # commit the changes
        db.session.commit()
        # Return success message
        return {"message": f"'{campaign.name}' was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 error message with the id
        return {"message": f"Campaign with id {campaign_id} does not exist"}, 404
