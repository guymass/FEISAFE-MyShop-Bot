from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern="cb_blue")
def bluelight(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "להלן תוצאות החיפוש שלכם:\n\n"

    uvexlow = emojize("UVEX Low End 150ש\"ח")
    uvexsq = emojize("UVEX מרובעות 420ש\"ח")
    uvexround = emojize("UVEX עגולים - 420ש\"ח")
    redlight = emojize("אור אדום - 140ש\"ח כולל משלוח")
    iristech = emojize("IRIS TECH APP")
    raoptics = emojize("RA OPTICS 600-1000ש\"ח לזוג")
    blueblox = emojize("BLUE BLOX HI END - 300-500ש\"ח לזוג")
    blueblock = emojize("BLUE BLOCKER - 300-700ש\"ח לזוג")
    screen = emojize("מגן מסך - 70-500ש\"ח לפי גודל")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(uvexlow, callback_data="cb_uvexlow")]]
    buttons += [[InlineKeyboardButton(uvexsq, callback_data="cb_uvexsq")]]
    buttons += [[InlineKeyboardButton(uvexround, callback_data="cb_uvexround")]]
    buttons += [[InlineKeyboardButton(redlight, callback_data="cb_redlight")]]
    buttons += [[InlineKeyboardButton(iristech, callback_data="cb_iristech")]]
    buttons += [[InlineKeyboardButton(raoptics, callback_data="cb_raoptics")]]
    #buttons += [[InlineKeyboardButton(blueblox, callback_data="cb_blueblox")]]
    #buttons += [[InlineKeyboardButton(blueblock, callback_data="cb_blueblock")]]
    buttons += [[InlineKeyboardButton(screen, callback_data="screen")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    bluelight_keyboard = list(buttons)
    reply_markup_water = InlineKeyboardMarkup(bluelight_keyboard)

    if data == "cb_blue":
        cursor = db.videos.find({})
        for v in cursor:
            video_id = v['VideoId']
            video_text = v['VideoText']
            file_type = v['FileType']
            category = v['Category']
            if file_type == 'video/mp4' and v['Category'] == 'משקפי מגן':
                context.bot.send_video(chat_id, text=message, video=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
            elif file_type == 'document' and v['Category'] == 'משקפי מגן':
                context.bot.send_document(chat_id, text=message, document=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")