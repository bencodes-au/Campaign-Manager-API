from init import db, ma


class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    game_master_id = db.Column(db.Integer, db.ForeignKey(
        "game_master.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    genre = db.Column(db.String(100))
    description = db.Column(db.String(100))

    game_master = db.relationship("GameMaster", back_populates="campaigns")
    characters = db.relationship("Character", back_populates="campaign")
    played_games = db.relationship("PlayedGame", back_populates="campaign")
    players = db.relationship("PlayerCampaign", back_populates="campaign")


class CampaignSchema(ma.Schema):
    class Meta:
        fields = ("id", "game_master_id", "name",
                  "genre", "description")


campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
