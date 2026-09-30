import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, OWNER_ID

from database import (
    setup,
    add_user,
    get_balance,
    change_diamonds,
    user_exists
)

from keyboards import main_menu, games_menu

from games import play_game

from group_games import (
    create_game,
    get_game,
    join_game,
    cancel_game,
    timeout_games
)


# -----------------------------
# بازی‌های خصوصی
# -----------------------------

user_games = {}


# -----------------------------
# پیام‌های بازی گروهی
# -----------------------------

group_messages = {}


# -----------------------------
# موجودی
# -----------------------------

def balance(user_id):

    if user_id == OWNER_ID:
        return "∞ 💎"

    return f"{get_balance(user_id):,} 💎"


# -----------------------------
# کم کردن الماس
# مالک نامحدود است
# -----------------------------

def remove_diamonds(user_id, amount):

    if user_id == OWNER_ID:
        return True

    if get_balance(user_id) < amount:
        return False

    change_diamonds(
        user_id,
        -amount
    )

    return True


# -----------------------------
# اضافه کردن الماس
# -----------------------------

def add_diamonds(user_id, amount):

    if user_id == OWNER_ID:
        return

    change_diamonds(
        user_id,
        amount
    )


# -----------------------------
# /start
# -----------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    first_time = not user_exists(user.id)

    add_user(
        user.id,
        user.username
    )

    if first_time:

        text = (
            "👋 خوش آمدید\n\n"
            "🎁 هدیه ورود شما:\n"
            "💎 1000 الماس رایگان\n\n"
            "از منوی زیر استفاده کنید."
        )

    else:

        text = (
            "👋 خوش آمدید دوباره\n\n"
            "از منوی زیر استفاده کنید."
        )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


