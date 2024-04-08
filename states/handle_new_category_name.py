from telegram.ext import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lib import (deco, states)
from lib.database import db

@deco.register_state_message(states.WAITING_FOR_CATEGORY, Filters.text, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def handle_new_category_name(update, context):
    context.bot.send_message(chat_id, text=f"Trying to add a category now!\n")
    try:
        chat_id = update.effective_chat.id
        new_category_name = update.message.text
        
        if new_category_name.lower() == 'cancel':
            # Cancel the operation and return to the manage categories menu
            context.bot.send_message(chat_id, text="הוספת הקטגוריה בוטלה.")
            manage_categories(update, context)
            return ConversationHandler.END
        
        # Check if the category name already exists
        cursor = db_buttons.find_one({"ButtonName": new_category_name})
        if cursor:
            context.bot.send_message(chat_id, text=f"הקטגוריה '{new_category_name}' כבר קיימת.")
        else:
            # Insert the new category into the buttons collection
            db_buttons.insert_one({"ButtonName": new_category_name, "ButtonCb": new_category_name.lower()})
            
            # Send a confirmation message
            context.bot.send_message(chat_id, text=f"הקטגוריה '{new_category_name}' נוספה בהצלחה!")
        
        # Update the state if needed
        context.user_data['state'] = states.CATEGORY_ADDED
        return states.CATEGORY_ADDED 

    except Exception as e:
        logger.error(f"Error in handle_new_category_name: {e}")
        context.bot.send_message(chat_id, text="אירעה שגיאה במהלך הוספת הקטגוריה.")
        return states.WAITING_FOR_CATEGORY