from lib import deco
from lib.database import db
from entries.welcome import welcome

@deco.run_async
def delete_messages(update, context):
    query = update.callback_query
    #message_id = update.callback_query.message.message_id
    #chat_id = query.message.chat.id
    chat_id = update.effective_message.chat_id
    cursor = db.messages.find({})
    for m in cursor:
        if m !=0:
            msgId = m["MessageId"]
            if msgId == 0:

                pass
            else:
                try:
                    context.bot.delete_message(chat_id, msgId)
                    print(str(msgId) + "<<<< ההודעה נמחקה")
                except:
                    pass
        else:
            pass
    start_message_id = context.user_data['start_message_id']
    start_message_id = start_message_id - 20

    msg_id_range = start_message_id+40
    for i in range(start_message_id, msg_id_range):
        try:
            context.bot.delete_message(chat_id, i)
            i += 1
        except:
            pass

    x = db.messages.delete_many({})
    z = db.tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    welcome(update, context)
