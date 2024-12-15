from init import db, ma


class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        "campaigns.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey(
        "player.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    backstory = db.Column(db.String(100))
    skills = db.Column(db.String(100))

    campaign = db.relationship("Campaign", back_populates="characters")
    player = db.relationship("Player", back_populates="characters")


class CharacterSchema(ma.Schema):
    class Meta:
        fields = ("id", "campaign_id", "player_id",
                  "name", "backstory", "skills")


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)
