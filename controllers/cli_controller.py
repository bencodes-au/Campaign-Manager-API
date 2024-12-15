from flask import Blueprint

from init import db
from models.campaigns import Campaign
from models.characters import Character
from models.game_masters import GameMaster
from models.played_games import PlayedGame
from models.players import Player

db_commands = Blueprint("db", __name__)

# Create Table Function


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables Created")

# Delete Table Function


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

# Seed Data Function


@db_commands.cli.command("seed")
def seed_tables():
    game_masters = [
        GameMaster(
            first_name="Aaron",
            last_name="Anderson",
            email="aaronanderson@icloud.com",
            phone="0400000001"
        ),
        GameMaster(
            first_name="Bob",
            last_name="Brighton",
            email="bobbrighton@gmail.com",
            phone="0400000002"
        ),
        GameMaster(
            first_name="Clyde",
            last_name="Cliff",
            email="clydecliff@hotmail.com",
            phone="0400000003"
        ),
        GameMaster(
            first_name="Declan",
            last_name="Davis",
            email="declandavis@gmail.com",
            phone="0400000004"
        ),
    ]
    db.session.add_all(game_masters)
    db.session.commit()

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
    db.session.add_all(players)
    db.session.commit()

    campaigns = [
        Campaign(
            name="Medieval Mayhem",
            genre="Fantasy",
            description="knights and dragons and magic",
            game_master_id=game_masters[0].id
        ),
        Campaign(
            name="Spooktober",
            genre="Horror",
            description="Spooky things are happening in October",
            game_master_id=game_masters[1].id
        ),
        Campaign(
            name="Last Draw",
            genre="Western",
            description="rooty tooty point and shooty",
            game_master_id=game_masters[2].id
        ),
        Campaign(
            name="Eureka City",
            genre="Heroes",
            description="caped crusaders save the day",
            game_master_id=game_masters[3].id
        ),
    ]
    db.session.add_all(campaigns)
    db.session.commit()

    characters = [
        Character(
            name="Seraphina Nightshade",
            backstory="knight turned assassin",
            skills="Retribution",
            campaign_id=campaigns[0].id,
            player_id=players[0].id
        ),
        Character(
            name="Elowen Throne",
            backstory="Healer from the forest",
            skills="Grace",
            campaign_id=campaigns[0].id,
            player_id=players[1].id
        ),
        Character(
            name="Kealen Stormrider",
            backstory="Cleric of the storm god",
            skills="Storm",
            campaign_id=campaigns[0].id,
            player_id=players[2].id
        ),
        Character(
            name="Maggie Hollaway",
            backstory="Nurse suffered tragic accident",
            skills="Healing",
            campaign_id=campaigns[1].id,
            player_id=players[3].id
        ),
        Character(
            name="Victor Graves",
            backstory="Researcher of eternal life",
            skills="Occult",
            campaign_id=campaigns[1].id,
            player_id=players[4].id
        ),
        Character(
            name="Evelyn Blackwood",
            backstory="Searching for missing daughter",
            skills="Streetwise",
            campaign_id=campaigns[1].id,
            player_id=players[5].id
        ),
        Character(
            name="Cass",
            backstory="Orphaned Cattle Hand",
            skills="Intuition",
            campaign_id=campaigns[2].id,
            player_id=players[6].id
        ),
        Character(
            name="Boone",
            backstory="Slick Talking Bounty Hunter",
            skills="Dexterity",
            campaign_id=campaigns[2].id,
            player_id=players[7].id
        ),
        Character(
            name="Jonah",
            backstory="Soldier turned Drifter",
            skills="Whiskey",
            campaign_id=campaigns[2].id,
            player_id=players[8].id
        ),
        Character(
            name="Lyra",
            backstory="Holder of the Starwind",
            skills="Cosmic",
            campaign_id=campaigns[3].id,
            player_id=players[9].id
        ),
        Character(
            name="Tobias",
            backstory="Struck by lightning",
            skills="Zap",
            campaign_id=campaigns[3].id,
            player_id=players[10].id
        ),
        Character(
            name="Aurora",
            backstory="Werewolf in hiding",
            skills="Hunter",
            campaign_id=campaigns[3].id,
            player_id=players[11].id
        )
    ]
    db.session.add_all(characters)
    db.session.commit()

    played_games = [
        PlayedGame(
            synopsis="There was magic",
            campaign_id=campaigns[0].id
        ),
        PlayedGame(
            synopsis="There was dragons",
            campaign_id=campaigns[0].id
        ),
        PlayedGame(
            synopsis="There was knights",
            campaign_id=campaigns[0].id
        ),
        PlayedGame(
            synopsis="The murder mystery",
            campaign_id=campaigns[1].id
        ),
        PlayedGame(
            synopsis="Ghosts haunted the manor",
            campaign_id=campaigns[1].id
        ),
        PlayedGame(
            synopsis="There was a dang shootout",
            campaign_id=campaigns[2].id
        ),
        PlayedGame(
            synopsis="We saved the city from the villain",
            campaign_id=campaigns[3].id
        ),
        PlayedGame(
            synopsis="There's a monster on the loose",
            campaign_id=campaigns[3].id
        )
    ]
    db.session.add_all(played_games)
    db.session.commit()

    print("Data seeded successfully!")
