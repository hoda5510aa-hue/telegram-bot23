from telegram import ReplyKeyboardMarkup


def main_menu():

    keyboard = [
        [
            "💎 موجودی",
            "🎮 بازی‌ها"
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )



def games_menu():

    keyboard = [

        [
            "💣 ماین",
            "🎰 اسلات"
        ],

        [
            "🚀 موشک",
            "🎲 تاس"
        ],

        [
            "🃏 کارت",
            "🪙 شیر یا خط"
        ],

        [
            "🎯 هدف",
            "🎡 گردونه"
        ],

        [
            "🔢 عدد",
            "🍀 شانس"
        ],

        [
            "🔙 برگشت"
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
