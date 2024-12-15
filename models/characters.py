from init import db, ma

__tablename__ = "characters"


class Character(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    # campaign id
    # player id
    name = db.Column(db.String(100), nullable=False)
    backstory = db.Column(db.String(100))
    skills = db.Column(db.String(100))

    # campaign_id relationship
    campaign = db.relationship("Campaign", back_populates="characters")

    # player_id relationship
    player = db.relationship("Player", back_populates="characters")


class CharacterSchema(ma.Schema):
    class Meta:
        fields = ("character_id", "campaign_id",
                  "player_id", "name", "backstory", "skills")


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)
