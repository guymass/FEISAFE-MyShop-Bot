from lib import deco
from emoji import emojize
from time import sleep
from entries.mainmenu import mainmenu
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_command_handler("help")
@deco.global_callback_handler(pattern="cb_help")
def help(update, context):
    chat_id = update.effective_chat.id
    msg = emojize("\U0000200F  \U0001F505  להלן רשימת הפקודות של הבוט \U0001F505\n\n" +
                                "/start - על מנת לקבל את התפריט הראשי\n\n"+
                                "לביטול לחצו על ביטול\n\n" +
                                "/setcategory - לשיוך מודעתכם לאחת הקטגוריות. יש להוסיף את קוד המודעה שלכם + רווח ולהוסיף את שם הקטגוריה.\n\n" +
                                "/delete - למחיקת מודעה הוסיפו את קוד המודעה יחד עם פקודה זו. אתם יכולים למחוק רק הודעות שמשוייכות אל החשבון איתו יצרתם את המודעה.\n\n" +
                                "/help - על מנת לקבל את ההודעה הזו.\n\n"+
                                "** בקרוב סדרת פקודות נוספות לניהול וחיפוש **")
    context.bot.send_message(chat_id=chat_id, text=msg)
    sleep(1)
    mainmenu(update,context)