# -----------------------------
# پیام‌های متنی
# -----------------------------

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user
    text = update.message.text

    add_user(
        user.id,
        user.username
    )


    # =============================
    # موجودی
    # =============================

    if text in ["💎 موجودی", "موجودی"]:

        await update.message.reply_text(
            "💎 موجودی شما:\n\n"
            f"{balance(user.id)}"
        )

        return


    # =============================
    # بازی‌های خصوصی
    # =============================

    if text == "🎮 بازی‌ها":

        await update.message.reply_text(
            "🎮 یک بازی انتخاب کنید:",
            reply_markup=games_menu()
        )

        return


    if text == "🔙 برگشت":

        await update.message.reply_text(
            "منوی اصلی:",
            reply_markup=main_menu()
        )

        return


    # =============================
    # انتخاب بازی خصوصی
    # =============================

    private_games = [
        "💣 ماین",
        "🎰 اسلات",
        "🚀 موشک",
        "🎲 تاس",
        "🃏 کارت",
        "🪙 شیر یا خط",
        "🎯 هدف",
        "🎡 گردونه",
        "🔢 عدد",
        "🍀 شانس"
    ]


    if text in private_games:

        user_games[user.id] = text

        await update.message.reply_text(
            f"{text}\n\n"
            "💎 مقدار الماس را وارد کنید:\n"
            "حداقل ۲۰ الماس"
        )

        return


    # =============================
    # مبلغ بازی خصوصی
    # =============================

    if user.id in user_games:

        try:

            amount = int(text.strip())

        except ValueError:

            await update.message.reply_text(
                "❌ فقط عدد وارد کنید."
            )

            return


        if amount < 20:

            await update.message.reply_text(
                "❌ حداقل مبلغ بازی ۲۰ 💎 است."
            )

            return


        if not remove_diamonds(
            user.id,
            amount
        ):

            await update.message.reply_text(
                "❌ موجودی شما کافی نیست."
            )

            return


        game_name = user_games.pop(
            user.id
        )


        result = play_game(
            game_name,
            amount
        )


        if result is None:

            add_diamonds(
                user.id,
                amount
            )

            await update.message.reply_text(
                "❌ خطا در اجرای بازی."
            )

            return


        if result["win"]:

            add_diamonds(
                user.id,
                result["reward"]
            )

            result_text = (
                "🎉 شما بردید!\n"
                f"💎 جایزه: +{result['reward']}"
            )

        else:

            result_text = (
                "💥 شما باختید!\n"
                f"💎 کسر شده: -{amount}"
            )


        await update.message.reply_text(
            f"{result['game']}\n\n"
            f"{result['display']}\n\n"
            f"{result_text}\n\n"
            f"💎 موجودی جدید: {balance(user.id)}",
            reply_markup=main_menu()
        )

        return


    # =============================
    # بازی گروهی
    # فقط گروه
    # =============================

    if (
        update.effective_chat.type in [
            "group",
            "supergroup"
        ]
        and text.startswith("بازی")
    ):

        try:

            amount = int(
                text.replace(
                    "بازی",
                    "",
                    1
                ).strip()
            )

        except ValueError:

            await update.message.reply_text(
                "❌ فرمت درست:\n\n"
                "بازی 20"
            )

            return


        if amount < 20:

            await update.message.reply_text(
                "❌ حداقل مبلغ بازی ۲۰ 💎 است."
            )

            return


        if not remove_diamonds(
            user.id,
            amount
        ):

            await update.message.reply_text(
                "❌ موجودی شما کافی نیست."
            )

            return


        game_id = create_game(
            user.id,
            user.username,
            amount
        )


        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎮 پیوستن",
                    callback_data=f"join:{game_id}"
                ),
                InlineKeyboardButton(
                    "❌ لغو",
                    callback_data=f"cancel:{game_id}"
                )
            ]
        ])


        message = await update.message.reply_text(
            "🎮 بازی جدید\n\n"
            f"👤 سازنده: {user.first_name}\n"
            f"💎 شرط: {amount}\n\n"
            "⏳ زمان ورود: ۳۰ ثانیه",
            reply_markup=keyboard
        )


        group_messages[game_id] = (
            update.effective_chat.id,
            message.message_id
        )

        return


    # =============================
    # انتقال
    # =============================

    if text.startswith("انتقال"):

        if not update.message.reply_to_message:

            await update.message.reply_text(
                "❌ باید روی پیام شخص موردنظر ریپلای کنید."
            )

            return


        try:

            amount = int(
                text.replace(
                    "انتقال",
                    "",
                    1
                ).strip()
            )

        except ValueError:

            await update.message.reply_text(
                "❌ فرمت درست:\n"
                "انتقال 10"
            )

            return


        if amount <= 0:

            await update.message.reply_text(
                "❌ مبلغ باید بیشتر از صفر باشد."
            )

            return


        receiver = (
            update.message
            .reply_to_message
            .from_user
        )


        if receiver.id == user.id:

            await update.message.reply_text(
                "❌ نمی‌توانید به خودتان انتقال دهید."
            )

            return


        if not remove_diamonds(
            user.id,
            amount
        ):

            await update.message.reply_text(
                "❌ موجودی شما کافی نمی باشد."
            )

            return


        add_user(
            receiver.id,
            receiver.username
        )

        add_diamonds(
            receiver.id,
            amount
        )


        await update.message.reply_text(
            "✅ انتقال موفق\n\n"
            f"💎 مقدار: {amount}\n"
            f"👤 گیرنده: {receiver.first_name}\n\n"
            f"💎 موجودی شما: {balance(user.id)}"
        )

        return


    # =============================
    # افزودن توسط مالک
    # =============================

    if (
        user.id == OWNER_ID
        and text.startswith("افزودن")
    ):

        if not update.message.reply_to_message:

            await update.message.reply_text(
                "❌ باید روی پیام کاربر ریپلای کنید."
            )

            return


        try:

            amount = int(
                text.replace(
                    "افزودن",
                    "",
                    1
                ).strip()
            )

        except ValueError:

            await update.message.reply_text(
                "❌ فرمت درست:\n"
                "افزودن 600"
            )

            return


        target = (
            update.message
            .reply_to_message
            .from_user
        )


        add_user(
            target.id,
            target.username
        )

        add_diamonds(
            target.id,
            amount
        )


        await update.message.reply_text(
            "✅ انجام شد\n\n"
            f"➕ {amount} 💎\n"
            f"👤 {target.first_name}\n"
            f"💎 موجودی جدید: {balance(target.id)}"
        )

        return


    # =============================
    # کسر توسط مالک
    # =============================

    if (
        user.id == OWNER_ID
        and text.startswith("کسر")
    ):

        if not update.message.reply_to_message:

            await update.message.reply_text(
                "❌ باید روی پیام کاربر ریپلای کنید."
            )

            return


        try:

            amount = int(
                text.replace(
                    "کسر",
                    "",
                    1
                ).strip()
            )

        except ValueError:

            await update.message.reply_text(
                "❌ فرمت درست:\n"
                "کسر 1000"
            )

            return


        if amount <= 0:

            await update.message.reply_text(
                "❌ مبلغ نامعتبر است."
            )

            return


        target = (
            update.message
            .reply_to_message
            .from_user
        )


        add_user(
            target.id,
            target.username
        )


        if target.id != OWNER_ID:

            current = get_balance(
                target.id
            )

            amount = min(
                amount,
                current
            )

            change_diamonds(
                target.id,
                -amount
            )


        await update.message.reply_text(
            "✅ انجام شد\n\n"
            f"➖ {amount} 💎\n"
            f"👤 {target.first_name}\n"
            f"💎 موجودی جدید: {balance(target.id)}"
        )

        return


