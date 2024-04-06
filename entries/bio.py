from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from emoji import emojize
from lib import (common, deco)

import logging
logger = logging.getLogger(__name__)


#@deco.global_callback_handler("bio", pattern='^cb_bio$', pass_user_data=True, pass_chat_data=True)
@deco.run_async
@deco.global_callback_handler(pattern="cb_session")
def bio(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = ""
    if data == "cb_session":
        message += "*סדנת ביו האקינג*\n\n" \
        "דרך טבעית מבוססת מדע לבריאות אופטימלית ושגשוג בעולם המודרני\n\n" \
        "זוכרים כשהייתם ילדים, איך הסתובבתם ערומים? יחפים על האדמה? בשמש? לא היה לכם קר ולא מלוכלך, לא הפחידו אתכם עם סרטן העור ולא עם חול מה קרה מאז? העולם השתנה!!! הבורגנות והמודרניות כרסמו בבריאות ובביולוגיה שלנו והילדים שלנו ואנחנו משלמים מחיר כבד על כך.\n\n" \
        "ביו-האקינג = שימוש בנתוני הסביבה הטבעיים, על מנת לשפר את היכולת הביולוגית של האדם וע\"י כך לשפר את הבריאות, להפחית דלקות ומחלות ולהיות בבריאות אופטימלית.\n\n" \
        "*בבני יהודה, דרום רמת הגולן*\n זוהי הסדנא היחידה בישראל שנותנת מענה לכל קשת האתגרים, כמעט, שיש כיום בעולם המודרני. אנחנו ניגע בכל תחום שמשפיע ישירות על הביולוגיה שלכם. אור ותאורה, מים, מזון, מגנטיות, קרינה, המטען החשמלי של תאי הגוף והשדה האלקטרומגנטי שאנו חיים בו. הבריאות שלכם נמצאת בתשתית הפיסיקלית הנכונה לגוף שלכם.\n\n" \
        "זהו סופ\"ש של שגשוג והעלאת רמת האנרגיה הפיזית, הרגשית והמנטלית שלכם ושל המשפחה\n\n" \
        "זוהי סדנא ייחודית, שתיתן לכם כלים אמיתיים לקחת לחיי היומיום ולהעביר את הידע והכלים הללו לדורות הבאים.\n\n" \
        "*חשוב לדעת:*\n\n זוהי סדנא אינטימית (עד 10 משתתפים!!) באווירה ביתית מועבר בה ידע נדיר, שנשאר איתכם לעד. לינה משותפת באוהל טבילה בבריכת מים חיים טבילה במעיין ארוחות נקיות ומפנקות בתדר גבוה קרקוע בהייה בשמש ואיך אפשר בלי טעימה מצלילי קערות הקריסטל\n\n" \
        "עלות הסדנא במחיר מיוחד\nלרוכשים הראשונים לעונה 1,848 ש\"ח בלבד (או בשישה תשלומים של 308 ש\"ח) * קוד הנחה לזוגות (200 שח): zoog200 * עלות התכנית כוללת רשימת הבונוסים המופיעה למטה\n\n" \
        " להצתרפות לסדנא ולהרשמה מהירה בחרו את אחת האפשרויות ועקבו אחר ההוראות עד קבלת אישור ההזמנה. אנו מקווים לראותכם איתנו בקרוב.\n\n"

        date1= emojize("\U00002196 להתצרפות לסדנא בתאריך:")
        date2 = emojize("\U00002196 להתצרפות לסדנא בתאריך:")
        date3 = emojize("\U00002196 להתצרפות לסדנא בתאריך:")
        back = emojize("\U000021AA חזרה")
        cancel = emojize("\U0000274c ביטול")

        buttons = [[InlineKeyboardButton(date1, callback_data="cb_date1")]]
        buttons += [[InlineKeyboardButton(date2, callback_data="cb_date2")]]
        buttons += [[InlineKeyboardButton(date3, callback_data="cb_date3")]]
        buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
        buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
        bio_keyboard = list(buttons)
        reply_markup_bio = InlineKeyboardMarkup(bio_keyboard)

        query.edit_message_text(message, reply_markup=reply_markup_bio, parse_mode="markdown")