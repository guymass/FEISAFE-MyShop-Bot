from lib import deco
from lib.database import db
from emoji import emojize
import logging
from settings import CHATID
from time import sleep
from entries.mainmenu import mainmenu
from pprint import pprint
logger = logging.getLogger(__name__)

@deco.restricted
@deco.run_async
@deco.global_callback_handler(pattern="^cb_latest$")
@deco.conversation_command_handler("getlist")
def getlist(update, context):
    chat_id = update.effective_chat.id
    result = db.videos.find({})
    val = ""
    for r in result:
        if r['Status'] == "pending":

            owner = r['Owner']
            ad_id = r['VideoCode']
            file_type = r['FileType']
            vidId = r['VideoId']
            vidCap = r['VideoText']
            uploaded_date = r['UploadDate']
            category = r['Category']
            state = r['State']
            status = r['Status']

            message = emojize("\U0000200F  \U0001F3F7 מצב מודעה: <b>" + status + "</b>\nקוד מודעה: <b>" + ad_id + "</b>\n\n👤<b> פורסם על ידי:</b> @"+str(owner)+"\nלהתחלת צאט עם המפרסם לחצו על הקישור.\n\n⬇<b> פרטי המודעה </b>⬇\n"+"🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀\n\n"+str(vidCap)+"\n\n📅<b> תאריך ושעת פרסום:</b> \n"+str(uploaded_date)+"\n\n🗃 <b>קטגוריה</b>: "+str(category)+"\n\n🟢 <b>מצב הפריט:</b> "+str(state)+"\n\n🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀\n")

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id=chat_id, video=vidId, caption=message)
            elif file_type == 'document':
                context.bot.send_document(chat_id=chat_id, document=vidId, caption=message)

            sleep(1)
    mainmenu(update, context)