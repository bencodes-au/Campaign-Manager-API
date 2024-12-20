from init import db, ma

from marshmallow import fields, validate


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    campaigns = db.relationship(
        "PlayerCampaign", back_populates="player", cascade="all, delete")

    characters = db.relationship("Character", back_populates="player")


class PlayerSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone")

    first_name = fields.Str(
        required=True,
        validate=validate.Length(
            min=1, max=100, error="First name must be between 1 and 100 characters.")
    )
    last_name = fields.Str(
        required=True,
        validate=validate.Length(
            min=1, max=100, error="Last name must be between 1 and 100 characters.")
    )
    email = fields.Email(
        required=True,
        validate=validate.Email(error="Invalid email address.")
    )

    phone = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\+?1?\d{9,15}$',
            error="Invalid phone number."
        )
    )


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
