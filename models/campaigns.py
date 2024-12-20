from marshmallow import fields, validate
from init import db, ma

from models.game_masters import GameMaster


class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    game_master_id = db.Column(db.Integer, db.ForeignKey(
        "game_masters.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    genre = db.Column(db.String(100))
    description = db.Column(db.String(100))

    game_master = db.relationship("GameMaster", back_populates="campaigns")
    players = db.relationship(
        "PlayerCampaign", back_populates="campaign", cascade="all, delete")
    characters = db.relationship(
        "Character", back_populates="campaign", cascade="all, delete")
    played_games = db.relationship(
        "PlayedGame", back_populates="campaign", cascade="all, delete")


class CampaignSchema(ma.Schema):
    class Meta:
        fields = ("id", "game_master_id", "name",
                  "genre", "description")

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=1, max=100, error="This field must be between 1 and 100 characters."),
            validate.Regexp(
                r'^[A-Za-z\s\-\'&]+$',
                error="This field can only contain letters (A-Z, a-z), spaces, hyphens (-), apostrophes ('), and ampersands (&)."
            ),
        ]
    )

    genre = fields.Str(
        validate=[
            validate.Length(
                min=1, max=100, error="This field must be between 1 and 100 characters."),
            validate.Regexp(
                r'^[A-Za-z\s\-\'&]+$',
                error="This field can only contain letters (A-Z, a-z), spaces, hyphens (-), apostrophes ('), and ampersands (&)."
            ),
        ]
    )

    description = fields.Str(
        validate=[
            validate.Length(
                min=1, max=100, error="This field must be between 1 and 100 characters."),
            validate.Regexp(
                r'^[A-Za-z\s\-\'&]+$',
                error="This field can only contain letters (A-Z, a-z), spaces, hyphens (-), apostrophes ('), and ampersands (&)."
            ),
        ]
    )


campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
