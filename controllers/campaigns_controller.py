from flask import Blueprint

from init import db
from models.campaigns import Campaign, campaigns_schema, campaign_schema

# This blueprint builds a prefix for the routing to enable shorter code blocks for the Campaign Controller.
campaign_bp = Blueprint("campaigns", __name__, url_prefix="/campaigns")

# Create a Campaign


# READ ALL CAMPAIGNS

# This function finds the requested list using an SQL Query and returns it in JSON.
# To do this, the application:
# - defines a route
# - builds a statement to select the appropriate table
# - retreives the result as a list
# - converts the data to JSON
# - returns the data


# This defines the route for the request. It is shortened by the above blueprint.
@campaign_bp.route("/")
def get_campaigns():
    # This statement selects all inputs from the Campaign Table
    stmt = db.select(Campaign)
    # This retrieves the results as a list. Scalars will provide multiple results.
    campaigns_list = db.session.scalars(stmt)
    # This converts the list into a JSON format using .dump
    data = campaigns_schema.dump(campaigns_list)
    # This returns the list
    return data

# READ A SELECT CAMPAIGN

# This function finds a select entry and returns it as JSON.
# To do this, the application:
# - defines the route for a GET request
# - selects the entity via it's id and filtering it with filter.by
# - Retrieves the result
# - if correct, converts to json and returns it
# - else returns an error message

# This defines the route for a GET request. It is shortened by the above blueprint.


@campaign_bp.route("/<int:campaign_id>")
def get_campaign(campaign_id):
    # This statement selects the entity based on the id and filters it using filter.by
    stmt = db.select(Campaign).filter_by(id=campaign_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    campaign = db.session.scalar(stmt)
    # Check if the entry matching the idea was found
    if campaign:
        # if so, convert into a json using .dump
        data = campaign_schema.dump(campaign)
        # return the data
        return data
    else:
        # return a 404 error message with the id
        return {"message": f"Campaign with id {campaign_id} does not exist"}, 404

# UPDATE A CAMPAIGN


# DELETE A CAMPAIGN
# This function deletes an entry by filtering for the id.
# To do so, the application:

# This defines the route for the DELETE request. It is shortened by the above blueprint.
@campaign_bp.route("/<int:campaign_id>", methods=["DELETE"])
def delete_campaign(campaign_id):
    # This statement selects the entity based on the id and filters it using filter.by
    stmt = db.select(Campaign).filter_by(id=campaign_id)
    # This retrieves the result. Scalar means it retrieves a single result.
    campaign = db.session.scalar(stmt)
    # if it exists:
    if campaign:
        # delete the entry
        db.session.delete(campaign)
        # commit the changes
        db.session.commit()
        # Return success message
        return {"message": f"'{campaign.name}' was deleted successfully"}
    # if it doesn't exist
    else:
        # return a 404 error message with the id
        return {"message": f"Campaign with id {campaign_id} does not exist"}, 404
