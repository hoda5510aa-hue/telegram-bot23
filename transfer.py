from database import get_balance, change_diamonds


def transfer_diamonds(sender_id, receiver_id, amount):

    if amount <= 0:
        return {
            "success": False,
            "message": "مقدار انتقال درست نیست"
        }


    sender_balance = get_balance(sender_id)


    if sender_balance < amount:

        return {
            "success": False,
            "message": "❌ موجودی شما کافی نمی باشد"
        }



    change_diamonds(
        sender_id,
        -amount
    )


    change_diamonds(
        receiver_id,
        amount
    )


    return {
        "success": True,
        "message": "✅ انتقال موفق"
    }
