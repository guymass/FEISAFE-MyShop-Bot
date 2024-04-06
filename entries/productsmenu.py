from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='^cb_products$')
def productsmenu(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "לפניכם רשימת מוצרים שאנו מוכרים ומשווקים לקהל העוקבים שלנו. הזמנה שתתקבל דרך הבוט תשלח לאחר קבלת התשלום. החיוב אינו מתבצע דרך הבוט, רק ההזמנה, אנו נחזור אליכם ברגע קבלת ההזמנה.\n\n"

    water_filter= emojize("\U0001F6B0 מזקק מים איכותי")
    live_water = emojize("\U0001F4A6 מתקני מים חיים לבית")
    blue_light = emojize("\U0001F4A1 הגנה מתאורה כחולה")
    radiation = emojize("\U00002622 מד קרינה")
    crystal = emojize("\U0001F963 דיסק 528 עם קערות קריסטל")
    air_cleaner = emojize("\U0001F32C מטהר ומחטא אויר לבית")
    silver_water = emojize("\U000026F2 מכונה להכנת מי כסף")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    if data == "cb_products":

        buttons = [[InlineKeyboardButton(water_filter, callback_data="cb_water")]]
        buttons += [[InlineKeyboardButton(live_water, callback_data="cb_live")]]
        buttons += [[InlineKeyboardButton(blue_light, callback_data="cb_blue")]]
        buttons += [[InlineKeyboardButton(radiation, callback_data="radiation")]]
        buttons += [[InlineKeyboardButton(crystal, callback_data="cb_crystal")]]
        buttons += [[InlineKeyboardButton(air_cleaner, callback_data="cb_cleaner")]]
        buttons += [[InlineKeyboardButton(silver_water, callback_data="cb_silver")]]
        buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
        buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
        products_keyboard = list(buttons)
        reply_markup_products = InlineKeyboardMarkup(products_keyboard)

        query.edit_message_text(message, reply_markup=reply_markup_products, parse_mode="markdown")
