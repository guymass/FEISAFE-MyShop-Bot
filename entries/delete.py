import os
from lib import deco

@deco.run_async
@deco.global_command_handler("delete")
def delete(update, context):
    # TODO: check file 
    filePath = '/root/botwo/botwo.txt'
    if os.path.exists(filePath):
        os.remove(filePath)
        print("Conversation Deleted!")
    else:
        print("Can not delete the file as it doesn't exists")