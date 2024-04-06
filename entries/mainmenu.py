from emoji import emojize
from telegram.ext import (ConversationHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (deco)
import logging

logger = logging.getLogger(__name__)


@deco.run_async
@deco.global_callback_handler(pattern='cb_back')
def mainmenu(update, context):
    chat_id = update.effective_chat.id
    message = "\U0000200F\U0001F3C1      תפריט ראשי      \U0001F3C1"
    search = emojize("\U0000200F\U0001F50D     חיפוש     \U0001F50D")
    cancel = emojize("\U0000200F\U0000274c     ביטול     \U0000274c")
    create = emojize("\U0000200F\U0001F4F0     צור מודעה     \U0001F4F0")
    posts = emojize("\U0000200F\U0001F440     המודעות שלי     \U0001F440")
    categories = emojize("\U0000200F \U0001F3F7     קטגוריות לשיוך מודעה     \U0001F3F7")
    set_cat = emojize("\U0000200F \U0001F516     שייך מודעה     \U0001F516")
    rules = emojize("\U0000200F \U0001F4F4     כללי שימוש     \U0001F4F4")
    privacy = emojize("\U0000200F \U0001F9B8     מדיניות הפרטיות     \U0001F9B8")
    support = emojize("\U0000200F \U0001F4BB     תמיכה טכנית     \U0001F4BB")
    help = emojize("\U0000200F \U00002753     עזרה     \U00002753")
    bots = emojize("\U0000200F \U0001F916     רוצים בוט משלכם?     \U0001F916")
    latest = emojize("\U0000200F \U0001F195     פרסומים חדשים     \U0001F195")

    buttons = [[InlineKeyboardButton(latest, callback_data="cb_latest")]]
    buttons += [[InlineKeyboardButton(search, callback_data="cb_search")]]
    buttons += [[InlineKeyboardButton(create, callback_data="cb_create")]]
    buttons += [[InlineKeyboardButton(posts, callback_data="cb_myposts")]]
    buttons += [[InlineKeyboardButton(categories, callback_data="cb_categories")]]
    buttons += [[InlineKeyboardButton(set_cat, callback_data="cb_get_post_id")]]
    buttons += [[InlineKeyboardButton(rules, callback_data="cb_rules")]]
    buttons += [[InlineKeyboardButton(privacy, callback_data="cb_privacy")]]
    buttons += [[InlineKeyboardButton(support, callback_data="cb_support")]]
    buttons += [[InlineKeyboardButton(bots, callback_data="cb_bots")]]
    buttons += [[InlineKeyboardButton(help, callback_data="cb_help")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    start_keyboard = list(buttons)
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    message,
    reply_markup=reply_markup_start
    )
    return ConversationHandler.END