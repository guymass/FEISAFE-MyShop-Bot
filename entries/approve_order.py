from lib import deco
from lib.database import db
from lib import common
from emoji import emojize
from random import choice
from string import ascii_uppercase
from time import sleep
from entries.delete_messages import delete_messages
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_callback_handler(pattern="^approve_order$")
def approve_order(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']
    print(data)
    if data == 'approve_order':
        cursor = db.tmp_product.find({'UserId':user_id})
        for res in cursor:
            username = str(res['UserName'])
            user_id = str(res['UserId'])
            fullname = str(res['FullName'])
            product = str(res['ProductText'])
            category = str(res['Category'])
            image_id = str(res['PhotoId'])
            quantity = str(res['Quantity'])
            price = str(res['Price'])
            date = str(res['Date'])
            status = str(res['Status'])

    order_number = ''.join(choice(ascii_uppercase) for i in range(12))


    one_completed_order = {

        "OrderNumber":order_number,
        "UserId":user_id,
        "UserName":username,
        "FullName":fullname,
        "Product":product,
        "Category":category,
        "PhotoId":image_id,
        "VideoId":"",
        "Quantity":quantity,
        "Price":0.0,

        "Mobile":"",
        "Address":"",
        "Location":"",
        "Status":"הזמנה חדשה",
        "Date":date,

    }
    db.products.insert_one(one_completed_order)
   
   
    message = "\U0000200F  \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505\n"
    message += "\U0001F505 אלו הם פרטי ההזמנה: \U0001F505\n\n"
    message += "מספר הזמנה: "+ order_number + "\n"
    message += "שם המזמין: @"+ username + "\n"
    message += "קוד זיהוי: " + user_id+"\n"
    message += "שם מלא: "+fullname+"\n"
    message += "קטגורית מוצר: "+category+"\n\n"
    message += "\U0001F5E3 פרטי המוצר:\n\n"+product+"\n\n"
    message += "כמות: "+quantity+"\n"
    message += "מחיר: "+price+"\n"
    message += "תאריך הזמנה: "+date+"\n"
    message += "סטטוס הזמנה: "+status+"\n\n"
    message += "\U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505"
    
    # Send Order Details Message to current chat
    context.bot.send_message(chat_id, "\U0000200F \U0001F505 להלן פרטי ההזמנה שרכשתם: \U0001F505 \n\n{}\n\nתודה שרכשתם בחנות של \"מעלים את התדר 528\" הזמנתכם התקבלה במערכת!, אנו נתקשר עמכם בהקדם לתאום משלוח.\U0001F505 להתראות.\n\n".format(message))
    # Send Order Details Message to customer
    context.bot.send_message(user_id, "\U0000200F \U0001F505 להלן פרטי ההזמנה שרכשתם: \U0001F505 \n\n{}\n\nתודה שרכשתם בחנות של \"מעלים את התדר 528\" הזמנתכם התקבלה במערכת!, אנו נתקשר עמכם בהקדם לתאום משלוח.\U0001F505 להתראות.\n\n".format(message))
    # Send Order Details Message to Bot Management Group
    context.bot.send_message(CHATID, "\U0001F981 קבלתם הזמנה חדשה! \n\n {}\n\n".format(message))

    sleep(5)
    delete_messages(update, context)
