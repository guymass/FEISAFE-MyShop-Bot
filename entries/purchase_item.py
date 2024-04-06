from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
from emoji import emojize
import logging
import datetime
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='^cb_purchase$')
def purchase_item(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']
    username = update.effective_message.from_user.username
    firstname = update.effective_message.from_user.first_name
    lastname = update.effective_message.from_user.last_name
    date = datetime.datetime.utcnow()

    print(user_id)

    cursor = db.tmp_product.find({})

    for res in cursor:
        if res['UserId'] == user_id:

            username = str(res['UserName'])
            user_id = str(res['UserId'])
            fullname = str(res['FullName'])
            product = str(res['ProductText'])
            category = str(res['Category'])
            image_id = str(res['PhotoId'])
            price = str(res['Price'])
            date = str(res['Date'])
            status = str(res['Status'])
        else:
            pass

    message = "\U0000200F \U0001F505 אלו הם פרטי ההזמנה: \U0001F505\n\n"
    message += "שם המזמין: @"+ username + "\n"
    message += "קוד זיהוי: " + user_id+"\n"
    message += "שם מלא: "+fullname+"\n"
    message += "קטגורית מוצר: "+category+"\n"
    message += "\U0001F5E3 פרטי המוצר:\n\n"+product+"\n\n"
    #message += "מחיר: "+price+"\n"
    message += "תאריך הזמנה: "+date+"\n"
    message += "סטטוס הזמנה: "+status+"\n\n"
    message += "לחיצה על אישור מהווה הסכמה לרכישה. אין אנו מבצעים גבייה כעת. אנו ניצור עמכם קשר לחיוב וקבלת פרטי משלוח."

    approve = emojize("\U0001F44D אישור")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(approve, callback_data="approve_order")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    approve_keyboard = list(buttons)
    reply_markup_approve = InlineKeyboardMarkup(approve_keyboard)
    context.bot.send_message(chat_id, text=message, reply_markup=reply_markup_approve, parse_mode="HTML")