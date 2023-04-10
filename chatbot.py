import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes,CallbackQueryHandler,ConversationHandler,MessageHandler,filters

from controllers import UserController,ActivityController
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

A_DATE, A_TIME, A_PLACE, A_EVENT = range(4)

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


async def create_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if context.bot_data["isLogin"]:
        if update.effective_user.id in PROFESSOR_LIST:
            await update.message.reply_text("Please enter the date (DD-MM-YYYY): ")#\nor you can click here to exit /cancel
            return A_DATE
        else:
            await update.message.reply_text("Sorry, you are not professor")
            return -1
    else:
        await update.message.reply_text("Sorry, you need to login first")

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date = update.message.text
    context.user_data["date"] = date
    await update.message.reply_text("Please enter the time (HH:MM): \nor you can click here to exit /cancel")
    return A_TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    time = update.message.text
    context.user_data["time"] = time
    await update.message.reply_text("Please enter the place: \nor you can click here to exit /cancel")
    return A_PLACE

async def get_place(update: Update, context:  ContextTypes.DEFAULT_TYPE) -> int:
    place = update.message.text
    context.user_data["place"] = place
    await update.message.reply_text("Please enter the event: \nor you can click here to exit /cancel")
    return A_EVENT

async def get_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event = update.message.text
    context.user_data["event"] = event

    new_activity = ActivityController.create(
        context.user_data["professor_id"],
        context.user_data["date"],
        context.user_data["time"],
        context.user_data["place"],
        context.user_data["event"]
    )

    await update.message.reply_text(f"New activity created with ID: {new_activity.activity_id}")
    return ConversationHandler.END


async def cancel_create_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Activity creation canceled.")
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""

    context_data = {
        "isLogin": False
    }

    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5613084877:AAEl8qbzCirqOhGtL7F3wTEFHrxBxh9wG-w").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))

    application.add_handler(CallbackQueryHandler(signUpButton))

    create_conversation = ConversationHandler(
        entry_points=[CommandHandler('create', create_activity)],
        states={
            A_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            A_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
            A_PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_place)],
            A_EVENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_event)],
        },
        fallbacks=[CommandHandler("cancel", cancel_create_activity)],
    )

    application.add_handler(create_conversation)
    application.bot_data.update(context_data)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()