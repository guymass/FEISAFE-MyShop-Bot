
from lib import (deco, states)
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import Filters
from emoji import emojize
from time import sleep
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
#@deco.conversation_message_handler(Filters.regex('^cb_get_category$', callback_data='cb_goodbye'))
@deco.register_state_message(states.CAT_NAME, Filters.regex('^cb_get_category$'))
def get_category(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    text = update.message.text
    print(text)

    if text != '':
        context.user_data['video_code'] = str(text)
        video_code = context.user_data['video_code']
        cancel_keyboard = []
        cancel_keyboard +=  [[InlineKeyboardButton("ביטול", callback_data="cb_back")]]
        #cancel_keyboard +=  [[InlineKeyboardButton("הבא", callback_data="cb_goodbye")]]
        cancel_keyboard = list(cancel_keyboard)
        reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)
        context.bot.send_message(chat_id=chat_id, text="\U0000200F 👩‍🌾 💬 אנא שלחו לי את שם הקטגוריה לשיוך, אני ממתין...⏳", reply_markup=reply_markup_cancel, callback_data="cb_goodbye")
        return states.GOODBYE
        
    elif text == '':
        context.bot.send_message(chat_id=chat_id, text="\U0000200F 👩‍🌾 💬 לא קבלתי קוד מודעה, אנא שלחו קוד אני ממתין...⏳", reply_markup=reply_markup_cancel, callback_data="cb_goodbye")
        return states.ORDERID     

    
