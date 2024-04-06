from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.conversation_command_handler("remove")
def delete_ad(update, context):
    user_id = update.effective_message.from_user.id
    code = str(context.args[0])
    cursor = db.videos.find({})

    for vid in cursor:
        if vid['UserId'] == user_id and vid['VideoCode'] == code:
            cur = db.videos.find_one_and_delete({"VideoCode": code})
            update.message.reply_text("מודעה עם קוד {} נמחקה מהמאגר!".format(code))
        elif vid['UserId'] != user_id or vid['UserId'] == "":
            update.message.reply_text("מודעה עם קוד {} לא נמצאה או שהקוד שגוי או שמודעה זו אינה משוייכת אל החשבון ממנו אתם מחוברים. אנא בדקו את הפרטים ונסו שנית.".format(code))

