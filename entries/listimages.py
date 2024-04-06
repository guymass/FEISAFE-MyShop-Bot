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
@deco.global_message_handler(Filters.photo)
@deco.conversation_message_handler(Filters.photo)
@deco.conversation_message_handler(
    Filters.document.category("video/mp4") | Filters.document.category("video") | Filters.video, pass_user_data=True, pass_chat_data=True, pass_update_queue=True)
def listimages(update, context):

    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id
    message_types = ['photo', 'video', 'video/mp4', 'document', 'animation']
    upload_date = update.effective_message.date
    caption = update.message.caption
    username = update.effective_message.from_user.username
    first_name = update.effective_message.from_user.first_name
    last_name = update.effective_message.from_user.last_name
    fullname = str(first_name) + " " + str(last_name)


    """mt = helpers.effective_message_type(update.message)
    #mt = update.message
    
    if mt in message_types and mt != "":
        print("MESSAGE TYPE >>>>>: " + str(mt))
    else:
        print("MEESAGE Type Is not in list")"""
    #print("MT >>>>>>>>" + str(mt))
    media = []
    userId = str(user_id)
    date = str(upload_date)
    cap = str(caption)
    image_code = ''
    m = update.message
    document = ''
    file_id = ''
    m = update.message
    if m.video:
        file_id = m.video.file_id
        document = "video/mp4"
    elif m.document:
        if m.document.mime_type == 'video/mp4':
            file_id = m.document.file_id
            document = "document"
    
    
    if username != "" and user_id !="":
        
        print("USERNAME >>>>> " + str(username))
        print("FULLNAME >>>>> " + str(fullname))
        print("USER_ID >>>>> " + str(user_id))
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

            video_details = emojize("\U0000200F  \U0001F505 תאריך פרסום: \U0001F505\n"+str(upload_date)+"\n"
                                    +"קוד מודעה: "+str(video_code)+"\n\n\U0001F505  \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505\n\n")
            video_details += cap + "\n\n\U0001F505  \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505\n\n"

            if document == 'video/mp4':

                context.bot.send_video(chat_id, video=file_id, caption=video_details)
                user_msg = "עותק זה נשלח על ידי הבוט בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_video(user_id, video=file_id, caption=video_details, parse_mode='HTML')
            elif document == 'document' or document == 'animation':
                context.bot.send_document(chat_id, document=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "עותק זה נשלח על ידי הבוט בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_document(user_id, document=file_id, caption=video_details, parse_mode='HTML')
            user_msg += "\n\nהפוסט שלכם נשמר בהצלחה ויופיע במאגר החיפוש החל מהיום.\n\n שמרו את פרטי המודעה ובפרט את קוד המודעה שהונפק עבורה, רק איתה תוכל לנהל את הפרסומים שלכם לבוט.\nעל מודעות שנענו ונמכרו, על אחריות המוכר לשלוח את פקודת ההסרה.\nמודעות מעל חודש יוסרו מהרשימה באופן אוטומטי אלא אם כן נשלחה פקודת חידוש."
            context.bot.send_message(chat_id, user_msg)
            pass
        else:
            context.bot.send_message(chat_id, text="משהו קרה והקובץ לא נשמר, נסו שנית.")
            print(document)
            pass
    else:
        context.bot.send_message("אנא וודאו שיש לכם לפחות שם משתמש רשום שאוכל להשתמש בו לרישום המודעות שלכם.\n וודאו שכל השדות בפרופיל שלכם בטלאגרם מלאים עם שם לזיהוי במערכת שלנו.\n תוכלו לחזור ולנסות שנית בכל עת שתרצו, תודה שהייתם אצלנו, להתראות.")
        pass    
    #update.message.reply_text("הצאט יתנקה תוך שניות ספורות, אנא שמרו את קוד המודעה.\nחשוב מאוד לא לאבד אותו, זכרו! ללא הקוד לא תוכלו לנהל את המודעה.")

    sleep(3)

    mainmenu(update, context)

    if caption == "logo":
        res = db.logo.delete_many({})
        update.message.reply_text(" תמונת לוגו התקבלה!")
        file_id = update.message.photo[0].file_id
        current_time = datetime.datetime.utcnow()
        context.bot.send_message(chat_id, str(upload_date))
        context.bot.send_message(chat_id, file_id)
        context.bot.send_photo(chat_id, file_id)
        context.bot.send_message(chat_id, str(caption))

        cursor = db.images.find({})
        for img in cursor:
            if img['PhotoCode'] == "logo":
                res = db.logo.delete_many({})
                pass
            elif db.images.count() == 0:
                image_code = "logo"

        image_code = "logo"
        image_type = str(document)
        userId = str(user_id)
        date = str(upload_date)
        imgId = str(file_id)
        cap = str(caption)
        imageItem = {
            "UserId": user_id,
            "PhotoId": imgId,
            "ImageText": cap,
            "FileType": image_type,
            "PhotoCode": image_code,
            "ImageDate": date

        }
        db.logo.insert_one(imageItem)
        context.bot.send_message(chat_id, text="\U0000200F תמונת לוגו התעדכנה!")

