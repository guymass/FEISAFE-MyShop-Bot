from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from emoji import emojize
from lib import deco
from lib.database import db
from entries.myorders import myorders
from entries.pmenu import pmenu
import logging

logger = logging.getLogger(__name__)

cbs = "session|org|health|body|todo|screen|crystal|cleaner|digital|silver|myorders"

#@deco.restricted
@deco.global_callback_handler(pattern='radiation')
@deco.global_callback_handler(pattern=f'^cb_({cbs})$')
def article(update, context):
    query = update.callback_query
    data = query.data
    cb_data = str(data)
    chat_id = update.effective_chat.id
    
    user_id = context.user_data['user_id']
    message = "להלן תוצאות החיפוש שלכם:\n\n"
    order_bio = emojize("\U000025C0 הזמן עכשיו")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    cb_list = ['cb_digital', 'cb_cleaner', 'cb_water', 'cb_live', 'cb_blue', 'cb_session', 'cb_org', 'cb_body', 'cb_todo', 'cb_health', 'cb_screen', 'radiation', 'cb_crystal', 'cb_cleaner', 'cb_digital', 'cb_screen', 'cb_silver']
    
    buttons = [[InlineKeyboardButton(order_bio, callback_data="cb_order_bio")]]
    
    if data in cb_list:
        buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
        print("CB DATA in CBLIST >>>>> " + str(data))
    elif data not in cb_list and data != 'cb_myorders':
        print("ELSE DATA >>>>> " + str(data))
        buttons += [[InlineKeyboardButton(pmenu, callback_data="pmenu")]]
        # TODO : resize_keyboard
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    bioarticle_keyboard = list(buttons)
    reply_markup_bioarticle = InlineKeyboardMarkup(bioarticle_keyboard)
    
    if data in cb_list:
        context.bot.send_message(chat_id, message, parse_mode="HTML")
        biocursor = db.videos.find({})
        for bio in biocursor:
            video_id = bio['VideoId']
            video_text = bio['VideoText']
            file_type = bio['FileType']
            category = bio['Category']
            callback = bio['MenuCb']
            print(callback)
            print(file_type)
            if file_type == 'video/mp4' and data == callback:
                context.bot.send_video(chat_id, video=video_id, caption=video_text, reply_markup=reply_markup_bioarticle, parse_mode='HTML')
                result1 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ProductText':video_text}})
                result2 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'VideoCode':video_id}})
                result3 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Price':0.0}})
                result4 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':category}})
            elif file_type == 'document' and data == callback:
                context.bot.send_document(chat_id, document=video_id, caption=video_text, reply_markup=reply_markup_bioarticle, parse_mode='HTML')
                result1 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ProductText':video_text}})
                result2 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'VideoCode':video_id}})
                result3 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Price':0.0}})
                result4 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':category}})
    
    #cb_data = update.callback_query.data
    elif data == 'cb_myorders':
        myorders(update, context)
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")
        

   