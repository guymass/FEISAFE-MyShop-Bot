from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
import logging
from emoji import emojize
import datetime
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern="uvexmenu")
def uvexmenu(update, context):
    query = update.callback_query
    data = query.data
    text = query.message.text
    chat_id = update.effective_chat.id
    date = datetime.datetime.utcnow()

    print("DATA FROM UVEXMENU >>>>>>" + str(data))
    purchase = emojize("\U0001F4B3 המשך לרכישה")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(purchase, callback_data="cb_purchase")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    bluelight_keyboard = list(buttons)

    text = "*** \
            הזמינו את שלכם היום \
            *** \
            "

    reply_markup_uvex = InlineKeyboardMarkup(bluelight_keyboard)
    context.bot.send_message(chat_id, text=text, reply_markup=reply_markup_uvex, parse_mode="HTML")
    cblist = ['cb_uvexround', 'cb_uvexsq', 'cb_uvexlow', 'cb_redlight', 'cb_iristech', 'cb_raoptics', 'cb_blueblox', 'cb_blueblock', 'screen']
    cursor = db.images.find({})
    for res in cursor:
        if res['MenuCb'] == data and data in cblist:
            user_id = context.user_data['user_id']
            cursor2 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ProductText':res['PhotoText']}})
            cursor3 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'PhotoId':res['PhotoId']}})
            cursor4 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':res['Category']}})
            cursor5 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Quantity':"1"}})
            cursor6 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Price':0.0}})