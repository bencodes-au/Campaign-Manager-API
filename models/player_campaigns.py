from init import db, ma


class PlayerCampaign(db.Model):
    __tablename__ = "player_campaigns"

    # This prevents players being in the same campaign multiple times
    __table_args__ = (
        db.UniqueConstraint("player_id", "campaign_id",
                            name="unique_player_campaign"),
    )

    player_id = db.Column(db.Integer, db.ForeignKey(
        "players.id"), primary_key=True, nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        "campaigns.id"), primary_key=True, nullable=False)

    player = db.relationship("Player", back_populates="campaigns")
    campaign = db.relationship("Campaign", back_populates="players")


class PlayerCampaignSchema(ma.Schema):
    class Meta:
        fields = ("player_id", "campaign_id")


player_campaign_schema = PlayerCampaignSchema()
player_campaigns_schema = PlayerCampaignSchema(many=True)
