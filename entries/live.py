
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_callback_handler(pattern='cb_live')
def live(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "להלן תוצאות החיפוש שלכם:\n\n"
    order_halfinch = emojize("\U0001F4A6 מתקן חצי אינצ' (לבית) - 3300 ש\"ח")
    order_3q = emojize("\U0001F4A6 מתקן 3/4 אינצ' (לבית) 4400ש\"ח")
    order_1in = emojize("\U0001F4A6 מתקן 1 אינצ' (שימוש חקלאי / תעשייתי)")
    order_125 = emojize("\U0001F4A6 מתקן 1.25 אינצ' (שימוש חקלאי / תעשייתי)")
    order_2in = emojize("\U0001F4A6 מתקן 2 אינצ' (שימוש חקלאי / תעשייתי)")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    buttons = [[InlineKeyboardButton(order_halfinch, callback_data="cb_halfinch")]]
    buttons += [[InlineKeyboardButton(order_3q, callback_data="cb_3q")]]
    buttons += [[InlineKeyboardButton(order_1in, callback_data="cb_1in")]]
    buttons += [[InlineKeyboardButton(order_125, callback_data="cb_125")]]
    buttons += [[InlineKeyboardButton(order_2in, callback_data="cb_2in")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    water_keyboard = list(buttons)
    reply_markup_water = InlineKeyboardMarkup(water_keyboard)

    #query.edit_message_text(message, reply_markup=reply_markup_water, parse_mode="markdown")

    if data == "cb_live":
        cursor = db.videos.find({})
        for v in cursor:
            video_id = v['VideoId']
            video_text = v['VideoText']
            file_type = v['FileType']
            category = v['Category']
            if file_type == 'video/mp4' and v['Category'] == 'מים חיים':
                context.bot.send_video(chat_id, text=message, video=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
            elif file_type == 'document' and v['Category'] == 'מים חיים':
                context.bot.send_document(chat_id, text=message, document=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")
