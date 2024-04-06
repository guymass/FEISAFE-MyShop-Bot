import logging
from settings import admin_list
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)
from telegram.ext.dispatcher import run_async
from functools import wraps

logger = logging.getLogger(__name__)

def log(func):
    logger.info(func.__name__)
###########################################################################

entry_points = []
def conversation_command_handler(cmd, **kwargs):
    def wrap_conversation_command_handler(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)
        entry_points.append(CommandHandler(cmd, wrapped, **kwargs))
        return wrapped
    return wrap_conversation_command_handler

def conversation_message_handler(filters, **kwargs):
    def wrap_conversation_message_handler(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)
        entry_points.append(MessageHandler(filters, wrapped, **kwargs))
        return wrapped
    return wrap_conversation_message_handler

###########################################################################

entry_states = {}
def register_state_callback(key, **kwargs):
    def wrap_register_state_callback(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)
        val = CallbackQueryHandler(wrapped, **kwargs)
        if key in entry_states:
            entry_states[key].append(val)
        else:
            entry_states[key] = [val]        
        return wrapped
    return wrap_register_state_callback

def register_state_message(key, filters, **kwargs):
    def wrap_register_state_message(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)        
        val = MessageHandler(filters, wrapped, **kwargs)
        if key in entry_states:
            entry_states[key].append(val)
        else:
            entry_states[key] = [val]        
        return wrapped
    return wrap_register_state_message

###########################################################################

entry_fallbacks = []
def fallback_handler(**kwargs):
    def wrap_fallback_handler(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)         
        entry_fallbacks.append(CallbackQueryHandler(wrapped, **kwargs))
        return wrapped
    return wrap_fallback_handler

###########################################################################

global_dispatchers = []
def global_command_handler(cmd):
    def wrap_global_command_handler(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)        
        global_dispatchers.append(CommandHandler(cmd, wrapped))
        return wrapped
    return wrap_global_command_handler

def global_message_handler(filters, **kwargs):
    def wrap_global_message_handler(func):
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)        
        global_dispatchers.append(MessageHandler(filters, wrapped, **kwargs))
        return wrapped
    return wrap_global_message_handler

def global_callback_handler(**kwargs):
    def wrap_global_callback_handler(func):
        default = {'pass_user_data':True, 'pass_chat_data':True,'pass_update_queue':True}
        @wraps(func)
        def wrapped (*a, **bb):
            log(func)
            return func(*a, **bb)
        global_dispatchers.append(CallbackQueryHandler(wrapped, **{**default,**kwargs}))
        return wrapped
    return wrap_global_callback_handler

###########################################################################

def restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_message.from_user.id
        user_name = update.effective_message.from_user.username
        print(user_id)
        print(user_name)
        if user_id not in admin_list:
            query = update.callback_query
            print("גישה חסומה עבורכם. {}.".format(user_id))
            query.edit_message_text('משתמש לא מאושר לשימוש בפקודה זו!')
            return  # quit function
        return func(update, context, *args, **kwargs)
    return wrapped
