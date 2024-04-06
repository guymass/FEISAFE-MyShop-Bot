from lib.database import db
from lib import deco
from emoji import emojize
from time import sleep
from entries.mainmenu import mainmenu
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.conversation_command_handler("setcategory")
@deco.global_callback_handler(pattern="cb_setcategory")
def setcategory(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    args = []
    i=1
    context_len = len(context.args)

    if context_len == 2:
        cat_name = str(context.args[1])
    if context_len == 3:
        cat_name = str(context.args[1]) + ' ' +  str(context.args[2])

    cursor = db.videos.find({})
    for v in cursor:
        if v['UserId'] == user_id:
            if v['VideoCode'] == context.args[0]:
                db.videos.update_one({'VideoCode': str(context.args[0])}, {'$set': {'Category': str(cat_name)}})
    context.bot.send_message(chat_id=chat_id, text="המודעה עודכנה ושויכה לקטגוריה {}.".format(cat_name))
    #update.message.reply_text("המודעה עודכנה ושויכה לקטגוריה {}.".format(cat_name))
    sleep(1)
    mainmenu(update, context)