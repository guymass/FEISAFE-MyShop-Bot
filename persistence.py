import os
from telegram.ext import PicklePersistence
from settings import pickle_logs, CHATID

def init_persistance():
     if os.path.exists(pickle_logs):
         os.remove(pickle_logs)
     else:
         print("Good!!! - The file does not exist!")

     fei_persist = PicklePersistence(
         filename=pickle_logs,
         store_user_data=True, store_chat_data=True,
         single_file=True)
     fei_persist.flush()

     userData = fei_persist.get_user_data()
     chatData = fei_persist.get_chat_data()
     userConv = fei_persist.get_conversations(CHATID)

     uDataFile = open(r"log/userData.txt", "w")
     cDataFile = open(r"log/chatData.txt", "w")
     cnvDataFile = open(r"log/convData.txt", "w")

     uDataFile.write(str(userData))
     uDataFile.close()
     cDataFile.write(str(chatData))
     cDataFile.close()
     cnvDataFile.write(str(userConv))
     cnvDataFile.close()

    return PicklePersistence(filename=pickle_logs, store_user_data=True, store_chat_data=True, single_file=False)
