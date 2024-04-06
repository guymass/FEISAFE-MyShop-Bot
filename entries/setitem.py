from lib import deco
from lib.database import db

@deco.restricted
@deco.run_async
@deco.global_command_handler("setitem")
def setitem(update, context):
    chat_id = update.effective_message.chat_id
    text = str(context.args)
    text = text.strip("[\']")
    #update.message.reply_text(chatId, "Updating status to delivered for {}...")
    result = db["completed"].find({})
    for r in result:
        Mobile = str(r["Mobile"])
        if Mobile == text:
            context.bot.send_message(chat_id, "...מעדכן רשומה למצב סופק")
            db["completed"].find_one_and_update({"Mobile": text}, {"$set":{"Status": "Delivered"}})
            context.bot.send_message(chat_id, "<b>Update SUCCESS!</b>", parse_mode='HTML')
            context.bot.send_message(chat_id, "הרשומה עודכנה בהצלחה!")
