from database import add_user, get_balance
from utils import format_diamonds


def start_user(user):
    add_user(
        user.id,
        user.username
    )


def balance_text(user_id):
    balance = get_balance(user_id)

    return (
        "💎 موجودی شما:\n\n"
        + format_diamonds(balance)
    )
