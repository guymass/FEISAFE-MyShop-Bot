from lib import deco
from lib.database import db
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_command_handler("purge")
def purge(update, context):
    chat_id = update.effective_message.chat_id
    msg = "\U0000200F כל הרשומות נמחקו!"
    x = db.completed_orders.delete_many({})
    context.bot.send_message(chat_id, msg)

