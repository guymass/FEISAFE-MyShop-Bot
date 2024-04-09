# FEISAFE-MyShop-Bot
A bot like craiglist that allows telegram users to create and manage items for sales, barters, giveaways and donations in a form of Videos and Images.


You should create a setting.py file at the root of the bot directory with the following information:


token = 'YourBotToken'
pickle_logs = "botwo.log" - You can change to any log name you wish.
timeout = 900

mongo_host = 'localhost' - can also be an IP. If you are using a different port just add :portnumber
#mongo_host = '178.162.220.42'
mongo_user = 'username'
mongo_password = 'password'
mongo_collection = 'botwo' -  ** You will require the mongo database to run this bot. Please PM me and I will send you an exported version.

admin_list = [list of telegram user ids seperated by commas]
CHATID = -100000000000 - Your Chat ID
