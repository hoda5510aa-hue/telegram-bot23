import random


GAMES = {
    "💣 ماین": "mine",
    "🎰 اسلات": "slot",
    "🚀 موشک": "rocket",
    "🎲 تاس": "dice",
    "🃏 کارت": "card",
    "🪙 شیر یا خط": "coin",
    "🎯 هدف": "target",
    "🎡 گردونه": "wheel",
    "🔢 عدد": "number",
    "🍀 شانس": "luck"
}


def play_game(game_name, amount):
    """
    اجرای یکی از ۱۰ بازی.
    مبلغ ورودی قبلاً از موجودی کاربر کم می‌شود.
    reward مبلغی است که در صورت برد به کاربر برمی‌گردد.
    """

    game_id = GAMES.get(game_name)

    if game_id is None:
        return None


    # -------------------------
    # 💣 ماین
    # -------------------------

    if game_id == "mine":

        cells = ["💎", "💎", "💣"]
        random.shuffle(cells)

        if "💣" not in cells[:1]:
            win = True
        else:
            win = False

        display = " | ".join(cells)

        multiplier = 3


    # -------------------------
    # 🎰 اسلات
    # -------------------------

    elif game_id == "slot":

        symbols = ["🍒", "🍋", "🍇", "⭐", "💎"]

        result = [
            random.choice(symbols),
            random.choice(symbols),
            random.choice(symbols)
        ]

        display = " | ".join(result)

        if result[0] == result[1] == result[2]:
            win = True
            multiplier = 3

        elif result[0] == result[1] or result[1] == result[2]:
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🚀 موشک
    # -------------------------

    elif game_id == "rocket":

        crash = random.randint(1, 100)

        if crash >= 45:
            win = True
            multiplier = random.choice([2, 3])
            display = "🚀🚀🚀 موشک پرواز کرد!"
        else:
            win = False
            multiplier = 0
            display = "🚀💥 موشک منفجر شد!"


    # -------------------------
    # 🎲 تاس
    # -------------------------

    elif game_id == "dice":

        player = random.randint(1, 6)
        bot = random.randint(1, 6)

        display = (
            f"🎲 عدد شما: {player}\n"
            f"🎲 عدد رقیب: {bot}"
        )

        if player > bot:
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🃏 کارت
    # -------------------------

    elif game_id == "card":

        cards = ["A", "K", "Q", "J", "10", "9", "8"]

        player = random.choice(cards)
        bot = random.choice(cards)

        display = (
            f"🃏 کارت شما: {player}\n"
            f"🃏 کارت رقیب: {bot}"
        )

        values = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 11,
            "10": 10,
            "9": 9,
            "8": 8
        }

        if values[player] > values[bot]:
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🪙 شیر یا خط
    # -------------------------

    elif game_id == "coin":

        result = random.choice(
            ["🦁 شیر", "🪙 خط"]
        )

        display = f"نتیجه: {result}"

        # انتخاب کاربر در نسخه bot.py انجام می‌شود.
        # اینجا نتیجه تصادفی است.
        if random.choice([True, False]):
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🎯 هدف
    # -------------------------

    elif game_id == "target":

        number = random.randint(1, 10)

        display = f"🎯 عدد هدف: {number}"

        if number >= 7:
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🎡 گردونه
    # -------------------------

    elif game_id == "wheel":

        result = random.randint(1, 10)

        display = f"🎡 گردونه روی {result} ایستاد!"

        if result in [7, 8, 9]:
            win = True
            multiplier = 2

        elif result == 10:
            win = True
            multiplier = 3

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🔢 عدد
    # -------------------------

    elif game_id == "number":

        number = random.randint(1, 5)

        display = f"🔢 عدد انتخاب‌شده: {number}"

        if number == 5:
            win = True
            multiplier = 3

        elif number >= 3:
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    # -------------------------
    # 🍀 شانس
    # -------------------------

    elif game_id == "luck":

        luck = random.randint(1, 100)

        display = f"🍀 عدد شانس شما: {luck}"

        if luck >= 70:
            win = True
            multiplier = 3

        elif luck >= 45:
            win = True
            multiplier = 2

        else:
            win = False
            multiplier = 0


    else:

        return None


    if win:

        reward = amount * multiplier

    else:

        reward = 0


    return {
        "game": game_name,
        "display": display,
        "win": win,
        "amount": amount,
        "multiplier": multiplier,
        "reward": reward
    }
