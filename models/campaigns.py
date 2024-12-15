from init import db, ma

__tablename__ = "campaigns"


class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    # game master id
    game_master_id = db.Column(db.Integer, db.ForeignKey(
        "game_master.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    description = db.Column(db.String(100))

    # game_masters id relationship
    game_master = db.relationship("Game_Master", back_populates="campaigns")
    # character_id relationship
    character = db.relationship("Character", back_populates="campaigns")
    # played_games relationship
    played_game = db.relationship("Played Game", back_populates="campaigns")


class CampaignSchema(ma.Schema):
    class Meta:
        fields = ("campaign_id", "game_master_id" "name",
                  "genre", "description")


campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
