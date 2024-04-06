from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import deco
from lib.database import db
from emoji import emojize
from time import sleep
from settings import CHATID
import logging
logger = logging.getLogger(__name__)


@deco.run_async
@deco.global_command_handler('start_order')
def start_order(update, context):


    query = update.callback_query
    query.answer()
    text = query

    opts = []
    o = []
    product_keyboard = []

    if context.user_data.get(text):
        reply_text = '\U0000200F הבחירה שלכם {} כבר שמורה אצלי\n' \
                     'המידע שברשותי כרגע הינו:\n {}'.format(facts_to_str(context.user_data))
    else:
        reply_text = emojize('\U0000200F :fire: מעולה! אנא גללו למעלה וצפו במוצרים הזמינים במלאי ובחרו מוצר אחד להזמנה.\n')
        chat_id = update.effective_chat.id

        imageId = ""
        imageText = ""
        imageDate = ""

        for image in db.images.find({}):

            imageId = image['PhotoId']
            imageText = image['ImageText']
            imageDate = image['ImageDate']
            #print(imageUrl)

            msg = emojize("\U0000200F :key: קוד בחירה: "+str(imageText)+"\n" + " :watch: פורסם בתאריך: " +str(imageDate)+"\n")
            #time.sleep(1)
            #context.bot.send_message(chat_id, text=msg, timeout=30)
            context.bot.send_photo(chat_id, photo=imageId, caption=msg, timeout=60)


        for img in db.images.find({}):
            prd_code = img['ImageCode']
            prd_name = img['ImageText']

            prd_name = emojize(" \U0001f31f " + prd_name)

            product_keyboard = product_keyboard + [[InlineKeyboardButton(prd_name, callback_data=prd_code)]]

        cancel_text = emojize("👎 ביטול")
        cancel_text = str(cancel_text)
        product_keyboard +=  [[InlineKeyboardButton(cancel_text, callback_data="cancel")]]
        product_keyboard = list(product_keyboard)
        reply_markup_product = InlineKeyboardMarkup(product_keyboard)

        context.bot.send_message(chat_id, text=reply_text, reply_markup=reply_markup_product)
    return FIRST
