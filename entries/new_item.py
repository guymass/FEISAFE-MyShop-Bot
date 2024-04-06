from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from lib import deco
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='^cb_create$')
def new_item(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    #query.edit_message_text(data)

    main_message = emojize("\U0000200F יופי \U0001F63A אני אשמח לקבל פריט חדש, בואו נתחיל.\n כל שעליכם לעשות הוא לשלוח לי סרטונים קצרים של הפריטים וכתבו בהודעה את כל הפרטים הרלוונטים\nכולל מחיר, מחיר משלוח אם קיים וכל  פרט חשוב.\nאתם יכולים להשתמש באימוג'ים ובכיתוב <b>להדגשת טקסט</b>.\nאנא וודאו כי צילמתם סרטון איכותי וקחו את הזמן לצלם לפחות 20 שניות.'")

    new_item_keyboard = emojize("פריט חדש")
    search = emojize("חיפוש")
    cancel = emojize("ביטול")

    replay_markup_keyboard = [[InlineKeyboardButton("חזרה", callback_data="cb_back"),
                                InlineKeyboardButton("ביטול", callback_data=str("cancel"))
                                ]]

    markup_keyboard = InlineKeyboardMarkup(replay_markup_keyboard)
    query.edit_message_text(str(main_message), reply_markup=markup_keyboard)