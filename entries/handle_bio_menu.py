from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
from emoji import emojize
import datetime
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='cb_order_bio')
def handle_bio_menu(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']
    date = datetime.datetime.utcnow()
    cblist = ['cb_health', 'cb_crystal', 'cb_todo', 'radiation', 'cb_cleaner', 'cb_screen', 'cb_org', 'cb_body', 'cb_digital', 'cb_order_bio', 'cb_silver', 'cb_live', 'cb_blue', 'cb_water']

    if data in cblist:
        result_handler = db.tmp_product.find({})
        for h in result_handler:
            if h['UserId'] == user_id:

                if data == "cb_water":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'פילטרים'}})
                elif data == "cb_live":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'מים חיים'}})
                elif data == "cb_blue":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'משקפי מגן'}})
                elif data == "cb_screen":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'אור אדום'}})
                elif data == "radiation":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'מד קרינה'}})
                elif data == "cb_crystal":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'קערות קריסטל'}})
                elif data == "cb_digital":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'מוזיקה'}})
                elif data == "cb_cleaner":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'מטהר אויר'}})
                elif data == "cb_silver":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'מי כסף'}})
                elif data == "cb_health":
                    cursor = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':'ביו'}})
                username = h['UserName']
                user_id = h['UserId']
                fullname = h['FullName']
                product = h['ProductText']
                category = h['Category']
                image_id = h['PhotoId']
                quantity = h['Quantity']
                price = h['Price']
                date = h['Date']
                status = h['Status']
    message = "\U0000200F  \U0001F505 אלו הם פרטי ההזמנה: \U0001F505\n\n"
    message += "שם המזמין: @"+ username + "\n"
    message += "קוד זיהוי: " + str(user_id)+"\n"
    message += "שם מלא: "+fullname+"\n"
    message += "קטגורית מוצר: "+category+"\n"
    message += "\U0001F5E3 פרטי המוצר:\n\n"+product+"\n\n"
    message += "מחיר: "+str(price)+"\n"
    message += "תאריך הזמנה: "+str(date)+"\n"
    message += "סטטוס הזמנה: "+status+"\n\n"
    message += "לחיצה על אישור מהווה הסכמה לרכישה. אין אנו מבצעים גבייה כעת. אנו ניצור עמכם קשר לחיוב וקבלת פרטי משלוח."

    approve_order = emojize("\U0001F44D אישור")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(approve_order, callback_data="approve_order")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    approve_keyboard = list(buttons)
    reply_markup_approve = InlineKeyboardMarkup(approve_keyboard)
    context.bot.send_message(chat_id, text=message, reply_markup=reply_markup_approve, parse_mode="HTML")
