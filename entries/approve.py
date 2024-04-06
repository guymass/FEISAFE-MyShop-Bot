from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.restricted
@deco.run_async
@deco.conversation_command_handler("approve")
def approve(update, context):
      
    code = str(context.args[0])
    print(code)
    cur = db.videos.find_one_and_update({"VideoCode": code},
                                    {"$set": {"Status": "approved"}})
    update.message.reply_text("מודעה עם קוד {} אושרה!".format(code))