from init import db, ma

__tablename__ = "players"


class Players(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    # character_id relationship
    character = db.relationship("Character", back_populates="players")


class Player_Schema(ma.Schema):
    class Meta:
        fields = ("player_id", "first_name", "last_name" "email", "phone")


player_schema = Player_Schema()
player_schema = Player_Schema(many=True)
