from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from emoji import emojize
from lib import deco
from lib.database import db
import logging


logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_command_handler('start')
def start(update, context):
    result = db.images.find_one_and_delete({"ImageText": "logo"})
    query = update.callback_query

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message_date = update.message.date
    message_id = update.message.message_id

    text = update.message.text

    item = {"UserId": user_id,
        "MessageId":message_id,
        "MessageText":text
    }

    if db.messages.count_documents({'MessageId': message_id}, limit=1) > 0:
        print("הודעה רשומה כבר!" + str(message_id))
        pass
    else:
        db.messages.insert_one(item)
        print("ההודעה נשמרה ;-)" + str(message_id))


    res = db.logo.find_one({"PhotoCode":"logo"})
    url = res['PhotoId']
    msg = "\U0000200F\n\U0001F981 שלום {} \n ברוכים הבאים אל בוט2, בוט שרות לסחר ישיר בין אנשים.".format(username) + "\n\n" \
    "\U0001F39E ראשית אני מעדיף לעבוד עם קבצי וידאו של MP4, אז קחו את הזמן ליצור את הסרטונים הכי יפים שלכם לפני שאתם שולחים לבוט\nאפשר להעלות איזה גודל שרוצים אבל עדיף סרטון קצר, קליט ומתומצת.\n\n" \
    "\U0001F4EE לעלות פוסט זה פשוט מאוד, לוחצים על צור מודעה והבוט יכנס למצב הקשבה להודעת המודעה שלכם עם הקובץ וידאו. \n\n" \
    "⚠ שימו לב! ברגע שההודעה שלכם עלתה הבוט יחזיר לכם עותק ביחד עם מספר מודעה ייחודי. תשמרו על קוד מודעה זה על מנת לנהל את המודעות שלכם. ⚠\n\n" \
    "\U00002049 מודעות עם תכנים מיניים, פוגעניים או כל סוג של מודעה שהמנהלים יחליטו שאינה מתאימה, תוסר לאלתר והמשתמש יקבל אזהרה. אנא עברו על כללי הבוט או כתבו /help.\n\n" \
    "\U0001F5FF מכיוון שטלאגרם הינה מערכת מוצפנת וחינמית, עדיין הבוט שפותח עבורה הוא שלנו. אנו מאפשרים שימוש חופשי במערכת זו ונמשיך לפתח אותה ככל שקהילת המשתמשים תגדל. דבר זה תלוי בזמן ומשאבים ולכן אנו נשתדל לתמוך במערכת ככל שנוכל. נשמח לראותכם כאן איתנו.\U0001F981"
    message = emojize(str(msg))
    user_full_details = emojize(str(user_id) + " - " + str(username))
    context.bot.send_photo(chat_id, url, message)
    #context.bot.send_message(583505750, user_full_details, parse_mode="HTML")
    user = update.effective_message.from_user

    logger.info("User %s started the conversation.", user.first_name)
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    message_date = update.effective_message.date
    msg_id = update.effective_message.message_id

    fullname = str(user.first_name) + " " +str(user.last_name)


    print(username)
    print(fullname)
    print(user_id)
    print(chat_id)
    print(msg_id)

    context.user_data['user_id'] = user_id
    context.user_data['fullname'] = fullname
    context.user_data['username'] = username
    context.user_data['start_message_id'] = msg_id
    #context.user_data['location'] = location
    details = context.user_data
    user_Mobile = ""
    user_location = ""
    reply_keyboard = []
    items = []

    tmp_product = {
            "UserId":user_id,
            "UserName": str(username),
            "FullName":str(fullname),
            "ProductText": "", #from button selection
            "Quantity":"", #from button selection
            "Mobile":"", #from button selection
            "Address":"", #from contact location optional!
            "Location":"",
            "Status":"Pending", # Dispatched/Delivered
            "Date":message_date
        }
    db.tmp_product.insert_one(tmp_product)

    reply_text = ""

    if context.user_data:
        reply_text += "\U0001F981 ברוכים השבים {}".format(username)
        #reply_text += message

    else:
        reply_text += message

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
    reply_text,
    reply_markup=reply_markup_start
    )

