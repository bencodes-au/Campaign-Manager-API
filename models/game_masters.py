from init import db, ma
from marshmallow import fields, validate


class GameMaster(db.Model):
    __tablename__ = "game_masters"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    campaigns = db.relationship("Campaign", back_populates="game_master")


class GameMasterSchema(ma.Schema):
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


game_master_schema = GameMasterSchema()

game_masters_schema = GameMasterSchema(many=True)
