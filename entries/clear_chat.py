from lib import deco
from lib.database import db
from emoji import emojize
import logging
from entries.welcome import welcome
logger = logging.getLogger(__name__)

@deco.restricted
@deco.global_command_handler("clear_chat")
def clear_chat(update, context):
    query = update.callback_query
    if query != "NoneType" and query != "":
        data = query.data
    else:
        pass
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
    if context.user_data == "":
        user_id = update.effective_message.from_user.id
    elif data == "cb_back":
        user_id = context.user_data['user_id']
    else:
        user_id = query.from_user.id
    #start_message_id = context.user_data['start_message_id']


    cur = db.messages.find_one({"UserId": user_id})
    if cur['MessageId'] == "":
        pass
    else:
        start_message_id = cur['MessageId'] - 10

    msg_id_range = start_message_id+20
    for i in range(start_message_id, msg_id_range):

        try:
            context.bot.delete_message(chat_id, i)
            i += 1
        except:
            pass

    x = db.messages.delete_many({})
    y = db.tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    welcome(update, context)