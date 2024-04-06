# from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
# from lib import states
# from time import sleep

# @deco.run_async
# def begin(update, context):
#     chat_id = update.effective_message.chat_id

#     if context.user_data['fullname'] != "":
#         reply_text = "\U0000200F👩‍🌾 תודה שחזרת אלינו -  {} \n".format(context.user_data.keys())
#     else:
#         reply_text = "\U0000200F\n👩‍🌾 להתחלת הזמנה לחץ על התחל. {} ".format(context.user_data['fullname']) + "אתם יכולים להתחיל מחדש על ידי לחיצה על ביטול\n /cancel | ביטול\n"

#     sleep(5)
#     start_keyboard = [
#             [InlineKeyboardButton("התחל", callback_data="begin"),
#              InlineKeyboardButton("ביטול", callback_data=str("cancel"))
#              ]
#         ]
#     reply_markup_start = InlineKeyboardMarkup(start_keyboard)
#     update.message.reply_text(
#     reply_text,
#     reply_markup=reply_markup_start
#     )
#     return states.FIRST
