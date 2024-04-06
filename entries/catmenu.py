from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_callback_handler(pattern="cb_search")
def catmenu(update, context):
    query = update.callback_query
    #data = query.data
    chat_id = update.effective_chat.id
    buttons = []
    menu_count = db.buttons.count()
    reply_text = "תפריט לחיפוש קטגוריות:\n"
    for b in db.buttons.find({}):
        button_name = b['ButtonName']
        button_cb = b['ButtonCb']

        #btn_name = emojize(" \U0001f31f " + button_name)

        buttons += [[InlineKeyboardButton(str(button_name), callback_data=str(button_cb))]]

    buttons += [[InlineKeyboardButton(str("חזרה"), callback_data="cb_back")]]
    menu_buttons = list(buttons)
    main_keyboard = InlineKeyboardMarkup(menu_buttons)
    query.edit_message_text(
    reply_text,
    reply_markup=main_keyboard,
    timeout=60
    )