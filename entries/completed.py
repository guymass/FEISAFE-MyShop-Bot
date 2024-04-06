from lib import deco
from lib.database import db
from random import choice
from string import ascii_uppercase
from time import sleep
from entries.delete_messages import delete_messages
from emoji import emojize
import logging
logger = logging.getLogger(__name__)



@deco.run_async
def completed(update, context):
    query = update.callback_query
    data = context.user_data
    message_date = update.effective_message.date
    chat_id = update.effective_chat.id
    print(''.join(choice(ascii_uppercase) for i in range(12)))
    order_number = ''.join(choice(ascii_uppercase) for i in range(12))
    user_id = context.user_data['user_id']

    one_completed_order = {

        "OrderNumber":order_number,
        "UserId":data['user_id'],
        "UserName":data['username'],
        "FullName":data['fullname'],
        "Product":data['product'],
        "Quantity":data['quantity'],
        "Mobile":data['mobile'],
        "Address":data['address'],
        "Message":data['note'],
        "Status":"Waiting",
        "Date":message_date,

    }
    db.completed_orders.insert_one(one_completed_order)
    context.bot.send_message(chat_id, "\U0000200F 👩‍🌾 הזמנתכם נשלחה! בקרוב יצרו עמכם קשר, היו זמינים. תודה ולהתראות.")

    sleep(5)
    delete_messages(update, context)

