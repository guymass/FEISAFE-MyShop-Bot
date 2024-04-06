from lib.database import db
from lib import deco
from emoji import emojize
from time import sleep
from entries.mainmenu import mainmenu
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_command_handler("categories")
@deco.global_callback_handler(pattern="cb_categories")
def categories(update, context):
    chat_id = update.effective_chat.id
    cursor = db.buttons.find({})
    catlist = ""
    words = ""
    for b in cursor:
        catlist += str(b['ButtonName']) + "\n"
        words += str(b['ButtonCb']) + " | "

    text = emojize("\U0000200F אלו הקטגוריות האפשריות לשיוך מודעות. אנא השתמשו בפקודת העריכה לקטגוריות ובחרו את הקטגוריה המתאימה עבורה המודעה שלכם.\n\n")
    message = str(text + catlist)
    context.bot.send_message(chat_id=chat_id, text=message)
    sleep(1)
    mainmenu(update,context)
