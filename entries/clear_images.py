from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_command_handler("clear")
def clear_images(update, context):
    chat_id = update.effective_message.chat_id
    msg = "\U0000200F כל התמונות נמחקו, אנא עדכנו תמונות חדשות על ידי העלאה לצאט."
    x = db.images.delete_many({})
    x = db.videos.delete_many({})
    context.bot.send_message(chat_id, msg)
