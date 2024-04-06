from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
import logging
from emoji import emojize
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='^cb_water$')
def water(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "להלן תוצאות החיפוש שלכם:\n\n"
    order_water = emojize("\U000025C0 הזמן עכשיו")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    buttons = [[InlineKeyboardButton(order_water, callback_data="cb_order_water")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    water_keyboard = list(buttons)
    reply_markup_water = InlineKeyboardMarkup(water_keyboard)

    #query.edit_message_text(message, reply_markup=reply_markup_water, parse_mode="markdown")

    if data == "cb_water":
        cursor = db.videos.find({})
        for v in cursor:
            video_id = v['VideoId']
            video_text = v['VideoText']
            file_type = v['FileType']
            category = v['Category']
            if file_type == 'video/mp4' and v['Category'] == 'פילטרים':
                context.bot.send_video(chat_id, text=message, video=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
            elif file_type == 'document' and v['Category'] == 'פילטרים':
                context.bot.send_document(chat_id, text=message, document=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")