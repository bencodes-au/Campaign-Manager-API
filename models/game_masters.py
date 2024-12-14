from init import db, ma

__tablename__ = "game_masters"


class Game_Master(db.Model):
    game_master_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

# campaign_id relationship


class Game_Master_Schema(ma.Schema):
    class Meta:
        fields = ("game_master_id", "first_name", "last_name" "email", "phone")


game_master_schema = Game_Master_Schema()
game_master_schema = Game_Master_Schema(many=True)
