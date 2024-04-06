from lib.database import db
from lib import (deco, states)
from telegram.ext import Filters
from emoji import emojize
from time import sleep
from settings import CHATID
from entries.mainmenu import mainmenu
import logging
logger = logging.getLogger(__name__)

@deco.run_async
#@deco.conversation_message_handler(Filters.regex('^cb_goodbye$'))
@deco.register_state_message(states.GOODBYE, Filters.regex('^cb_goodbye$'))
def goodbye(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    text = update.message.text
    print(text)
    context.user_data['category_name'] = str(text)
    category_name = context.user_data['category_name']
    video_code == context.user_data['video_code']

    cursor = db.videos.find({})
    curcat = db.buttons.find({})
    category_list = []
    for cat in curcat:
        category_list.append(cat['ButtonName'])


    print(category_name)

    if category_name in category_list:

        for p in cursor:
            if video_code == p['VideoCode'] and user_id == p['UserId']:
                update_one = db.videos.find_one_and_update({'VideoCode':video_code}, {'$set':{'Category':str(category_name)}})
                message = emojize("מודעתכם שוייכה בהצלחה לקטגוריה {}\n".format(category_name))
                update.message.reply_text(chat_id=chat_id, text=message)
            else:
                pass
        
    else:
        message = emojize("\U0000200F 👩‍🌾 💬 מודעתכם לא עודכנה! יתכן והקוד שהזנתם שגוי, שהמודעה אינה משוייכת אליכם או שהמודעה לא קיימת! אנא נסו שוב.")
        update.message.reply_text(chat_id=chat_id, text=message)

    
    
    sleep(1)
    mainmenu(update, context)
    return ConversationHandler.END