from init import db, ma


class PlayedGame(db.Model):
    __tablename__ = "played_games"

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        "campaigns.id"), nullable=False)
    synopsis = db.Column(db.String(500))

    campaign = db.relationship("Campaign", back_populates="played_games")


class PlayedGameSchema(ma.Schema):
    class Meta:
        fields = ("id", "campaign_id", "synopsis")


played_game_schema = PlayedGameSchema()
played_games_schema = PlayedGameSchema(many=True)
