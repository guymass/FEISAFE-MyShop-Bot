from lib import deco
from emoji import emojize
from time import sleep
from entries.mainmenu import mainmenu
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.restricted
@deco.global_command_handler("admin")
def admin(update, context):
    chat_id = update.effective_chat.id
    msg = emojize("\U0000200F  \U0001F505 להלן רשימת הפקודות של הבוט \U0001F505 \n\n" +
                                "להתחלת הזמנה הקלידו /start\n" +
                                "לביטול הזמנה לחצו על סיום ללא הקלדת נתונים או כתבו /cancel - סיום או Done\n" +
                                "רק לאחר שמלאתם את כל הנתונים לחיצה על סיום תשלח הזמנה.\n" +
                                "לצפייה בהזמנות במצב המתנה כתבו את הפקודה /getlist\n" +
                                "לסגירת ההזמנה סיום המשלוח יש לכתוב את פקודת /setitem והמספר הטלפון של המזמין\n פקודה זו תעדכן את מצב ההזמנה - ל- Delivered\n" +
                                "לקבלת עדכון מצב של כל ההזמנות שבוצעו יחד עם סך כולל יש לכתוב /total\n" +
                                "עלמנת לעדכן תמונות מוצר חדשים לבוט יש פשוט להעלות תמונה לבוט והוא יארגן אותן במקום \n\n כאשר רוצים להחליף תמונות יש לרשום פקודת /clear שתמחוק את התמונות הישנות.\n" +
                                "עלמנת לעדכן תמונת פתיחה\לוגו יש לשלוח תמונה עם הכיתוב logo בלבד"
                                "עלמנת לראות שוב את הודעת העזרה כתבו /help")
    context.bot.send_message(chat_id=chat_id, text=msg)
    sleep(1)
    print(msg)
    mainmenu(update,context)