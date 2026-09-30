from database import change_diamonds


def admin_change(owner_id, target_id, amount, action):

    if action == "add":

        change_diamonds(
            target_id,
            amount
        )

        return {
            "success": True,
            "message": f"✅ {amount} 💎 اضافه شد"
        }


    elif action == "remove":

        change_diamonds(
            target_id,
            -amount
        )

        return {
            "success": True,
            "message": f"✅ {amount} 💎 کسر شد"
        }


    return {
        "success": False,
        "message": "دستور نامعتبر است"
    }
