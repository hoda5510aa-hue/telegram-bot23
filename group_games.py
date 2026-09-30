import random
import time


group_games = {}


def create_game(user_id, username, amount):

    game_id = str(int(time.time() * 1000))

    group_games[game_id] = {
        "creator": user_id,
        "creator_name": username or "کاربر",
        "amount": amount,
        "player2": None,
        "player2_name": None,
        "created_at": time.time()
    }

    return game_id


def get_game(game_id):

    return group_games.get(game_id)


def join_game(game_id, user_id, username):

    game = group_games.get(game_id)

    if game is None:
        return None

    if time.time() - game["created_at"] >= 30:

        return {
            "expired": True,
            "creator": game["creator"],
            "amount": game["amount"]
        }

    if game["creator"] == user_id:
        return None

    if game["player2"] is not None:
        return None

    game["player2"] = user_id
    game["player2_name"] = username or "کاربر"

    winner = random.choice([
        game["creator"],
        user_id
    ])

    if winner == game["creator"]:

        loser = user_id
        winner_name = game["creator_name"]
        loser_name = game["player2_name"]

    else:

        loser = game["creator"]
        winner_name = game["player2_name"]
        loser_name = game["creator_name"]

    amount = game["amount"]

    del group_games[game_id]

    return {
        "expired": False,
        "winner": winner,
        "loser": loser,
        "winner_name": winner_name,
        "loser_name": loser_name,
        "reward": amount * 2,
        "lose": amount,
        "amount": amount
    }


def cancel_game(game_id, user_id):

    game = group_games.get(game_id)

    if game is None:
        return None

    if game["creator"] != user_id:
        return None

    result = {
        "creator": game["creator"],
        "creator_name": game["creator_name"],
        "amount": game["amount"]
    }

    del group_games[game_id]

    return result


def timeout_games():

    now = time.time()
    expired = []

    for game_id, game in list(group_games.items()):

        if now - game["created_at"] >= 30:

            expired.append({
                "game_id": game_id,
                "creator": game["creator"],
                "creator_name": game["creator_name"],
                "amount": game["amount"]
            })

            del group_games[game_id]

    return expired
