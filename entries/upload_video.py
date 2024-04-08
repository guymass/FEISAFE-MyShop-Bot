from telegram.utils import helpers
from telegram.ext import Filters
from emoji import emojize
from lib import (deco, common)
from lib.database import db
import datetime
from lib.common import randStr
from time import sleep
from entries.mainmenu import mainmenu
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_message_handler(Filters.document.category("video/mp4") | Filters.document.category("video") | Filters.video)
def upload_video(update, context):
    #query = update.callback_query

    message = update.message.chat.type
    #pprint(message)


    m = update.message
    if m.video:
        file_id = m.video.file_id
        document = "video/mp4"
    elif m.document:
        if m.document.mime_type == 'video/mp4':
            file_id = m.document.file_id
            document = "document"
    
    print("DOCUMENT TYPE >>>>>>> " + str(document))
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    first_name = update.effective_message.from_user.first_name
    last_name = update.effective_message.from_user.last_name

    fullname = str(first_name) +' '+ str(last_name)

    upload_date = update.effective_message.date
    msg_id = update.effective_message.message_id
    message_types = ['document', 'video', 'video/mp4']
    text = update.effective_message.caption

    """cursor = db.videos.find({})
    for vid in cursor:
        if vid['VideoId'] == file_id:
            update.message.reply_text("הסרטון הזה כבר קיים במערכת, אנא העלו סרטון חדש.")
        else:

            pass"""

    if username != 0 and fullname !=0:

        if document in message_types:
            #file_id = update.message.video.file_id

            current_time = datetime.datetime.utcnow()

            m = update.message
            if document == 'video/mp4':
                file_id = m.video.file_id
            elif document == 'document':
                file_id = m.document.file_id
            print("FILE-ID >>>>> " + str(file_id))

            userId = str(user_id)
            date = str(upload_date)
            vidId = str(file_id)
            cap = str(text)
            video_owner = str(username)
            randomNum = randStr(N=10)
            video_code = str(userId+randomNum)
            video_item = {
                "Owner":username,
                "FileType":document,
                "UserId":user_id,
                "VideoId":vidId,
                "VideoText":cap,
                "VideoCode":video_code,
                "UploadDate":upload_date,
                "Category":"category",
                "MenuCb":"cb",
                "Price":0.0,
                "Quantity":0,
                "Width":0.0,
                "Length":0.0,
                "Height":0.0,
                "Weight":0.0,
                "Color":"color",
                "State":"used",
                "Status":"pending"

            }
            db.videos.insert_one(video_item)

            video_details = emojize("\U0000200F  \U0001F505 תאריך פרסום: \U0001F505"+str(upload_date)+"\n"
                                    +"Post Code: "+str(video_code)+"\n\n"+"Status: Waiting for approval"+"\n\n\U0001F505  \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505\n\n")
            video_details += cap + "\n\n\U0001F505  \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505\n\n"

            if document == 'video/mp4':

                context.bot.send_video(chat_id, video=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "עותק זה נשלח על ידי הבוט בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_video(user_id, video=file_id, caption=video_details, parse_mode='HTML')
            elif document == 'document':
                context.bot.send_document(chat_id, document=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "עותק זה נשלח על ידי הבוט בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_document(user_id, document=file_id, caption=video_details, parse_mode='HTML')

            context.bot.send_message(chat_id, "הפוסט שלכם נשמר בהצלחה ויופיע במאגר החיפוש החל מהיום.\n שמרו את פרטי המודעה ובפרט את קוד המודעה שהונפק עבורה, רק איתה תוכלו לנהל את הפרסומים שלכם לבוט.\nעל מודעות שנענו ונמכרו, על אחריות המוכר לשלוח את פקודת ההסרה.\nמודעות מעל חודש יוסרו מהרשימה באופן אוטומטי אלא אם כן נשלחה פקודת חידוש.")
            pass
        else:
            context.bot.send_message(chat_id, text="משהו קרה והקובץ לא נשמר, נסו שנית.")
            pass
    else:
        context.bot.send_message("אנא וודאו שיש לכם לפחות שם משתמש רשום שאוכל להשתמש בו לרישום המודעות שלכם.\n וודאו שכל השדות בפרופיל שלכם בטלאגרם מלאים עם שם לזיהוי במערכת שלנו.\n תוכלו לחזור ולנסות שנית בכל עת שתרצו, תודה שהייתם אצלנו, להתראות.")
        pass    
    update.message.reply_text("הצאט יתנקה תוך שניות ספורות, אנא שמרו את קוד המודעה.\nחשוב מאוד לא לאבד אותו, זכרו! ללא הקוד לא תוכלו לנהל את המודעה.")

    sleep(3)

    mainmenu(update, context)