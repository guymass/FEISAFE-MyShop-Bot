from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (deco, states)
from emoji import emojize
from time import sleep
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='^cb_get_post_id$')
@deco.register_state_callback(states.ORDERID, pattern='^cb_get_post_id$')
def get_post_id(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id

    cancel_keyboard = []
    cancel_keyboard +=  [[InlineKeyboardButton("ביטול", callback_data="cb_back")]]
    #cancel_keyboard +=  [[InlineKeyboardButton("הבא", callback_data="cb_get_category")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)

    context.bot.send_message(chat_id=chat_id, text="\U0000200F 👩‍🌾 💬 אנא שלחו לי את קוד המודעה לעדכון, אני ממתין...⏳", reply_markup=reply_markup_cancel, callback_data='cb_get_category')

    return states.CAT_NAME