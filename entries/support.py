from lib import deco
import logging
from emoji import emojize
logger = logging.getLogger(__name__)

@deco.run_async
@deco.global_callback_handler(pattern='cb_support')
def support(update, context, *args, **kwargs):
    query = update.callback_query
    chat_id = update.effective_chat.id
    #context.answer_callbak_query(update.callback_query.id)
    data = query.data

    if data == "cb_support":
        context.bot.send_message(chat_id, text='https://t.me/feisupport')
    else:
        context.bot.send_message(chat_id, text='https://t.me/feisupport')