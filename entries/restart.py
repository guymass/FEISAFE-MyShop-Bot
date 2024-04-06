from lib import deco
from lib.database import db
import logging
from entries.clear_chat import clear_chat
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_callback_handler(pattern="^cb_back$")
def restart(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data

    clear_chat(update, context)