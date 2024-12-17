from init import db, ma


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)

    characters = db.relationship("PlayerCampaign", back_populates="player")
    campaigns = db.relationship(
        "PlayerCampaign", back_populates="player", cascade="all, delete")


class PlayerSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone")


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
