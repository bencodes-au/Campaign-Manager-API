from flask import Blueprint

from init import db
from models.campaigns import Campaign
from models.characters import Character
from models.game_masters import Game_Master
from models.played_games import Played_Game
from models.players import Player


db_commands = Blueprint("db", __name__)

# Create Table Function (CRUD)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables Created")


# Delete Table Function (CRUD)
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():

    #     students = [
    #         Student(
    #             name="Student 1",
    #             email="student1@email.com",
    #             address="Sydney"
    #         ),
    #         )
    #     ]
    #     db.session.add_all(campaigns)

    campaigns = [
        Campaign(
            # GM1
            name="Medieval Mayhem",
            genre="Fantasy",
            description="knights and dragons and magic"
        ),
        Campaign(
            # GM2
            name="Spooktober",
            genre="Horror",
            description="Spooky things are happening in October"
        ),
        Campaign(
            # GM3
            name="Last Draw",
            genre="Western",
            description="rooty tooty point and shooty"
        ),
        Campaign(
            # GM4
            name="Eureka City",
            genre="Heroes",
            description="caped crusaders save the day"
        )
    ]

    db.session.add_all(campaigns)

    characters = [
        Character(
            # CA1
            # CH1
            name="Seraphina Nightshade",
            backstory="knight turned assassin",
            skills="Retribution"
        ),
        Character(
            # CA1
            # CH2
            name="Elowen Throne",
            backstory="Healer from the forest",
            skills="Grace"
        ),
        Character(
            # CA1
            # CH3
            name="Kealen Stormrider",
            backstory="Cleric of the storm god",
            skills="Storm"
        ),
        Character(
            # CA2
            # CH4
            name="Maggie Hollaway",
            backstory="Nurse sufferred tragic accident",
            skills="Healing"
        ),
        Character(
            # CA2
            # CH5
            name="Victor Graves",
            backstory="Researcher of eternal life",
            skills="Occult"
        ),
        Character(
            # CA2
            # CH6
            name="Evelyn Blackwood",
            backstory="Searching for missing daughter",
            skills="Streetwise"
        ),
        Character(
            # CA3
            # CH7
            name="Cass",
            backstory="Orphaned Cattle Hand",
            skills="Intuition"
        ),
        Character(
            # CA3
            # CH8
            name="Boone",
            backstory="Slick Talking Bounty Hunter",
            skills="Dexterity"
        ),
        Character(
            # CA3
            # CH9
            name="Jonah",
            backstory="Soldier turned Drifter",
            skills="Whiskey"
        ),
        Character(
            # CA4
            # CH10
            name="Lyra",
            backstory="Holder of the Starwind",
            skills="Cosmic"
        ),
        Character(
            # CA4
            # CH11
            name="Tobias",
            backstory="struck by lightning",
            skills="Zap"
        ),
        Character(
            # CA4
            # CH12
            name="Aurora",
            backstory="Werewolf in hiding",
            skills="Hunter"
        )

    ]
    db.session.add_all(characters)

    game_masters = [
        Game_Master(
            first_name="Aaron",
            last_name="Anderson",
            email="aaronanderson@icloud.com",
            phone="0400000001"
        ),
        Game_Master(
            first_name="Bob",
            last_name="Brighton",
            email="bobbrighton@gmail.com",
            phone="0400000002"
        ),
        Game_Master(
            first_name="Clyde",
            last_name="Cliff",
            email="clydecliff@hotmail.com",
            phone="0400000003"
        ),
        Game_Master(
            first_name="Declan",
            last_name="Davis",
            email="declandavis@gmail.com",
            phone="0400000004"
        ),
    ]
    db.session.add_all(game_masters)

    played_games = [
        Played_Game(
            # GM1
            synopsis="there was magic"
        ),
        Played_Game(
            # GM1
            synopsis="there was dragons"
        ),
        Played_Game(
            # GM1
            synopsis="there was knights"
        ),
        Played_Game(
            # GM2
            synopsis="the murder mystery"
        ),
        Played_Game(
            # GM2
            synopsis="ghosts haunted the manor"
        ),
        Played_Game(
            # GM3
            synopsis="there was a dang shootout"
        ),
        Played_Game(
            # GM4
            synopsis="we saved the city from the villian"
        ),
        Played_Game(
            # GM4
            synopsis="there's a monster on the loose"
        ),
    ]

    players = [
        Player(
            first_name="Earvin",
            last_name="Evans",
            email="earvinevans@icloud.com",
            phone="0400000005"
        ),
        Player(
            first_name="Fred",
            last_name="Farley",
            email="fredfarley@gmail.com",
            phone="0400000006"
        ),
        Player(
            first_name="Gerald",
            last_name="Green",
            email="geraldgreen@hotmail.com",
            phone="0400000007"
        ),
        Player(
            first_name="Hugh",
            last_name="Humphrey",
            email="hughhumphrey@yahoo.com",
            phone="0400000008"
        ),
        Player(
            first_name="Ivy",
            last_name="Irwin",
            email="ivyirwin@icloud.com",
            phone="0400000009"
        ),
        Player(
            first_name="James",
            last_name="Johnson",
            email="jamesjohnson@gmail.com",
            phone="0400000010"
        ),
        Player(
            first_name="Kylie",
            last_name="King",
            email="kylieking@yahoo.com",
            phone="0400000011"
        ),
        Player(
            first_name="Lily",
            last_name="Lewis",
            email="lilylewis@outlook.com",
            phone="0400000012"
        ),
        Player(
            first_name="Mark",
            last_name="Miller",
            email="markmiller@outlook.com",
            phone="0400000013"
        ),
        Player(
            first_name="Nora",
            last_name="Nelson",
            email="noranelson@icloud.com",
            phone="0400000014"
        ),
        Player(
            first_name="Oscar",
            last_name="Owens",
            email="oscarowens@gmail.com",
            phone="0400000015"
        ),
        Player(
            first_name="Peter",
            last_name="Parker",
            email="peterparker@icloud.com",
            phone="0400000016"
        ),
    ]
    db.session.add_all(game_masters)

    db.session.commit()

    print("Tables seeded")
