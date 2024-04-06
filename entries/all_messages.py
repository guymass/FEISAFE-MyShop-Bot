from telegram import MessageEntity
from telegram.ext import Filters
from lib import deco
from lib.database import db

@deco.run_async
@deco.global_message_handler(Filters.user('@bottwoilbot') and Filters.entity(MessageEntity.TEXT_LINK) and (
        Filters.entity(MessageEntity.URL)) and (Filters.text) and (Filters.command))
def all_messages(update, context):

    msgId = update.message.message_id
    text = update.message.text

    item = {
        "MessageId":msgId,
        "MessageText":text
    }

    if db.messages.count_documents({'MessageId': msgId}, limit=1) > 0:
        print("הודעה רשומה כבר!")
        pass
    else:
        db.messages.insert_one(item)
        print(str(msgId) + " >>>>>>> פרטי ההודעה נשמרו! <<<<<<<<<<")
        pass