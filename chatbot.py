import logging
from telegram import Update

from telegram.ext import Application, CommandHandler, ContextTypes

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! \n\n" + HELP_MSG)