from lib import deco
from lib.database import db
import logging
from entries.mainmenu import mainmenu

logger = logging.getLogger(__name__)

buttons = db.buttons.find({})
pattern = "|".join(
    list(map(lambda btn: (str(btn['ButtonCb'])), buttons))
)

if pattern == "":
    pattern = "never_gonna_get_here"

@deco.run_async
@deco.global_callback_handler(pattern=f'^{pattern}$')
def search(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    cursor = db.buttons.find_one({"ButtonCb":data})
    text = cursor['ButtonName']

    context.bot.send_message(chat_id, text="מחפש מודעות בקטגוריה {}".format(text))
    mainmenu(update,context)