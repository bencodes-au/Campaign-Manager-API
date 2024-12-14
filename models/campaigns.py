from init import db, ma

__tablename__ = "campaigns"


class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    description = db.Column(db.String(100))

# game_masters id relationship
# character_id relationship
# played_games relationship


class CampaignSchema(ma.Schema):
    class Meta:
        fields = ("campaign_id", "name", "genre", "description")


campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
