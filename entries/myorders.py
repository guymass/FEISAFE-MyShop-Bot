from lib import deco
from emoji import emojize
from time import sleep
from entries.mainmenu import mainmenu
from lib.database import db
from time import sleep
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='myorders')
def myorders(update, context):
    chat_id = update.effective_chat.id
    msg = emojize("\U0000200F  \U0001F505 להלן רשימת ההזמנות שבצעתם \U0001F505 \n\n")
    user_id = context.user_data['user_id']
    print("UserID >>>>" + str(user_id))
    my_orders = db.products.find({})
    orders_list = []
    for o in my_orders:
        if str(user_id) == o['UserId']:
            
            order_id = str(o['OrderNumber'])
            category = o['Category']
            product = o['Product']
            quantity = str(o['Quantity'])
            price = str(o['Price'])
            date = str(o['Date'])
            msg += emojize('מספר הזמנה: ' + str(order_id) + "\n קטגוריה: " + str(category) + "\n\U0001F4E6  מוצר שהוזמן: " + str(product) + "\n כמות: " + 
                        str(quantity) + "\n מחיר: " + str(price) + "\n תאריך רכישה: " + str(date) + 
                        "\n\n\U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505  ")
            
            orders_list.append(msg)
            
        else:
            pass
    if len(orders_list) == 0:
        context.bot.send_message(chat_id=chat_id, text="אין לכם הזמנות במערכת!")
    else:
        for order in orders_list:
            context.bot.send_message(chat_id=chat_id, text=order)
        
    sleep(3)
    mainmenu(update, context)