# =============================
# دکمه‌های بازی گروهی
# =============================

async def group_game_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    data = query.data


    # =============================
    # پیوستن
    # =============================

    if data.startswith("join:"):

        game_id = data.split(
            ":",
            1
        )[1]


        game = get_game(
            game_id
        )


        if game is None:

            await query.answer(
                "❌ این بازی دیگر وجود ندارد.",
                show_alert=True
            )

            return


        if user.id == game["creator"]:

            await query.answer(
                "❌ سازنده نمی‌تواند به بازی خودش بپیوندد.",
                show_alert=True
            )

            return


        amount = game["amount"]


        if not remove_diamonds(
            user.id,
            amount
        ):

            await query.answer(
                "❌ موجودی شما کافی نیست.",
                show_alert=True
            )

            return


        result = join_game(
            game_id,
            user.id,
            user.username
        )


        if result is None:

            add_diamonds(
                user.id,
                amount
            )

            await query.answer(
                "❌ این بازی دیگر قابل ورود نیست.",
                show_alert=True
            )

            return


        if result.get("expired"):

            add_diamonds(
                user.id,
                amount
            )

            add_diamonds(
                result["creator"],
                result["amount"]
            )

            await query.edit_message_text(
                "⌛ زمان بازی تمام شده بود.\n\n"
                f"💎 {result['amount']} الماس به سازنده برگشت."
            )

            return


        # پرداخت جایزه برنده
        add_diamonds(
            result["winner"],
            result["reward"]
        )


        await query.edit_message_text(
            "🎲 بازی تمام شد\n\n"
            f"🏆 برنده: {result['winner_name']}\n"
            f"💎 برنده: +{result['reward']}\n\n"
            f"💥 بازنده: {result['loser_name']}\n"
            f"💎 بازنده: -{result['lose']}"
        )

        return


    # =============================
    # لغو
    # =============================

    if data.startswith("cancel:"):

        game_id = data.split(
            ":",
            1
        )[1]


        result = cancel_game(
            game_id,
            user.id
        )


        if result is None:

            await query.answer(
                "❌ فقط سازنده می‌تواند بازی را لغو کند.",
                show_alert=True
            )

            return


        add_diamonds(
            result["creator"],
            result["amount"]
        )


        group_messages.pop(
            game_id,
            None
        )


        await query.edit_message_text(
            "❌ بازی لغو شد.\n\n"
            f"💎 {result['amount']} الماس به سازنده برگشت."
        )

        return


# =============================
# تایمر ۳۰ ثانیه‌ای
# =============================

async def timeout_loop(
    application
):

    while True:

        await asyncio.sleep(1)

        expired = timeout_games()


        for game in expired:

            add_diamonds(
                game["creator"],
                game["amount"]
            )


            message_info = group_messages.pop(
                game["game_id"],
                None
            )


            if message_info:

                chat_id, message_id = message_info

                try:

                    await application.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=(
                            "⌛ زمان بازی تمام شد.\n\n"
                            f"💎 {game['amount']} الماس "
                            "به سازنده برگشت."
                        )
                    )

                except Exception:
                    pass


# =============================
# شروع ربات
# =============================

async def post_init(
    application
):

    application.create_task(
        timeout_loop(application)
    )


def main():

    setup()


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            group_game_callback
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            text_handler
        )
    )


    print("Bot Started")


    app.run_polling()


if __name__ == "__main__":
    main()
