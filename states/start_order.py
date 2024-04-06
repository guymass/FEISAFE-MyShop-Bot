from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (common, deco, states)
from lib.database import db
from emoji import emojize
from time import sleep

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern='^begin$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def start_order(update, context):
    query = update.callback_query
    query.answer()
    text = query
    fullname = context.user_data['fullname']
    opts = []
    o = []
    product_keyboard = []

    if context.user_data.get(text):
        reply_text = '\U0000200F הבחירה שלכם {} כבר שמורה אצלי\n' \
                     'המידע שברשותי כרגע הינו:\n {}'.format(common.facts_to_str(context.user_data))
    else:
        reply_text = emojize('\U0000200F 👩‍🌾 מצויין , אנא בחרו אחד מהמוצרים שברשימה.\n\nאם אתם מעוניינים ביותר  ממוצר אחד פשוט שלחו לי הזמנה נוספת לאחר שסיימתם את זו.')
        chat_id = update.effective_chat.id

        PhotoId = ""
        imageText = ""
        imageDate = ""

        for image in db.images.find({}):

            PhotoId = image['PhotoId']
            imageText = image['ImageText']
            imageDate = image['ImageDate']
            #print(imageUrl)

            msg = emojize("\U0000200F :key: קוד בחירה: "+str(imageText)+"\n" + " :watch: פורסם בתאריך: " +str(imageDate)+"\n")
            #time.sleep(1)
            #context.bot.send_message(chat_id, text=msg, timeout=30)
            #context.bot.send_photo(chat_id, PhotoId, msg, parse_mode='HTML')

            if image['FileType'] == "video/mp4" or image['FileType'] == "video":
                context.bot.send_video(chat_id, video=PhotoId, caption=msg, parse_mode='HTML')
                sleep(1)
            elif image['FileType'] == "document":
                context.bot.send_document(chat_id, document=PhotoId, caption=msg, parse_mode='HTML')
                sleep(1)
            elif image['FileType'] == "photo":
                context.bot.send_photo(chat_id, PhotoId, msg, parse_mode='HTML')
                sleep(1)

        for img in db.images.find({}):
            prd_code = img['PhotoCode']
            prd_name = img['ImageText']

            prd_name = emojize(prd_name)

            product_keyboard = product_keyboard + [[InlineKeyboardButton(prd_name, callback_data=prd_code)]]

        cancel_text = emojize("👎 ביטול")
        cancel_text = str(cancel_text)
        product_keyboard +=  [[InlineKeyboardButton(cancel_text, callback_data="cancel")]]
        product_keyboard = list(product_keyboard)
        reply_markup_product = InlineKeyboardMarkup(product_keyboard)

        context.bot.send_message(chat_id, text=reply_text, reply_markup=reply_markup_product)
    
    return states.FIRST
