from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lib import (common, deco, states)
from time import sleep

from entries.show_data import show_data

@deco.run_async
@deco.register_state_callback(states.SIXTH, pattern="^done$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def done(update, context):
    query = update.callback_query
    query.answer()
    category = context.user_data
    reply_text = "\U0000200F👩‍🌾 אלו הם פרטי ההזמנה שאושרו, אני יעדכן אותכם בקרוב , היו זמינים!\n" + "\n{}\n".format(common.facts_to_str(context.user_data))

    done_keyboard = []
    done_keyboard =  [[InlineKeyboardButton("נקה צ'אט'", callback_data="completed")]]
    done_keyboard = list(done_keyboard)
    reply_markup_done = InlineKeyboardMarkup(done_keyboard)
    if category != 0:
        show_data(update, context)
        #query.edit_message_text("מעולה! אלו הם פרטי ההזמנה עד כה: \n{} תודה שרכשתם אצלנו.".format(context.user_data), reply_markup=reply_markup_done)
    else:
        # TODO: error handling
        print(f'ERROR category is 0')
    sleep(1)
    #return ConversationHandler.END

