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
from lib import (deco, states)

#
# UserWarning: If 'per_message=True', all entry points and state handlers must be 'CallbackQueryHandler', since no other handlers have a message context.

logger = logging.getLogger(__name__)

username = urllib.parse.quote_plus('')
password = urllib.parse.quote_plus('')
client = MongoClient('mongodb://%s:%s@127.0.0.1:17474/' % (username, password), unicode_decode_error_handler='ignore')

db = client.bowto
db_buttons = db['buttons']

def admin_menu(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    data = query.data
    message = "\U0001F3C1 תפריט אדמין \U0001F3C1"
    pending_posts = "ממתינים לאישור"
    manage_categories = "ניהול קטגוריות"
    manage_users = "ניהול משתמשים"
    analytics = "ניתוח נתונים"
    
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
        [InlineKeyboardButton("מחיקת קטגוריה", callback_data="cb_delete_category")],
        [InlineKeyboardButton("הוספת קטגוריה", callback_data="cb_add_category")],
        [InlineKeyboardButton("חזרה לתפריט קודם", callback_data="cb_admin_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Edit the message to display the manage categories menu
    query.edit_message_text(text=text, reply_markup=reply_markup)


def delete_category(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Ask the user for the category name
    context.bot.send_message(chat_id, text="בבקשה שלח את שם הקטגוריה שברצונך למחוק, או לחץ על 'ביטול' לחזרה לתפריט הקטגוריות:",
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול", callback_data="cb_cancel_delete")]]))
    
    # Set the state to "waiting_for_category_name"
    context.user_data['state'] = 'waiting_for_category_name'




def cancel_delete(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Send a message indicating cancellation
    context.bot.send_message(chat_id, text="פעולת מחיקת הקטגוריה בוטלה.")
    
    # Return to the manage categories menu
    manage_categories(update, context)


def add_category(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Ask the user for the category name
    context.bot.send_message(chat_id, text="בבקשה שלח את שם הקטגוריה שברצונך להוסיף:")
    
    # Set the state to WAITING_FOR_CATEGORY_NAME
    context.user_data['state'] = "WAITING_FOR_CATEGORY"
    return states.WAITING_FOR_CATEGORY

@deco.register_state_message(states.WAITING_FOR_CATEGORY, Filters.text, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def handle_new_category_name(update, context):
    chat_id = update.message.chat_id
    new_category_name = update.message.text

    try:
        # Check if the category name already exists
        cursor = db_buttons.find_one({"ButtonName": new_category_name})
        if cursor:
            context.bot.send_message(chat_id, text=f"הקטגוריה '{new_category_name}' כבר קיימת.")
        else:
            # Insert the new category into the buttons collection
            db_buttons.insert_one({"ButtonName": new_category_name, "ButtonCb": new_category_name.lower()})
            
            # Send a confirmation message
            context.bot.send_message(chat_id, text=f"הקטגוריה '{new_category_name}' נוספה בהצלחה!")
        
        # Return to the manage categories menu
        manage_categories(update, context)
        return ConversationHandler.END
    except Exception as e:
        # Handle any exceptions and log the error
        context.bot.send_message(chat_id, text="An error occurred while adding the category.")
        context.bot.send_message(chat_id, text=str(e))  # Send error message
        logger.error(f"Error adding category: {e}")

        # Return to the manage categories menu
        return ConversationHandler.END

# Create ConversationHandler

def fallback(update, context):
    update.message.reply_text("Sorry, I didn't understand that. Please try again.")


def cancel_add(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    # Send a message indicating cancellation
    context.bot.send_message(chat_id, text="פעולת הוספת הקטגוריה בוטלה.")
    
    # Return to the manage categories menu
    manage_categories(update, context)


def back_to_main_menu(update, context):
    # Call the main menu function to display the main menu
    admin_menu(update, context)


