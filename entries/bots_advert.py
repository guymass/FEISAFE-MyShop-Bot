
from lib import deco
from lib.database import db
from emoji import emojize
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern="cb_bots")
def bots_advert(update, context):
    query = update.callback_query
    message = emojize("🦁 בוט לניהול ואבטחת קבוצות " \
            "🦁 בוט לניהול הזמנת מוצרים " \
            "🦁 בוט מיני אתר\חנות " \
            "🦁 הדרכה - פיתוח בוטים " \
            "🦁 בוטים לניהול מאגרי מידע " \
            "🦁  צאט בוטים לכל מטרה! " \
            "🦁 צרו עמי קשר " \
            "@FlatEarthBob")
    query.message.reply_text(message)