import logging
from telegram import (ParseMode)
from telegram.ext import (Defaults, Updater, PicklePersistence, ConversationHandler)
from lib import deco
from settings import CHATID, token, timeout, pickle_logs
from entries import *
from states import *
from exits import cancel
from time import sleep

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    #persistance = init_persistance()
    pp = PicklePersistence(filename=pickle_logs, store_user_data=True, store_chat_data=True, single_file=False)
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(token, persistence=pp, use_context=True, defaults=defaults, request_kwargs={'read_timeout': timeout, 'connect_timeout': timeout})

    """SELF_CHAT_ID = f'@{updater.bot.get_me().username}'
    logger.info(f'SELF_CHAT_ID {SELF_CHAT_ID}')
    logger.info(f'CHATID {CHATID}')"""

    conversation_handler = ConversationHandler(
        entry_points=deco.entry_points,
        states=deco.entry_states,
        fallbacks=deco.entry_fallbacks,
        name="order",
        persistent=True,
        allow_reentry=True,
        per_user=True,
        per_chat=True,
        # per_message=True
    )

    updater.dispatcher.add_handler(conversation_handler)
    for dispatcher in deco.global_dispatchers:
        updater.dispatcher.add_handler(dispatcher)

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
