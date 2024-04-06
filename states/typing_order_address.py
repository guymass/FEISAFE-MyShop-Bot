from telegram.ext import Filters
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (deco, states)
from lib.database import db

@deco.run_async
@deco.register_state_message(states.THIRD, Filters.text, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def typing_order_address(update, context):
    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['mobile'] = text
    category = context.user_data['mobile']


    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)
    if category != 0 and category.isdecimal():

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Mobile": category}
        },upsert=True
        )

        update.message.reply_text("\U0000200F 👩‍🌾 אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n\n 💬אנא שלחו לי כתובת למשלוח, אני ממתין...⏳", reply_markup=reply_markup_cancel)
        return states.FORTH

    elif category.isdecimal() != 1:
        update.message.reply_text("\U0000200F 👩‍🌾 אנא שלחו רק מספרים!\n\n 💬אנא שלחו מספר נייד עדכני, אני ממתין...⏳", reply_markup=reply_markup_cancel)

    elif category.isdecimal() == 0:
        #typing_order_address(update, context)
        return states.THIRD

