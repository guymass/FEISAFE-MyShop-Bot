from lib import deco
from emoji import emojize
from settings import CHATID
from time import sleep
from entries.completed import completed

@deco.run_async
@deco.global_command_handler("show_data")
def show_data(update, context):

    query = update.callback_query

    user_id = context.user_data['user_id']
    fullname = context.user_data['fullname']
    username = context.user_data['username']
    product = context.user_data['product']
    quantity = context.user_data['quantity']
    ordername = context.user_data['ordername']
    mobile = context.user_data['mobile']
    address = context.user_data['address']
    note = context.user_data['note']
    date = update.effective_message.date

    message = "\U0000200F \U0001F464 זיהוי משתמש: " + str(user_id)+ "\n\U0001F3F7 שם מלא: " + str(fullname)+ "\n\U0001F3F7 שם משתמש: " + str(username)+ "\n\U0001F3F7 מוצר: " + str(product) + "\n\U0001F3F7 כמות: "
    message += str(quantity)+ "\n\U0001F3F7 שם המזמין: " + str(ordername)+ "\n\U0001F4DE נייד: " + str(mobile)+ "\n\U0001F697 כתובת: "
    message += str(address)+ "\n\U00002139 הערת משלוח: " + str(note) + "\nתאריך: " + str(date) + "\n"
    print(message)
    message = emojize(message)
    msg = emojize("\U0000200F👩‍🌾 אלו הם פרטי ההזמנה עד כה: \n\n {}\n\n תודה שרכשתם אצלנו, משהו יצור אתכם קשר בקרוב, היו זמינים. \U0001F343".format(message))
    context.bot.send_message(chat_id=update.effective_message.chat_id, text=msg)
    message_admin = emojize("\U0000200F\U0001F343 \U0001F343 \U0001F343\n {}\n \U0001F343 \U0001F343 \U0001F343".format(message))

    context.bot.send_message(chat_id=CHATID, text=message_admin)
    sleep(2)
    completed(update, context)


