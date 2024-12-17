from init import db, ma


class GameMaster(db.Model):
    __tablename__ = "game_masters"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)

    campaigns = db.relationship("Campaign", back_populates="game_master")


class GameMasterSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone")


game_master_schema = GameMasterSchema()

game_masters_schema = GameMasterSchema(many=True)
