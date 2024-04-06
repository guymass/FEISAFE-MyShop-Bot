from telegram.ext import Filters
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (deco, states)
from lib.database import db

@deco.run_async
@deco.register_state_message(states.SECOND, Filters.text, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def typing_name(update, context):

    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['ordername'] = text
    category = context.user_data['ordername']



    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)
    if category != 0:

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"FullName": category}
        },upsert=True
        )

        update.message.reply_text("\U0000200F 👩‍🌾 אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n\n 💬 אנא כתבו ושלחו לי את הנייד שלכם להתקשרות, אני ממתין...⏳", reply_markup=reply_markup_cancel)

    return states.THIRD

