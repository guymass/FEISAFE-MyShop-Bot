from lib import deco
from lib.database import db
from time import sleep
from settings import CHATID
import logging

logger = logging.getLogger(__name__)

@deco.run_async
@deco.conversation_command_handler("set")
def set(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    args1 = str(context.args[0])
    args2 = str(context.args[1])
    try:
        args3 = str(context.args[2])
    except:
        args3 = ""

    cat_name = str(args2) + ' ' +  str(args3)
    print("CATEGORY TO UPDATE >>>>>>>>" + str(cat_name))
    string = str(cat_name)
    cursor = db.videos.find({})
    cur_cat = db.buttons.find({})
    cat_arr = []
    for v in cursor:
        if v['UserId'] == user_id and string != "":
            if v['VideoCode'] == args1:
                for catitem in cur_cat:
                    cat_arr.append(catitem[u'ButtonName'])
                    #print("BUTTON NAME: >>>>>" + str(catitem['ButtonName']))
                    #cat_list = list(cat_arr)
                if string in cat_arr:
                    db.videos.update_one({'VideoCode': str(args1)}, {'$set': {'Category': string}})
                    context.bot.send_message(chat_id=chat_id, text="המודעה עודכנה בהצלחה ל {}".format(string))
                else:
                    
                    print(cat_arr)
                    context.bot.send_message(chat_id=chat_id, text="שם הקטגוריה שהקלדתם לא תואמת את רשימת הקטגוריות הניתנות לשיוך. אנא בדקו את הרשימה   מהכפתור בתפריט ולאחר מכן נסו שנית.")
                    
