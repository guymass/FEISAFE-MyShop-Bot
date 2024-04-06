from lib import deco
from lib.database import db
from time import sleep
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.restricted
@deco.global_callback_handler(pattern="cb_pmenu")
def products(update, context):
    products = db.images.find({})
    update.message.reply_text("\U0000200F אלו הם המוצרים הזמינים לבוט.\n\n")
    for prd in products:
        ImageId = prd['ImageId']
        msg = prd['ImageText']
        if prd['FileType'] == "video/mp4" or prd['FileType'] == "video":
            context.bot.send_video(CHATID, video=ImageId, caption=msg, parse_mode='HTML')
            sleep(1)
        elif prd['FileType'] == "document":
            context.bot.send_document(CHATID, document=ImageId, caption=msg, parse_mode='HTML')
            sleep(1)
        elif prd['FileType'] == "photo":
            context.bot.send_photo(CHATID, ImageId, msg, parse_mode='HTML')
            sleep(1)
