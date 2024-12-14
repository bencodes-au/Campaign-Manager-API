from init import db, ma

__tablename__ = "played_games"


class Played_Game(db.Model):
    played_games_id = db.Column(db.Integer, primary_key=True)
    synopsis = db.Column(db.String(500))

# campaign_id relationship


class Played_Game_Schema(ma.Schema):
    class Meta:
        fields = ("games_played", "synopsis")


Played_Games_schema = Played_Game_Schema()
Played_Games_schema = Played_Game_Schema(many=True)
