from lib import deco
from lib.database import db
from emoji import emojize
import logging
from entries.welcome import welcome

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResult, InlineQuery)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                         ConversationHandler, CallbackQueryHandler, PicklePersistence, Defaults)
from telegram.ext import CallbackContext
import urllib.parse
import pymongo
from mongoengine import *
from pymongo import MongoClient
import logging
from telegram.ext import ConversationHandler, CallbackQueryHandler
from settings import admin_list
#from lib.deco import *
#import lib.states
#from lib.states import *

from lib import (common, deco, states)
from lib.database import db

#cbs = "add_category|handle_new_category_name|category_added"

logger = logging.getLogger(__name__)

username = urllib.parse.quote_plus('guy')
password = urllib.parse.quote_plus('OVc8EBd@guy!')
client = MongoClient('mongodb://%s:%s@127.0.0.1:17474/' % (username, password), unicode_decode_error_handler='ignore')

db = client.bowto
db_buttons = db['buttons']

def admin_menu(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    data = query.data
    message = "\U0001F3C1 Admin Menu \U0001F3C1"
    pending_posts = "Pending Posts Approval"
    manage_categories = "Manage Categories"
    manage_users = "Manage Users"
    analytics = "Analytics"
    
    # Define buttons for each admin option
    buttons = [
        [InlineKeyboardButton(pending_posts, callback_data="cb_pending_posts")],
        [InlineKeyboardButton(manage_categories, callback_data="cb_manage_categories")],
        [InlineKeyboardButton(manage_users, callback_data="cb_manage_users")],
        [InlineKeyboardButton(analytics, callback_data="cb_analytics")],
        [InlineKeyboardButton("חזרה", callback_data="cb_main_menu")]
    ]
    
    admin_keyboard = InlineKeyboardMarkup(buttons)
    
    query.edit_message_text(
        message,
        reply_markup=admin_keyboard,
        timeout=60
    )


def manage_categories(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Text for the manage categories menu
    text = "ניהול קטגוריות\n\nבחר פעולה:"
    
    # Define buttons for manage categories menu
    buttons = [
        [InlineKeyboardButton("Remove Category", callback_data="cb_delete_category")],
        [InlineKeyboardButton("Add New Category", callback_data="cb_add_category")],
        [InlineKeyboardButton("Previous Menu", callback_data="cb_admin_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Edit the message to display the manage categories menu
    query.edit_message_text(text=text, reply_markup=reply_markup)


def delete_category(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Ask the user for the category name
    context.bot.send_message(chat_id, text="בבקשה שלח את שם הקטגוריה שברצונך למחוק, או לחץ על 'ביטול' לחזרה לתפריט הקטגוריות:",
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="cb_cancel_delete")]]))
    
    # Set the state to "states.WAITING_FOR_CATEGORY_name"
    context.user_data['state'] = states.WAITING_FOR_CATEGORY


def handle_delete_category_name(update, context):
    chat_id = update.message.chat_id
    category_name = update.message.text
    
    # Check if the category name exists in the buttons collection
    cursor = db_buttons.find_one({"ButtonName": category_name})
    
    if cursor:
        # Remove the category from the buttons collection
        db_buttons.delete_one({"ButtonName": category_name})
        
        # Send a confirmation message
        context.bot.send_message(chat_id, text=f"קטגוריה '{category_name}' נמחקה בהצלחה!")
    else:
        # Send a message indicating that the category does not exist
        context.bot.send_message(chat_id, text=f"הקטגוריה '{category_name}' לא נמצאה.")

    # Return to the manage categories menu
    manage_categories(update, context)

def cancel_delete(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Send a message indicating cancellation
    context.bot.send_message(chat_id, text="פעולת מחיקת הקטגוריה בוטלה.")
    
    # Return to the manage categories menu
    manage_categories(update, context)


@deco.register_state_callback("add_category", pattern="^add_category$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def add_category(update, context):
    context.user_data['state'] = states.WAITING_FOR_CATEGORY
    #try:
    chat_id = update.effective_chat.id
    # Define the cancel button
    cancel_button = InlineKeyboardButton("cancel", callback_data="cb_cancel_add_category")
    
    # Create the message with the cancel button
    message_text = "בבקשה שלח את שם הקטגוריה שברצונך להוסיף או לחץ על 'ביטול' לביטול הפעולה:"
    reply_markup = InlineKeyboardMarkup([[cancel_button]])
    
    # Send the message with the cancel button
    context.bot.send_message(chat_id, text=message_text, reply_markup=reply_markup)
    
    # Set the state to states.WAITING_FOR_CATEGORY_NAME

    return states.WAITING_FOR_CATEGORY
    #except Exception as e:
    #    logger.error(f"Error in add_category: {e}")
    #    return ConversationHandler.END


@deco.register_state_callback("handle_new_category_name", pattern="^handle_new_category_name$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def handle_new_category_name(update, context):
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

@deco.register_state_callback("category_added", pattern="^category_added$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def category_added(update, context):
  update.message.reply_text("Category added!")
  manage_categories(update, context)
  return ConversationHandler.END

def fallback(update, context):
    update.message.reply_text("Sorry, I didn't understand that. Please try again.")

@deco.fallback_handler(pattern='^cb_cancel_add_category$')
def cancel_add_category(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Send a message indicating cancellation
    context.bot.send_message(chat_id, text="פעולת הוספת הקטגוריה בוטלה.")
    
    # Return to the manage categories menu
    manage_categories(update, context)
    return ConversationHandler.END



def back_to_main_menu(update, context):
    # Call the main menu function to display the main menu
    admin_menu(update, context)


# Create ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(add_category, pattern='^add_category$'), CommandHandler('add_category', add_category)],
    states={
        states.WAITING_FOR_CATEGORY: [CallbackQueryHandler(handle_new_category_name, pattern='^handle_new_category_name$')],
        states.CATEGORY_ADDED: [CallbackQueryHandler(category_added, pattern='^category_added$')],
    },
    fallbacks=[CallbackQueryHandler(cancel_add_category, pattern='^cb_cancel_add_category$')],
    allow_reentry=True,
    per_message=False
    )