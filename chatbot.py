import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

from controllers import UserController
from utils import register

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

HELP_MSG = "/login       login your account.\n"
HELP_MSG += "/create    create activity. (if you are professor)\n"
HELP_MSG += "/join        join activity.\n"
HELP_MSG += "/list         list activity.\n"
HELP_MSG += "/my_activities  personal joined activities.\n"
HELP_MSG += "/help        list Available commands.\n"

PROFESSOR_LIST = [5138021525]  # Set your predefined user_id here


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! \n\n" + HELP_MSG)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    first check if user in database.
    if not:
        Sends a message with three inline buttons attached.
    else:
        Send Welcome message.
    """
    user_id = update.effective_user.id
    # search user by user_id in database:
    user = UserController.get(user_id)
    if user:
        context.bot_data["isLogin"] = True
        await update.message.reply_text("Welcome Back! " + f" {user.user_name} ({user.user_type}) \n\n")
    else:
        keyboard = [
            [
                InlineKeyboardButton("professor", callback_data="professor"),
                InlineKeyboardButton("student", callback_data="student"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please choose an option to sign up: ", reply_markup=reply_markup)


async def signUpButton(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

    user_id = update.effective_user.id
    query = update.callback_query
    option = query.data

    if option == "professor":
        if user_id in PROFESSOR_LIST:
            await query.answer()

            user_id = update.effective_user.id
            username = update.effective_user.username
            new_user = register(user_id, username, query.data)
            context.bot_data["isLogin"] = True

            await query.edit_message_text(f"You are now a {new_user.user_type}. \n" + HELP_MSG)
        else:
            await query.edit_message_text(f"You can not sign up as professor, coz you are not on professor list")

    elif option == "student":
        if user_id not in PROFESSOR_LIST:
            await query.answer()

            user_id = update.effective_user.id
            username = update.effective_user.username
            new_user = register(user_id, username, query.data)
            context.bot_data["isLogin"] = True

            await query.edit_message_text(f"You are now a {new_user.user_type}. \n" + HELP_MSG)
        else:
            await query.edit_message_text(f"You can not sign up as student, coz you are not on professor list")
