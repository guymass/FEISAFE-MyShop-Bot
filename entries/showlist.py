from lib import deco
from lib.database import db
import logging
from emoji import emojize
from time import sleep
from entries.uvexmenu import uvexmenu
logger = logging.getLogger(__name__)

cbs = "uvexround|uvexsq|uvexlow|redlight|iristech|raoptics"
@deco.run_async
@deco.global_callback_handler(pattern='^screen$')
@deco.global_callback_handler(pattern=f'^cb_({cbs})$')
@deco.conversation_command_handler("showlist")
def showlist(update, context):
    chat_id = update.effective_chat.id
    result = db.videos.find({})

    for r in result:
        if r['Status'] == "pending":

            owner = r['Owner']
            file_type = r['FileType']
            vidId = r['VideoId']
            vidCap = r['VideoText']
            uploaded_date = r['UploadDate']
            category = r['Category']
            state = r['State']

            message = emojize("משיוך אל: @"+str(owner)+"\nפרטי המודעה:\n"+str(vidCap)+"\nתאריך פרסום: "+str(uploaded_date)+"\nקטגוריה: "+str(category)+"\nמצב הפריט: "+str(state)+"\n")

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id=chat_id, video=vidId, caption=message)
            elif file_type == 'document':
                context.bot.send_document(chat_id=chat_id, document=vidId, caption=message)

            sleep(1)
    sleep(3)
    mainmenu(update,context)