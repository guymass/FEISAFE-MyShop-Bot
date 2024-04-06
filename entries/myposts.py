from lib import deco
from lib.database import db
from emoji import emojize
from time import sleep
from entries.mainmenu import mainmenu
from settings import CHATID
import logging
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern="^cb_myposts$")
def myposts(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    query.edit_message_text("מביא את רשימת המודעות שלך, אנא המתן...\n")
    user_id = update.callback_query.from_user.id
    cursor = db.videos.find({})
    print(user_id)
    for item in cursor:
        if item['UserId'] == user_id:
            print("foudn match!!!!!!")
            owner = str(item['Owner'])
            video_id = str(item['VideoId'])
            video_text = str(item['VideoText'])
            video_code = str(item['VideoCode'])
            date = str(item['UploadDate'])
            cat = str(item['Category'])
            state = str(item['State'])
            status = str(item['Status'])
            file_type = str(item['FileType'])

            message = emojize("\U0000200F \U0001F505 פרטי המוצר: \U0001F505"+"\n\n"+"קוד מודעה: "+video_code+"\n"+"הועלה בתאריך: "+date+"\n"+"קטגוריה: "+cat+"\n"+"סטטוס מודעה: "+status+"\n\n"+video_text + "\n\U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505 \U0001F505")

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id, video=video_id, caption=message, parse_mode='HTML')
            elif file_type == 'document':
                context.bot.send_document(chat_id, document=video_id, caption=message, parse_mode='HTML')
        else:
            query.edit_message_text("לא נמצאו מודעות שפרסמתם! או שקוד המודעה אינו משוייך אליכם.\n אנא בדקו שרשמתם את קוד המודעה המתאים ושהמודעה משוייכת לחשבון ממנו אתם מחוברים.")
    sleep(3)
    mainmenu(update,context)
