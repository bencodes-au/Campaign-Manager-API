from init import db, ma

__tablename__ = "characters"


class Character(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    backstory = db.Column(db.String(100))
    skills = db.Column(db.String(100))

# campaign_id relationship
# player_id relationship


class CharacterSchema(ma.Schema):
    class Meta:
        fields = ("character_id", "name", "backstory", "skills")


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)
