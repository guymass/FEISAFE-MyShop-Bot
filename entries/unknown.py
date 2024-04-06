from lib import deco
from telegram.ext import Filters
import logging
from emoji import emojize
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_message_handler(Filters.command)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="\U0000200F  \U0001F505 \U0000200F סליחה אבל הפקודה הזאת אינה מוכרת לי \U0001F505 \n\nאנא כתבו את הפקודה /help בכדי לקבל רשימת הפקודות האפשריות.\n")
