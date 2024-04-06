from telegram.utils import helpers
from telegram.ext import Filters
from emoji import emojize
from lib import (deco, common)
from lib.database import db
import logging
import datetime
from lib.common import randStr
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_message_handler(Filters.photo)
def upload_photo(update, context):
    message = update.message.chat.type
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    first_name = update.effective_message.from_user.first_name
    last_name = update.effective_message.from_user.last_name
    fullname = str(first_name) +' '+ str(last_name)

    upload_date = update.effective_message.date
    msg_id = update.effective_message.message_id
    text = update.effective_message.caption

    m = update.message
    if m.photo:
        file_id = m.photo[0].file_id
        print(file_id)


    if username != "" and fullname != "":
        current_time = datetime.datetime.utcnow()

        userId = str(user_id)
        date = str(upload_date)
        photoId = str(file_id)
        cap = str(text)
        photo_owner = str(username)
        randomNum = randStr(N=10)
        photo_code = str(userId+randomNum)
        photo_item = {
            "Owner":photo_owner,
            "UserId":user_id,
            "PhotoId":photoId,
            "PhotoText":cap,
            "PhotoCode":photo_code,
            "UploadDate":upload_date,
            "Category":"category",
            "MenuCb":"cb",
            "Price":0.0,
            "Quantity":0,
            "Width":0.0,
            "Length":0.0,
            "Height":0.0,
            "Weight":0.0,
            "Color":"צבע",
            "State":"חדש",
            "Status":"ממתין"

        }
        db.images.insert_one(photo_item)

        photo_details = emojize("Upload Date: "+str(upload_date)+"\n"
                                +"File Owner: "+"@"+str(username)+"\n"
                                +"Photo Code: "+str(photo_code)+"\n"
                                +"Photo ID: "+str(photoId)+"\n----------------\n")

        photo_details += cap

        context.bot.send_photo(chat_id, photo=file_id, caption=photo_details, parse_mode='HTML')