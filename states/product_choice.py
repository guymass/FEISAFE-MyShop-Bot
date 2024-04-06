from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern='^p[1-4]$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def product_choice(update, context):

    query = update.callback_query
    data = update.callback_query.data

    user_data = context.user_data

    chat_id = update.effective_message.chat_id

    keyword = str(data)


    user_id = query.from_user.id



    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text
    button0 = ""
    button1 = ""
    button2 = ""
    button3 = ""

    menu_count = db.images.count()

    i = 0
    for i in range(0, menu_count):
        #text = update.callback_query.message.reply_markup.inline_keyboard[0][i].text
        exec("button%s = '%s'" % (i, i))
        #button%i = update.callback_query.message.reply_markup.inline_keyboard[0][i].text
        i += 1


    if button0 != "0" and keyword == "p1":
        p1 = update.callback_query.message.reply_markup.inline_keyboard[0][0].text
        print(p1)
        pass
    elif button1 != "1" and keyword == "p2":
        p2 = update.callback_query.message.reply_markup.inline_keyboard[1][0].text
        print(p2)
        pass
    elif button2 != "2" and keyword == "p3":
        p3 = update.callback_query.message.reply_markup.inline_keyboard[2][0].text
        print(p3)
        pass
    elif button3 != "3" and keyword == "p4":
        p4 = update.callback_query.message.reply_markup.inline_keyboard[3][0].text
        print(p4)
        pass

    if keyword == "p1":
            context.user_data['product'] = p1
            category = context.user_data['product']
            print("INLINE BUTTON >>>>>>>>> "+ p1)
            doc = db.tmp_orders.find_one_and_update(
            {"UserId": user_id},
            {"$set":
                {"ProductText": category}
            },upsert=True
            )

    elif keyword == "p2":
            context.user_data['product'] = p2
            category = context.user_data['product']
            print("INLINE BUTTON >>>>>>>>> "+ p2)
            doc = db.tmp_orders.find_one_and_update(
            {"UserId": user_id},
            {"$set":
                {"ProductText": category}
            },upsert=True
            )

    elif keyword == "p3":
            print(p3)
            context.user_data['product'] = p3
            category = context.user_data['product']
            print("INLINE BUTTON >>>>>>>>> "+ p3)
            doc = db.tmp_orders.find_one_and_update(
            {"UserId": user_id},
            {"$set":
                {"ProductText": category}
            },upsert=True
            )

    elif keyword == "p4":
            context.user_data['product'] = p4
            category = context.user_data['product']
            print("INLINE BUTTON >>>>>>>>> "+ p4)
            doc = db.tmp_orders.find_one_and_update(
            {"UserId": user_id},
            {"$set":
                {"ProductText": category}
            },upsert=True
            )

    if context.user_data.get(category):
        reply_text = '\U0000200F 👩‍🌾 הבחירה שלכם {} כבר שמורה אצלי\n'.format(common.facts_to_str(context.user_data))

    else:
        reply_text = "\U0000200F 👩‍🌾 בחרתם: {} \n".format(category) + '💬 אנא בחרו את הכמות הרצויה.\n'

    quantity_keyboard = []
    for q in db.qty.find({}):
        print(q)
        quantity = q['Qty']
        q_id = q['qID']
        quantity_keyboard = quantity_keyboard + [[InlineKeyboardButton(quantity, callback_data=q_id)]]

    cancel_text = emojize("👎 ביטול")
    cancel_text = str(cancel_text)

    quantity_keyboard +=  [[InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    quantity_keyboard = list(quantity_keyboard)
    reply_markup_quantity = InlineKeyboardMarkup(quantity_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_quantity)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(keyword))
    return states.FIRST
