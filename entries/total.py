from lib import deco
from lib.database import db
from emoji import emojize

@deco.restricted
@deco.run_async
@deco.global_command_handler("total")
def total(update, context):
    chat_id = update.effective_message.chat_id
    result = db["completed"].find({})
    total_orders = []
    sum = 0
    for r in result:
        status = str(r["Status"])
        if status == "Delivered":
            total_orders.append(r["Quantity"])
            msg = emojize("\U0000200F☑️ הזמנה שסופקה:" + "\n" + str(r["UserId"]) + "\n" + str(r["UserName"]) + "\n" + str(r["FullName"]) + "\n" + "קוד מוצר: " + str(r["Product"]) + "\n" + "כמות: " +str(r["Quantity"]))
            msg2 = emojize("\U0000200F\n" + str(r["Mobile"]) + "\n" + str(r["Address"]) + "\n" + str(r["Message"]) + "\n\U0001F973 " + str(r["Status"]) + " \U0001F973\n" + str(r["Date"]))
            context.bot.send_message(chat_id, msg+msg2)

    for i in range(0, len(total_orders)):
        sum = sum + total_orders[i];

    msg = emojize("\U0000200F סך כל ההזמנות שסופקו:\n {} ".format(sum))
    context.bot.send_message(chat_id, msg)
