from emoji import emojize
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, CallbackQueryHandler)
from lib import (deco, states)
from lib.database import db
import logging
from entries.mainmenu import mainmenu

logger = logging.getLogger(__name__)


@deco.run_async
@deco.global_callback_handler(pattern="^cb_(date[1-3])$")
def workshop(update, context):
    query = update.callback_query
    data = query.data
    user_id = query.message.from_user.id
    chat_id = update.effective_chat.id

    if data == "cb_date1":
        query.edit_message_text("\U00002757 אין כרגע סדנאות פתוחות בתאריך זה! {}\n".format(data))
    elif data == "cb_date2":
        query.edit_message_text("\U00002757 אין כרגע סדנאות פתוחות בתאריך זה! {}\n".format(data))
    elif data == "cb_date3":
        query.edit_message_text("\U00002757 אין כרגע סדנאות פתוחות בתאריך זה! {}\n".format(data))
    mainmenu(update, context)