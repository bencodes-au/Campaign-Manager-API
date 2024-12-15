from flask import Blueprint

from init import db
from models.campaigns import Campaign, campaigns_schema, campaign_schema

campaign_bp = Blueprint("campaigns", __name__, url_prefix="/campaigns")

# Create a Campaign


# Read all Campaigns


@campaign_bp.route("/")
def get_campaigns():
    stmt = db.select(Campaign)
    campaigns_list = db.session.scalars(stmt)
    data = campaigns_schema.dump(campaigns_list)
    return data

# Read a select Campaign


@campaign_bp.route("/<int:campaign_id>")
def get_campaign(campaign_id):
    stmt = db.select(Campaign).filter_by(id=campaign_id)
    campaign = db.session.scalar(stmt)
    if campaign:
        data = campaign_schema.dump(campaign)
        return data
    else:
        return {"message": f"Campaign with id {campaign_id} does not exist"}, 404

# Update a Campaign


# Delete a Campaign
@campaign_bp.route("/<int:campaign_id>", methods=["DELETE"])
def delete_campaign(campaign_id):
    stmt = db.select(Campaign).filter_by(id=campaign_id)
    campaign = db.session.scalar(stmt)
    if campaign:
        db.session.delete(campaign)
        db.session.commit()

        return {"message": f"'{campaign.name}' was deleted successfully"}

    else:
        return {"message": f"Campaign with id {campaign_id} does not exist"}, 404
