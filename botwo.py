#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Bot2 - BoTwo was Developed by Guy Mass

import telegram
from telegram import *
import telegram.ext
from telegram import Chat, ChatAction, ChatMember, Message, MessageEntity
from telegram import utils
from telegram.utils import helpers
from telegram.ext.dispatcher import run_async
import json
from json_reader.decoder import iter_loads, JSONDecoder, PyJSONScanner
import pprint
from functools import wraps
#import fasttext
#model = fasttext.load_model('lid.176.ftz')
from bson.objectid import ObjectId
#import vlc
import pymongo
from mongoengine import *
from pymongo import MongoClient
import urllib.parse
from pprint import pprint
from bson.objectid import ObjectId

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResult, InlineQuery)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                         ConversationHandler, CallbackQueryHandler, PicklePersistence, Defaults)

import threading
from io import BytesIO
import requests
import datetime, time
from time import time, ctime, sleep
import string
import io
import os
import random
from random import choice
from string import ascii_uppercase
import re
import sys
import urllib
from emoji import emojize
from settings import (mongo_host, mongo_user, mongo_password, mongo_collection)
from entries.admin_functions import admin_menu, manage_categories, delete_category, add_category, back_to_main_menu, handle_category_name, cancel_delete, cancel_add_category
from entries.admin_functions import handle_new_category_name, conv_handler

from lib import deco
from lib.database import db
import states
import logging
from settings import admin_list
from lib.deco import *


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'

directory = '/uploads'

username = urllib.parse.quote_plus(mongo_user)
password = urllib.parse.quote_plus(mongo_password)
client = MongoClient('mongodb://%s:%s@127.0.0.1:17474/' % (username, password), unicode_decode_error_handler='ignore')
db = client.bowto

#admin_list = [583505750]
CHATID = -1001177209024


def restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):

        user_id = update.effective_message.from_user.id
        user_name = update.effective_message.from_user.username
        print(user_id)
        print(user_name)
        if user_id not in admin_list:
            print("גישה חסומה עבורכם. {}.".format(user_id))
            query.edit_message_text('משתמש לא מאושר לשימוש בפקודה זו!')
            return  # quit function
        return func(update, context, *args, **kwargs)
    return wrapped

@restricted
def shutdown():
    updater.stop()
    updater.is_idle = False
@restricted
def stop(update, context):
    #threading.Thread(target=shutdown).start()
    #os.kill(os.getpid(), signal.SIGINT)
    os.system('kill %d' % os.getpid())


# define the MONGO collections ##############################################
# client['your_database']
db_images = db['images']
db_categories = db['categories']
db_tmp_product = db['tmp_product']
db_products = db['products']
db_messages = db['messages']
db_buttons = db['buttons']
db_logo = db['logo']
db_videos = db['videos']

@restricted
def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

@restricted
def rebot(update, context):
    update.message.reply_text('מאתחל את הבוט עכשיו אנא המתן...')
    Thread(target=stop_and_restart).start()
    sleep(20)
    update.message.reply_text('הבוט אותחל!')


#####################################################################################################
#####################################################################################################
#####################################################################################################

start_msg_id = range(1)
START, FIRST, SECOND, RESTART = range(4)
name_keyboard = [['שם מלא', 'ביטול']]
name_markup = InlineKeyboardButton(name_keyboard, one_time_keyboard=True)

mobile_keyboard = [['נייד', 'ביטול']]
mobile_markup = InlineKeyboardButton(mobile_keyboard, one_time_keyboard=True)

address_keyboard = [['כתובת', 'ביטול']]
address_markup = InlineKeyboardButton(address_keyboard, one_time_keyboard=True)

done_keyboard = [['סיום', 'ביטול']]
done_markup = InlineKeyboardButton(done_keyboard, one_time_keyboard=True)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))


def bots_advert(update, context):
    query = update.callback_query
    message = "🦁 בוט לניהול ואבטחת קבוצות " \
            "🦁 בוט לניהול הזמנת מוצרים " \
            "🦁 בוט מיני אתר\חנות " \
            "🦁 הדרכה - פיתוח בוטים " \
            "🦁 בוטים לניהול מאגרי מידע " \
            "🦁  צאט בוטים לכל מטרה! " \
            "🦁 צרו עמי קשר " \
            "@FlatEarthBob"
    query.message.reply_text(message)


def mainmenu(update, context):
    user_id = update.effective_message.from_user.id
    chat_id = update.effective_chat.id
   
    buttons = []
    
    message = "\U0001F3C1 תפריט ראשי \U0001F3C1"
    
    admin_menu = emojize("תפריט ניהול")
    search = emojize("\U0001F50D חיפוש")
    cancel = emojize("\U0000274c ביטול")
    create = emojize("\U0001F4F0 צור מודעה")
    posts = emojize("\U0001F440 המודעות שלי")
    rules = emojize("\U0001F4F4 כללי שימוש")
    privacy = emojize("\U0001F9B8 מדיניות הפרטיות")
    support = emojize("\U0001F4BB תמיכה טכנית")
    help = emojize("\U00002753 עזרה")
    bots = emojize("\U0001F916 רוצים בוט משלכם?")
    latest = emojize("\U0001F195 פרסומים חדשים")

    # Always include the admin menu item
    #if user_id in admin_list:
    
    buttons += [[InlineKeyboardButton(admin_menu, callback_data="cb_admin_menu")]]
    buttons += [[InlineKeyboardButton(latest, callback_data="cb_latest")]]
    buttons += [[InlineKeyboardButton(search, callback_data="cb_search")]]
    buttons += [[InlineKeyboardButton(create, callback_data="cb_create")]]
    buttons += [[InlineKeyboardButton(posts, callback_data="cb_myposts")]]
    buttons += [[InlineKeyboardButton(rules, callback_data="cb_rules")]]
    buttons += [[InlineKeyboardButton(privacy, callback_data="cb_privacy")]]
    buttons += [[InlineKeyboardButton(support, callback_data="cb_support")]]
    buttons += [[InlineKeyboardButton(bots, callback_data="cb_bots")]]
    buttons += [[InlineKeyboardButton(help, callback_data="cb_help")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    

    start_keyboard = list(buttons)
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    message,
    reply_markup=reply_markup_start
    )

def catmenu(update, context):
    query = update.callback_query
    #data = query.data
    chat_id = update.effective_chat.id
    buttons = [[]]
    menu_count = db_buttons.count_documents({})
    reply_text = "תפריט לחיפוש קטגוריות:\n"
    for b in db_buttons.find({}):
        button_name = b['ButtonName']
        button_cb = b['ButtonCb']

        #btn_name = emojize(" \U0001f31f " + button_name)

        #buttons[0].append(InlineKeyboardButton(str(button_name), callback_data=str(button_cb)))
        buttons += [[InlineKeyboardButton(str(button_name), callback_data=str(button_cb))]]
    def chunks(lst, n):

        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    buttons += [[InlineKeyboardButton(str("חזרה"), callback_data="cb_back")]]
    menu_buttons = list(buttons)
    
    main_keyboard = InlineKeyboardMarkup(menu_buttons)
    query.edit_message_text(
    reply_text,
    reply_markup=main_keyboard,
    timeout=60
    )

def start(update, context):
    print("STARTING BOT2")
    
    print(str(db_images) + "\n\n&&&&&&&&&&&&&&&&&&&&\n\n")
    result = db_images.find_one_and_delete({"ImageText": "logo"})
    query = update.callback_query

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message_date = update.message.date
    message_id = update.message.message_id

    text = update.message.text
    
    item = {"UserId": user_id,
        "MessageId":message_id,
        "MessageText":text
    }
    if db.messages.find_one({'MessageId': message_id}):
        print("הודעה רשומה כבר!" + str(message_id))
    else:
        db.messages.insert_one(item)
        print("ההודעה נשמרה ;-)" + str(message_id))
    
    """if db.messages.count({'MessageId': message_id}, limit=1) > 0:
        print("הודעה רשומה כבר!" + str(message_id))
        pass
    else:
        db.messages.insert_one(item)
        print("ההודעה נשמרה ;-)" + str(message_id)) """

    
    res = db_logo.find_one({"ImageCode":"logo"})
    print("RESULT - " + str(res))
    url = res['ImageId']
    
    msg = "\U0000200F\n\U0001F981 שלום {} \n ברוכים הבאים אל בוט2, בוט שרות לסחר ישיר בין אנשים.".format(username) + "\n\n" \
    "\U0001F39E ראשית אני מעדיף לעבוד עם קבצי וידאו של MP4, אז קחו את הזמן ליצור את הסרטונים הכי יפים שלכם לפני שאתם שולחים לבוט\nאפשר להעלות איזה גודל שרוצים אבל עדיף סרטון קצר, קליט ומתומצת.\n\n" \
    "\U0001F4EE לעלות פוסט זה פשוט מאוד, לוחצים על צור מודעה והבוט יכנס למצב הקשבה להודעת המודעה שלכם עם הקובץ וידאו. \n\n" \
    "⚠ שימו לב! ברגע שההודעה שלכם עלתה הבוט יחזיר לכם עותק ביחד עם מספר מודעה ייחודי. תשמרו על קוד מודעה זה על מנת לנהל את המודעות שלכם. ⚠\n\n" \
    "\U00002049 מודעות עם תכנים מיניים, פוגעניים או כל סוג של מודעה שהמנהלים יחליטו שאינה מתאימה, תוסר לאלתר והמשתמש יקבל אזהרה. אנא עברו על כללי הבוט או כתבו /help.\n\n" \
    "\U0001F5FF מכיוון שטלאגרם הינה מערכת מוצפנת וחינמית, עדיין הבוט שפותח עבורה הוא שלנו. אנו מאפשרים שימוש חופשי במערכת זו ונמשיך לפתח אותה ככל שקהילת המשתמשים תגדל. דבר זה תלוי בזמן ומשאבים ולכן אנו נשתדל לתמוך במערכת ככל שנוכל. נשמח לראותכם כאן איתנו.\U0001F981"
    message = emojize(str(msg))
    user_full_details = emojize(str(user_id) + " - " + str(username))
    context.bot.send_photo(chat_id, url, message)
    #context.bot.send_message(583505750, user_full_details, parse_mode="HTML")
    user = update.effective_message.from_user

    logger.info("User %s started the conversation.", user.first_name)
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    message_date = update.effective_message.date
    msg_id = update.effective_message.message_id

    fullname = str(user.first_name) + " " +str(user.last_name)


    print(username)
    print(fullname)
    print(user_id)
    print(chat_id)
    print(msg_id)

    context.user_data['user_id'] = user_id
    context.user_data['fullname'] = fullname
    context.user_data['username'] = username
    context.user_data['start_message_id'] = msg_id
    #context.user_data['location'] = location
    details = context.user_data
    user_Mobile = ""
    user_location = ""
    reply_keyboard = []
    items = []

    tmp_product = {
            "UserId":user_id,
            "UserName": str(username),
            "FullName":str(fullname),
            "ProductText": "", #from button selection
            "Quantity":"", #from button selection
            "Mobile":"", #from button selection
            "Address":"", #from contact location optional!
            "Location":"",
            "Status":"Pending", # Dispatched/Delivered
            "Date":message_date
        }
    db_tmp_product.insert_one(tmp_product)

    reply_text = ""

    if context.user_data:
        reply_text += "\U0001F981 ברוכים השבים {}".format(username)
        #reply_text += message

    else:
        reply_text += message

    search = emojize("\U0001F50D חיפוש")
    cancel = emojize("\U0000274c ביטול")
    create = emojize("\U0001F4F0 צור מודעה")
    posts = emojize("\U0001F440 המודעות שלי")
    rules = emojize("\U0001F4F4 כללי שימוש")
    privacy = emojize("\U0001F9B8 מדיניות הפרטיות")
    support = emojize("\U0001F4BB תמיכה טכנית")
    help = emojize("\U00002753 עזרה")
    bots = emojize("\U0001F916 רוצים בוט משלכם?")
    latest = emojize("\U0001F195 פרסומים חדשים \U0001F195")
    admin_menu = "תפריט אדמין"
    
    
    buttons = []
    if user_id in admin_list:
        buttons += [[InlineKeyboardButton(admin_menu, callback_data="cb_admin_menu")]]
    else:
        pass
    buttons += [[InlineKeyboardButton(latest, callback_data="cb_latest")]]
    buttons += [[InlineKeyboardButton(search, callback_data="cb_search")]]
    buttons += [[InlineKeyboardButton(create, callback_data="cb_create")]]
    buttons += [[InlineKeyboardButton(posts, callback_data="cb_myposts")]]
    buttons += [[InlineKeyboardButton(rules, callback_data="cb_rules")]]
    buttons += [[InlineKeyboardButton(privacy, callback_data="cb_privacy")]]
    buttons += [[InlineKeyboardButton(support, callback_data="cb_support")]]
    buttons += [[InlineKeyboardButton(bots, callback_data="cb_bots")]]
    buttons += [[InlineKeyboardButton(help, callback_data="cb_help")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    
    start_keyboard = list(buttons)
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    reply_text,
    reply_markup=reply_markup_start
    )






def upload_video(update, context):
    #query = update.callback_query

    message = update.message.chat.type
    #pprint(message)


    m = update.message
    if m.video:
        file_id = m.video.file_id
        document = "video/mp4"
    elif m.document:
        if m.document.mime_type == 'video/mp4':
            file_id = m.document.file_id
            document = "document"

    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    first_name = update.effective_message.from_user.first_name
    last_name = update.effective_message.from_user.last_name

    fullname = str(first_name) +' '+ str(last_name)

    upload_date = update.effective_message.date
    msg_id = update.effective_message.message_id
    message_types = ['document', 'video', 'video/mp4']
    text = update.effective_message.caption

    """cursor = db_videos.find({})
    for vid in cursor:
        if vid['VideoId'] == file_id:
            update.message.reply_text("הסרטון הזה כבר קיים במערכת, אנא העלו סרטון חדש.")
        else:

            pass"""

    if username != 0 and fullname !=0:

        if document in message_types:
            #file_id = update.message.video.file_id

            current_time = datetime.datetime.utcnow()

            m = update.message
            if document == 'video/mp4':
                file_id = m.video.file_id
            elif document == 'document':
                file_id = m.document.file_id
            print("FILE-ID >>>>> " + str(file_id))

            userId = str(user_id)
            date = str(upload_date)
            vidId = str(file_id)
            cap = str(text)
            video_owner = str(username)
            randomNum = randStr(N=10)
            video_code = str(userId+randomNum)
            video_item = {
                "Owner":username,
                "FileType":document,
                "UserId":user_id,
                "VideoId":vidId,
                "VideoText":cap,
                "VideoCode":video_code,
                "UploadDate":upload_date,
                "Category":"category",
                "Price":0.0,
                "Quantity":0,
                "Width":0.0,
                "Length":0.0,
                "Height":0.0,
                "Weight":0.0,
                "Color":"color",
                "State":"used",
                "Status":"pending"

            }
            db_videos.insert_one(video_item)

            video_details = emojize("Upload Date: "+str(upload_date)+"\n"
                                    +"File Owner: "+"@"+str(username)+"\n"
                                    +"Post Code: "+str(video_code)+"\n----------------\n")
            video_details += cap

            if document == 'video/mp4':

                context.bot.send_video(chat_id, video=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "\U0000200F עותק זה נשלח על ידי בוט2 בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_video(user_id, video=file_id, caption=video_details, parse_mode='HTML')
            elif document == 'document':
                context.bot.send_document(chat_id, document=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "\U0000200F עותק זה נשלח על ידי בוט2 בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_document(user_id, document=file_id, caption=video_details, parse_mode='HTML')

            context.bot.send_message(chat_id, "\U0000200F הפוסט שלכם נשמר בהצלחה ויופיע במאגר החיפוש החל מהיום.\n שמרו את פרטי המודעה ובפרט את קוד המודעה שהונפק עבורה, רק איתה תוכלולנהל את המודעה שלכם.\nעל מודעות שנענו ונמכרו, על אחריות המוכר לשלוח את פקודת ההסרה.\nמודעות מעל חודש יוסרו מהרשימה באופן אוטומטי אלא אם כן נשלחה פקודת חידוש.")
            pass
        else:
            context.bot.send_message(chat_id, text="משהו קרה והקובץ לא נשמר, נסו שנית.")
            pass
    else:
        context.bot.send_message("\U0000200F אנא וודאו שיש לכם לפחות שם משתמש רשום שאוכל להשתמש בו לרישום המודעות שלכם.\n וודאו שכל השדות בפרופיל שלכם בטלאגרם מלאים עם שם לזיהוי במערכת שלנו.\n תוכלו לחזור ולנסות שנית בכל עת שתרצו, תודה שהייתם אצלנו, להתראות.")
    update.message.reply_text("\U0000200F הצאט יתנקה תוך שניות ספורות, אנא שמרו את קוד המודעה.\nחשוב מאוד לא לאבד אותו, זכרו! ללא הקוד לא תוכלו לנהל את המודעה.")
    sleep(3)

    mainmenu(update, context)


def clear_chat(update, context):
    query = update.callback_query
    if query != "NoneType" and query != "":
        data = query.data
    else:
        pass
    #message_id = update.callback_query.message.message_id
    #chat_id = query.message.chat.id
    chat_id = update.effective_message.chat_id
    cursor = db_messages.find({})
    for m in cursor:

        if m !=0:

            msgId = m["MessageId"]
            if msgId == 0:

                pass
            else:
                try:
                    context.bot.delete_message(chat_id, msgId)
                    print(str(msgId) + "<<<< ההודעה נמחקה")
                except:
                    pass

        else:

            pass
    if context.user_data == "":
        user_id = update.effective_message.from_user.id
    elif data == "cb_back":
        user_id = context.user_data['user_id']
    else:
        user_id = query.from_user.id
    #start_message_id = context.user_data['start_message_id']


    cur = db_messages.find_one({"UserId": user_id})
    if cur['MessageId'] == "":
        pass
    else:
        start_message_id = cur['MessageId'] - 10

    msg_id_range = start_message_id+20
    for i in range(start_message_id, msg_id_range):

        try:
            context.bot.delete_message(chat_id, i)
            i += 1
        except:
            pass

    x = db_messages.delete_many({})
    y = db_tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    welcome(update, context)


def restart(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data

    clear_chat(update, context)


def new_item(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    #query.edit_message_text(data)

    main_message = emojize("\U0000200F יופי \U0001F63A אני אשמח לקבל פריט חדש, בואו נתחיל.\n כל שעליכם לעשות הוא לשלוח לי סרטונים קצרים של הפריטים וכתבו בהודעה את כל הפרטים הרלוונטים\nכולל מחיר, מחיר משלוח אם קיים וכל  פרט חשוב.\nאתם יכולים להשתמש באימוג'ים ובכיתוב <b>להדגשת טקסט</b>.\nאנא וודאו כי צילמתם סרטון איכותי וקחו את הזמן לצלם לפחות 20 שניות.'")

    new_item_keyboard = emojize("פריט חדש")
    search = emojize("חיפוש")
    cancel = emojize("ביטול")

    replay_markup_keyboard = [[InlineKeyboardButton("חזרה", callback_data="cb_back"),
                                InlineKeyboardButton("ביטול", callback_data=str("cancel"))
                                ]]

    markup_keyboard = InlineKeyboardMarkup(replay_markup_keyboard)
    query.edit_message_text(str(main_message), reply_markup=markup_keyboard, parse_mode="HTML")


def privacy(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    if data == "cb_privacy":
        message = "\U0000200F מדיניות הפרטיות:\n\n" \
                "הבוט הזה שנקרא \"בוט2\" פותח בעבור הקהילה ובאופן חינמי ועל מנת לספק שרות עבור כל אחד ואחת שירצו לפרסם כל מוצר למכירה או מסירה.\n\n" \
                "המידע המפורסם במודעה הינה על אחריות המפרסם ותפקידו לנהל את המודעות שלו ולדאוג לתקשורת ישירה מול הרוכש. אין אנו אחראים למפורסם ו\או לכל עניין שבין המוכר לקונה. אנו רק מספקים פלטפורמה ודואגים לתפעולה.\n\n" \
                "אנו נעשה את כל המאמצים לוודא שרק מודעות שיעמדו בכללי המערכת יפורסמו למאגר החיפוש. במידה ונתקלתם במודעה עם תוכן פוגעני עבורכם וברצונכם להתלונן על כך, תוכלו לעשות זאת בקבוצת התמיכה.\n\n" \
                "לכל מודעה שתפורסם יצורף קישור להתקשרות ישירה עם המפרסם. בדרך זו תוכלו להתקשר בצאט ישיר אל המוכר\קונה ולסגור את פרטי העסקה ביניכם. אין אנו אחראים להסרת מודעות לאחר גמר המכירה, אנו מבקשים מכם לוודא שהסרתם את המודעה שלם בעזרת הפקודה המיועדת לכך בסיום העסקה.\n\n" \
                "מעבר לפרסום שם המשתמש של המפרסם בטלאגרם אין אנו מפרסמים שום מידע אחר ואת קוד המודעה שהינו פרטי לכל מודעה עליכם לשמור למעקב וניהול. עניין זה באחריותכם בלבד.\n\n" \
                "כמו כן כל מידע אחר כמו מספרי טלפון וכתובות לאספקה ומשלוח הינו על אחריות המפרסם בלבד ואין מידע זה מפורסם על ידינו כלל. אנו תמיד ממליצים לשמור על בטיחות ברשת ולא לחשוף פרטים מעבר לנדרש.\n\n" \
                "אנו נשתדל לעשות כל שביכולתינו לעמוד לרשותכם ולעזור לכם למצוא את מבוקשכם. מכיוון שזו מערכת חדשה יתכנו באגים ותקלות קטנות שאותן נפתור בהקדם האפשרי.\n\n" \
                "נשמח לענות לכל שאלה \בקשה בקבוצה התמיכה, אנו מקווים לראותכם איתנו בקרוב.\n בברכה, צוות בוט2"
        context.bot.send_message(chat_id, text=message)
    sleep(3)
    mainmenu(update,context)


def rules(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    if data == "cb_rules":
        message = "\U0000200F כללי שימוש:\n\n" \
                "\U0001F539 מטרת הבוט הינה לספק שרות חינמי, פשוט, יעיל ומהיר לפרסום מוצרים למכירה\מסירה.\n\n" \
                "\U0001F539 כל אחד\אחת רשאים להעלות כמה מודעות שירצו ובלבד שאלו יהיו רק מודעות וידאו.\n\n" \
                "\U0001F539 אנו עובדים בהתנדבות ומפאת זמן ומשאבים נעשה ככל יכולתנו לוודא שהמערכת תעבוד באופן שוטף.\n\n" \
                "\U0001F539 המטרה שלנו הינה ליצור שרותים חינמיים בטלאגרם שיפעלו באופן קהילתי ולא תאגידי. הכל יעבוד בדרך של תרומות ותמיכה של הקהילה בעצמה.\n\n" \
                "\U0001F539 אנו נעשה את כל המאמצים להבטיח שרות פעיל ושוטף ואנו מזמינים אתכם להיות חלק מהקהילה המתפתחת שלנו בטלאגרם.\n\n" \
                "\U0001F539 מודעות שמפורסמות קודם כל עוברות בדיקה לוודא שהן עומדות בנהלים שלנו. מרגע שהמודעה מאושרת היא תופיע במאגר של המודעות. עליכם לוודא שלאחר יצירת המודעה יש לשייך אותה לאחת הקטגוריות מהרשימה.\n\n" \
                "\U0001F539 אנו ממליצים לעבור על הפקודות השונות בכדי להתרגל למערכת. אל תחששו ליצור מודעות וגם למחוק אותן כמה שתרצו על מנת שתלמדו להעלות מודעות יפות ומסודרות.\n\n" \
                "\U0001F539 אנו מאמינים שברגע שתתרגלו לעבוד עם המערכת שלנו לא תכנסו יותר לשום אתר אחר לחפש את המוצר שלכם. הכל יהיה הרבה יותר נגיש מהמובייל, בכל מקום ובכל שעה.\n\n" \
                "\U0001F539 אנו שומרים את הזכות לעדכן את הנהלים מפעם לפעם וכמו כן להוסיף פקודות ושרותים חדשים לבוט. לקבלת תמיכה טכנית או לשאול כל שאלה בנושא תפעול הבוט, אנא השתמשו בקבוצה התמיכה דרך הקישור בתפריט הראשי.\n\n" \
                "\U0001F600 נשמח לראותכם איתנו פועלים יחד למען כולנו."
        context.bot.send_message(chat_id, text=message)
    sleep(3)
    mainmenu(update,context)


def support(update, context, *args, **kwargs):
    query = update.callback_query
    chat_id = update.effective_chat.id
    #context.answer_callbak_query(update.callback_query.id)
    data = query.data
    #url = "".format(str("https://t.me/feisupport"))
    if data == "cb_support":
        context.bot.send_message(chat_id, text='https://telegram.me/feisupport')

def search(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    
    # Retrieve the category name from the button callback data
    cursor = db_buttons.find_one({"ButtonCb": data})
    category_name = cursor['ButtonName']

    # Search the videos collection for posts in the selected category
    posts = db_videos.find({"Category": category_name})

    # Construct a message with the search results
    message = f"מודעות בקטגוריה {category_name}:\n"
    for post in posts:
        owner = str(post['Owner'])
        video_id = str(post['VideoId'])
        video_text = str(post['VideoText'])
        video_code = str(post['VideoCode'])
        date = str(post['UploadDate'])
        cat = str(post['Category'])
        state = str(post['State'])
        status = str(post['Status'])
        file_type = str(post['FileType'])

        message += emojize("👤 פורסם על ידי: @"+str(owner)+"\nלהתחלת צאט עם המפרסם לחצו על הקישור.\n\n⬇ פרטי המודעה ⬇\n"+"-------------\n\n"+"👇 קוד מודעה 👇 <b>"+video_code+"</b> \n\n"+"📅 הועלה בתאריך: \n"+str(date)+"\n\n"+"🗃 קטגוריה: "+cat+"\n"+"🟢 מצב פריט: "+state+"\n"+"⚠ סטטוס מודעה: "+status+"\n\n"+str(video_text)+"\n\n-------------\n")
        
        #message += f"Title: {post['title']}\nDescription: {post['description']}\n\n"

    # If no posts found, inform the user
    nposts = list(db_videos.find({"Category": category_name}))
    num_posts = len(nposts)
    if num_posts == 0:
        message = f"לא נמצאו מודעות בקטגוריה {category_name}.\n"

    # Send the search results or message indicating no posts found to the chat
    context.bot.send_message(chat_id, text=message)

    # Return to the main menu
    mainmenu(update, context)


def welcome(update, context):

    query = update.callback_query
    res = db_logo.find_one({"ImageCode":"logo"})
    url = res['ImageId']
    firstName = update.effective_message.from_user.first_name
    lastName = update.effective_message.from_user.last_name
    username = str(firstName) + " " +  str(lastName)
    category = context.user_data
    reply_text = "ברוכים הבאים {} להתחלה לחצו על /start".format(username)
    """star_keyboard = []
    star_keyboard =  [[InlineKeyboardButton("התחל", callback_data="restart")]]
    star_keyboard = list(star_keyboard)
    reply_markup_start = InlineKeyboardMarkup(star_keyboard)"""
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id, url, reply_text)
    #return ConversationHandler.END

def ending_order(update, context):
    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['address'] = text
    category = context.user_data['address']

    print("TYPING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(text))

    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("✅ אישור", callback_data="done")], [InlineKeyboardButton("❌ ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)

    if category != 0:

        doc = db_tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Address": category}
        },upsert=True
        )

        order.append(category)
        #update.message.reply_text("מעולה! אלו הם פרטי ההזמנה עד כה: \n{}\n לאישור ההזמנה לחצו על אישור והשליח יצא לדרך...".format(context.user_data), reply_markup=reply_markup_cancel)
        update.message.reply_text("אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n\n 💬 תודה רבה שרכשתם אצלנו, לאישור ההזמנה לחצו על אישור.", reply_markup=reply_markup_cancel)
    return FIFTH

def completed(update, context):
    query = update.callback_query
    data = context.user_data
    message_date = update.effective_message.date
    print(''.join(choice(ascii_uppercase) for i in range(12)))
    order_number = ''.join(choice(ascii_uppercase) for i in range(12))
    user_id = context.user_data['user_id']

    one_completed_order = {

        "OrderNumber":order_number,
        "UserId":data['user_id'],
        "UserName":data['username'],
        "FullName":data['fullname'],
        "Product":data['product'],
        "Quantity":data['quantity'],
        "Mobile":data['mobile'],
        "Address":data['address'],
        "Location":"",
        "Status":"Waiting",
        "Date":message_date,

    }
    db_completed_orders.insert_one(one_completed_order)
    context.bot.send_message(user_id, "הזמנתכם התקבלה במערכת ואנו פועלים להוציא אליכם שליח במהירות. אנא היו זמינים לעדכון ממני מתי  להיות מוכנים להגעת השליח.")

    sleep(5)
    delete_messages(update, context)

def done(update, context):
    query = update.callback_query
    query.answer()

    category = context.user_data
    reply_text = "אלו הם פרטי ההזמנה שאושרו, אני יעדכן אותכם בקרוב , היו זמינים!\n" + "\n{}\n".format(facts_to_str(context.user_data))

    done_keyboard = []
    done_keyboard =  [[InlineKeyboardButton("נקה צ'אט'", callback_data="completed")]]
    done_keyboard = list(done_keyboard)
    reply_markup_done = InlineKeyboardMarkup(done_keyboard)
    if category != 0:
        show_data(update, context)
        #query.edit_message_text("מעולה! אלו הם פרטי ההזמנה עד כה: \n{} תודה שרכשתם אצלנו.".format(context.user_data), reply_markup=reply_markup_done)
    sleep(1)
    #return ConversationHandler.END

def show_data(update, context):

    query = update.callback_query

    user_id = context.user_data['user_id']
    fullname = context.user_data['fullname']
    username = context.user_data['username']
    product = context.user_data['product']
    quantity = context.user_data['quantity']
    ordername = context.user_data['ordername']
    mobile = context.user_data['mobile']
    address = context.user_data['address']
    date = update.effective_message.date

    message = "זיהוי משתמש: " + str(user_id)+ "\nשם מלא: " + str(fullname)+ "\nשם משתמש: " + str(username)+ "\nמוצר: " + str(product) + "\nכמות: "
    message += str(quantity)+ "\nשם המזמין: " + str(ordername)+ "\nנייד: " + str(mobile)+ "\nכתובת: "
    message += str(address)+ "\nתאריך: " + str(date) + "\n"
    print(message)
    message = emojize(message)
    msg = emojize("אלו הם פרטי ההזמנה עד כה: \n {}\n השאירו את הצאט פתוח שאוכל לעדכן אתכם בהמשך, היו זמינים, השליח בדרך :pizza: ".format(message))
    context.bot.send_message(chat_id=update.effective_message.chat_id, text=msg)
    sleep(2)
    completed(update, context)
#############################################################################################################
#############################################################################################################


def delete_messages(update, context):
    query = update.callback_query
    #message_id = update.callback_query.message.message_id
    #chat_id = query.message.chat.id
    chat_id = update.effective_message.chat_id
    cursor = db_messages.find({})
    for m in cursor:

        if m !=0:

            msgId = m["MessageId"]
            if msgId == 0:

                pass
            else:
                try:
                    context.bot.delete_message(chat_id, msgId)
                    print(str(msgId) + "<<<< ההודעה נמחקה")
                except:
                    pass

        else:

            pass
    start_message_id = context.user_data['start_message_id']
    start_message_id = start_message_id - 10

    msg_id_range = start_message_id+20
    for i in range(start_message_id, msg_id_range):

        try:
            context.bot.delete_message(chat_id, i)
            i += 1
        except:
            pass

    x = db_messages.delete_many({})
    y = db_tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    welcome(update, context)



def all_messages(update, context):

    msgId = update.message.message_id
    text = update.message.text

    item = {
        "MessageId":msgId,
        "MessageText":text
    }


#############################################################################################################
#############################################################################################################
def catch_error(f):
    @wraps(f)
    def wrap(bot, update):
        logger.info("User {user} sent {message}".format(user=update.message.from_user.username, message=update.message.text))
        try:
            return f(bot, update)
        except Exception as e:
            # Add info to error tracking
            client.user_context({
                "username": update.message.from_user.username,
                "message": update.message.text
            })

            client.captureException()
            logger.error(str(e))
            bot.send_message(chat_id=update.message.chat_id,
                             text="An error occured ...")

    return wrap


def cancel(update, context):
    query = update.callback_query
    query.answer()

    username = query.from_user.username

    if username == None:
        firstName = query.from_user.first_name
        lastName = query.from_user.last_name
        username = str(firstName) + " " +  str(lastName)
    query.edit_message_text("להתראות {}".format(username))
    chat_id = update.effective_message.chat_id
    cursor = db_messages.find({})
    for m in cursor:
        print(m)
        if m !=0:

            msgId = m["MessageId"]
            if msgId == 0:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - >>>>>>>>>>הודעה ריקה - אין ID")
                pass
            else:
                try:
                    context.bot.delete_message(chat_id, msgId)
                except:
                    print(str(msgId) + "<<<< הודעה אינה קיימת!")
                    pass
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - >>>>>>>>>> אין הודעות")
            pass
    start_message_id = context.user_data['start_message_id']
    start_message_id = start_message_id - 20

    msg_id_range = start_message_id+40
    for i in range(start_message_id, msg_id_range):

        try:
            context.bot.delete_message(chat_id, i)
            print('Message {} Deleted'.format(i))
            i += 1
        except:
            print("NO Message ID {} Found, not deleted".format(i))
    x = db_messages.delete_many({})
    y = db_tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    sleep(2)
    welcome(update, context)




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="סליחה אבל הפקודה הזאת אינה מוכרת לי\nאנא כתבו את הפקודה /help בכדי לקבל רשימת הפקודות האפשריות.\n")

def help(update, context):
    chat_id = update.effective_message.chat_id
    msg = emojize("להלן רשימת הפקודות של הבוט\n\n" +
                                "/start - על מנת לקבל את התפריט הראשי\n\n"+
                                "לביטול לחצו על ביטול\n\n" +
                                "/getlist - לרשימת מודעות שפורסמו לאחרונה.\n\n" +
                                "/categories - לקבלת רשימת קטגוריות לשיוך מודעות\n\n" +
                                "/set - לשיוך מודעתכם לאחת הקטגוריות. יש להוסיף את קוד המודעה שלכם + רווח ולהוסיף את שם הקטגוריה.\n\n" +
                                "/myposts - להצגת רשימה של המודעות שפירסמתם\n\n" +
                                "/delete - למחיקת מודעה הוסיפו את קוד המודעה יחד עם פקודה זו. אתם יכולים למחוק רק הודעות שמשוייכות אליכם!   \n\n" +
                                "** בקרוב סדרת פקודות נוספות לניהול וחיפוש **")
    context.bot.send_message(chat_id, msg)
    sleep(3)
    mainmenu(update,context)

@restricted
def admin(update, context):
    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id
    msg = emojize("להלן רשימת הפקודות של הבוט\n" +
                                "להתחלת הזמנה הקלידו /start\n" +
                                "לביטול הזמנה לחצו על סיום ללא הקלדת נתונים או כתבו /cancel - סיום או Done\n" +
                                "רק לאחר שמלאתם את כל הנתונים לחיצה על סיום תשלח הזמנה.\n" +
                                "לצפייה בהזמנות במצב המתנה כתבו את הפקודה /getlist\n" +
                                "לסגירת ההזמנה סיום המשלוח יש לכתוב את פקודת /setitem והמספר הטלפון של המזמין\n פקודה זו תעדכן את מצב ההזמנה - ל- Delivered\n" +
                                "לקבלת עדכון מצב של כל ההזמנות שבוצעו יחד עם סך כולל יש לכתוב /total\n" +
                                "עלמנת לעדכן תמונות מוצר חדשים לבוט יש פשוט להעלות תמונה לבוט והוא יארגן אותן במקום \n\n כאשר רוצים להחליף תמונות יש לרשום פקודת /clear שתמחוק את התמונות הישנות.\n" +
                                "עלמנת לעדכן תמונת פתיחה\לוגו יש לשלוח תמונה עם הכיתוב logo בלבד"
                                "עלמנת לראות שוב את הודעת העזרה כתבו /help")
    context.bot.send_message(chat_id, msg)
    sleep(3)
    mainmenu(update,context)

@restricted
def showlist(update, context):
    chat_id = update.effective_chat.id    
    result = db_videos.find({"Status" : "pending"})

    if result != "":
    
        for r in result:
            if r['Status'] == "pending":

                owner = r['Owner']
                file_type = r['FileType']
                vidId = r['VideoId']
                vidCap = r['VideoText']
                uploaded_date = r['UploadDate']
                category = r['Category']
                state = r['State']

                message = emojize("משיוך אל: @"+str(owner)+"\nפרטי המודעה:\n"+str(vidCap)+"\nתאריך פרסום: "+str(uploaded_date)+"\nקטגוריה: "+str(category)+"\nמצב הפריט: "+str(state)+"\n")

                if file_type == 'video/mp4':
                    context.bot.send_video(CHATID, video=vidId, caption=message, parse_mode='HTML')
                elif file_type == 'document':
                    context.bot.send_document(CHATID, document=vidId, caption=message, parse_mode='HTML')

                sleep(1)
            else:
                pass
    else:
        context.bot.send_message(CHATID, text="לא נמצאו מודעות לאישורכם.")
    sleep(5)
    mainmenu(update,context)

def myposts(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    query.edit_message_text("מביא את רשימת המודעות שלך, אנא המתן...\n")
    sleep(1)
    user_id = update.callback_query.from_user.id
    cursor = db.videos.find({})
    print(user_id)
    for item in cursor:
        sleep(0.5)
        if item['UserId'] == user_id:
            print("foudn match!!!!!!")
            owner = str(item['Owner'])
            video_id = str(item['VideoId'])
            video_text = str(item['VideoText'])
            video_code = str(item['VideoCode'])
            date = str(item['UploadDate'])
            cat = str(item['Category'])
            state = str(item['State'])
            status = str(item['Status'])
            file_type = str(item['FileType'])

            message = emojize("👤 פורסם על ידי: @"+str(owner)+"\nלהתחלת צאט עם המפרסם לחצו על הקישור.\n\n⬇ פרטי המודעה ⬇\n"+"-------------\n\n"+"👇 קוד מודעה 👇 <b>"+video_code+"</b> \n\n"+"📅 הועלה בתאריך: \n"+str(date)+"\n\n"+"🗃 קטגוריה: "+cat+"\n"+"🟢 מצב פריט: "+state+"\n"+"⚠ סטטוס מודעה: "+status+"\n\n"+str(video_text)+"\n\n-------------\n")
            #message = emojize("👤 פורסם על ידי: @"+str(owner)+"\nלהתחלת צאט עם המפרסם לחצו על הקישור.\n\n⬇ פרטי המודעה ⬇\n"+"-------------\n\n"+str(vidCap)+"\n\n📅 תאריך ושעת פרסום: \n"+str(uploaded_date)+"\n\n🗃 קטגוריה: "+str(category)+"\n\n🟢 מצב הפריט: "+str(state)+"\n\n-------------\n")

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id, video=video_id, caption=message, parse_mode='HTML')
            elif file_type == 'document':
                context.bot.send_document(chat_id, document=video_id, caption=message, parse_mode='HTML')
        else:
            query.edit_message_text("לא נמצאו מודעות שפרסמתם! או שקוד המודעה אינו משוייך אליכם.\n אנא בדקו שרשמתם את קוד המודעה המתאים ושהמודעה משוייכת לחשבון ממנו אתם מחוברים.")
    sleep(3)
    mainmenu(update,context)


def set(update, context):
    chat_id = update.effective_message.chat_id
    user_id = update.effective_message.from_user.id

    args1 = str(context.args[0])
    args2 = str(context.args[1])
    try:
        args3 = str(context.args[2])
    except:
        args3 = ""

    cat_name = str(args2) + ' ' +  str(args3)
    cursor = db_videos
    cur_cat = db_buttons
    
    cat_arr = []
    for v in cursor.find():
        if v['UserId'] == user_id:
            if v['VideoCode'] == args1:
                for cat in cur_cat.find():

                    btn_name = str(cat['ButtonName'])
                    cat_arr.append(btn_name)

                #print(f"{cat_arr=}")
                if str(cat_name) != "" and str(cat_name.strip()) in cat_arr:
                    db_videos.update_one({'VideoCode': str(args1)}, {'$set': {'Category': str(cat_name)}})
                    update.message.reply_text("הקטגוריה {} שוייכה בהצלחה למודעה שלכם.".format(cat_name))
                elif str(cat_name) != "" and str(cat_name) not in cat_arr:
                    #print(f"{cat_name=}")
                    update.message.reply_text("שם הקטגוריה שהקלדתם לא תואמת את רשימת הקטגוריות הניתנות לשיוך. אנא בדקו את הרשימה על ידי פקודת /categories ולאחר מכן נסו שנית.")
                    #context.bot.send_message(chat_id, text="שם הקטגוריה שהקלדתם לא תואמת את רשימת הקטגוריות הניתנות לשיוך. אנא בדקו את הרשימה על ידי פקודת /categories ולאחר מכן נסו שנית.")
                    pass
                else:
                    update.message.reply_text("המודעה עודכנה ושויכה לקטגוריה {}.".format(cat_name))

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def set_category(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Fetch the list of categories from the database
    categories = [cat['ButtonName'] for cat in db_buttons.find()]

    # Generate inline keyboard buttons for each category
    keyboard = [[InlineKeyboardButton(cat_name, callback_data=f"select_category_{cat_name}")] for cat_name in categories]

    # Create InlineKeyboardMarkup from the keyboard buttons
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message to the user with the list of categories as buttons
    update.message.reply_text("בחר קטגוריה:", reply_markup=reply_markup)

def select_category(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    category_name = query.data.split('_')[2]

    # Update the post category in the database
    db_videos.update_one({'VideoCode': args1, 'UserId': user_id}, {'$set': {'Category': category_name}})

    # Send a confirmation message
    query.edit_message_text(f"הקטגוריה '{category_name}' שוייכה בהצלחה למודעה שלך.")



def categories(update, context):
    cursor = db_buttons
    catlist = ""
    words = ""

    for btn in cursor.find():
        print(btn['ButtonName'])
        catlist += str(btn['ButtonName']) + "\n"
        words += str(btn['ButtonCb']) + " | "
        
    text = "אלו הקטגוריות האפשריות לשיוך מודעות. אנא השתמשו בפקודת העריכה לקטגוריות ובחרו את הקטגוריה המתאימה עבור המודעה שלכם.\n\n"
    message = text + catlist
    update.message.reply_text(message)
    sleep(3)
    mainmenu(update,context)

@restricted
def delete(update, context):
    user_id = update.effective_message.from_user.id
    code = str(context.args[0])
    cursor = db_videos.find({})

    for vid in cursor:
        if vid['UserId'] == user_id and vid['VideoCode'] == code:
            cur = db_videos.find_one_and_delete({"VideoCode": code})
            update.message.reply_text("מודעה עם קוד {} נמחקה מהמאגר!".format(code))
        elif vid['UserId'] != user_id or vid['UserId'] == "":
            update.message.reply_text("מודעה עם קוד {} לא נמצאה או שהקוד שגוי או שמודעה זו אינה משוייכת אל החשבון ממנו אתם מחוברים. אנא בדקו את הפרטים ונסו שנית.".format(code))

@restricted
def approve(update, context):

    code = str(context.args[0])
    cur = db_videos.find_one_and_update({"VideoCode": code},
                                    {"$set": {"Status": "approved"}})
    update.message.reply_text("מודעה עם קוד {} אושרה!".format(code))

def quickstart(update, context):
    result = db_images.find_one_and_delete({"ImageText": "logo"})
    query = update.callback_query

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message_date = update.message.date
    message_id = update.message.message_id

    text = ""
    res = db_logo.find_one({"ImageCode":"logo"})
    url = res['ImageId']
    msg = "בקרוב תפריט לחיפוש נוח יותר לבנתיים תוכלו תמיד לכתוב לי /help בשביל לקבל את רשימת הפקודות העדכניות."
    message = emojize(str(msg))
    user_full_details = emojize(str(user_id) + " - " + str(username))
    context.bot.send_photo(chat_id, url, text)

    start_keyboard = emojize("התחל")
    search = emojize("חיפוש")
    cancel = emojize("ביטול")
    start_keyboard = [
            [InlineKeyboardButton(start_keyboard, callback_data="start"), InlineKeyboardButton(cancel, callback_data="cancel")]
             ]
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    message,
    reply_markup=reply_markup_start
    )

    return FIRST

def getlist(update, context):
    chat_id = update.effective_chat.id
    result = db_videos.find({})
    val = ""
    for r in result:
        if r['Status'] == "approved":

            owner = r['Owner']
            file_type = r['FileType']
            vidId = r['VideoId']
            vidCap = r['VideoText']
            uploaded_date = r['UploadDate']
            category = r['Category']
            state = r['State']

            message = emojize("👤 פורסם על ידי: @"+str(owner)+"\nלחצו על השם לפתיחת צאט ישיר\n\n⬇ פרטי המודעה ⬇\n"+"-------------\n\n"+str(vidCap)+"\n\n📅 תאריך ושעת פרסום: \n"+str(uploaded_date)+"\n\n🗃 קטגוריה: "+str(category)+"\n\n🟢 מצב הפריט: "+str(state)+"\n\n-------------\n")

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id, video=vidId, caption=message, parse_mode='HTML')
            elif file_type == 'document':
                context.bot.send_document(chat_id, document=vidId, caption=message, parse_mode='HTML')

            sleep(1)
    mainmenu(update, context)


def pendingPosts (update, context):
    chat_id = update.effective_chat.id
    result = db_videos.find({})
    val = ""
    for r in result:
        if r['Status'] == "pending":

            owner = r['Owner']
            file_type = r['FileType']
            vidId = r['VideoId']
            vidCap = r['VideoText']
            uploaded_date = r['UploadDate']
            category = r['Category']
            state = r['State']

            message = emojize("👤 פורסם על ידי: @"+str(owner)+"\nלחצו על השם לפתיחת צאט ישיר\n\n⬇ פרטי המודעה ⬇\n"+"-------------\n\n"+str(vidCap)+"\n\n📅 תאריך ושעת פרסום: \n"+str(uploaded_date)+"\n\n🗃 קטגוריה: "+str(category)+"\n\n🟢 מצב הפריט: "+str(state)+"\n\n-------------\n")

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id, video=vidId, caption=message, parse_mode='HTML')
            elif file_type == 'document':
                context.bot.send_document(chat_id, document=vidId, caption=message, parse_mode='HTML')

            sleep(1)
    mainmenu(update, context)
    

@restricted
def setitem(update, context):
    chat_id = update.effective_message.chat_id
    text = str(context.args)
    text = text.strip("[\']")
    #update.message.reply_text(chatId, "Updating status to delivered for {}...")
    result = db["completed"].find({})
    for r in result:
        Mobile = str(r["Mobile"])
        if Mobile == text:
            context.bot.send_message(chat_id, "...מעדכן רשומה למצב סופק")
            db["completed"].find_one_and_update({"Mobile": text}, {"$set":{"Status": "Delivered"}})
            context.bot.send_message(chat_id, "<b>Update SUCCESS!</b>", parse_mode='HTML')
            context.bot.send_message(chat_id, "הרשומה עודכנה בהצלחה!")

"""@restricted
def total(update, context):
    chat_id = update.effective_message.chat_id
    result = db["completed"].find({})
    total_orders = []
    sum = 0
    for r in result:
        status = str(r["Status"])
        if status == "Delivered":
            total_orders.append(r["Quantity"])
            msg = emojize("☑️ הזמנה שסופקה:" + "\n" + str(r["UserId"]) + "\n" + str(r["UserName"]) + "\n" + str(r["FullName"]) + "\n" + "קוד מוצר: " + str(r["Product"]) + "\n" + "כמות: " +str(r["Quantity"]))
            msg2 = emojize("\n" + str(r["Mobile"]) + "\n" + str(r["Address"]) + "\n" + str(r["Status"]) + "\n" + str(r["Date"]))
            context.bot.send_message(chat_id, msg+msg2)

    for i in range(0, len(total_orders)):
        sum = sum + total_orders[i];

    msg = emojize("סך כל ההזמנות שסופקו:\n {} ".format(sum))
    context.bot.send_message(chat_id, msg)"""

@restricted
def clear_images(update, context):
    chat_id = update.effective_message.chat_id
    msg = "כל התמונות נמחקו, אנא עדכנו תמונות חדשות על ידי העלאה לצאט."
    x = db_images.delete_many({})
    context.bot.send_message(chat_id, msg)

@restricted
def listimages(update, context):

    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id
    message_types = ['photo', 'video']
    upload_date = update.effective_message.date
    caption = update.message.caption
    caption = caption.lower()

    #if helpers.effective_message_type(update.message) in message_types:
    if caption == "logo":
        res = db_logo.delete_many({})
        update.message.reply_text(" תמונת לוגו התקבלה!")
        file_id = update.message.photo[0].file_id
        current_time = datetime.datetime.utcnow()
        context.bot.send_message(chat_id, str(upload_date))
        context.bot.send_message(chat_id, file_id)
        context.bot.send_photo(chat_id, file_id)
        context.bot.send_message(chat_id, str(caption))

        cursor = db_images.find({})
        for img in cursor:
            if img['ImageCode'] == "logo":
                res = db_logo.delete_many({})
                pass
            elif db_images.count_documents({}) == 0:
                image_code = "logo"


        image_code = "logo"
        userId = str(user_id)
        date = str(upload_date)
        imgId = str(file_id)
        cap = str(caption)
        imageItem = {
            "UserId":user_id,
            "ImageId":imgId,
            "ImageText":cap,
            "ImageCode":image_code,
            "ImageDate":date

        }
        db_logo.insert_one(imageItem)

    else:

        #file_id = update.message.photo[0].file_id
        #current_time = datetime.datetime.utcnow()
        #context.bot.send_message(chat_id, str(upload_date))
        #context.bot.send_message(chat_id, file_id)
        #context.bot.send_photo(chat_id, file_id)
        
        message = "אני מקבל רק קבצי וידאו MP4.\nבבקשה שלחו לי קובץ צילום וידאו של הפריט או השרות שהנכם מציעים למכירה או רכישה, אני ממתין...\n"
        context.bot.send_message(chat_id, str(message))

    return mainmenu(update, context)

def fallback(update, context):
    update.message.reply_text("Sorry, I didn't understand that. Please try again.")

def main():

    defaults = Defaults(parse_mode=ParseMode.HTML)
    if os.path.exists("botwo_persist_file.txt"):
        os.remove("botwo_persist_file.txt")
    else:
        print("Good!!! - The file does not exist!")
    fei_persist = PicklePersistence(filename='botwo_persist_file.txt', store_user_data=True, store_chat_data=True,
                                    single_file=True)
    fei_persist.flush()

    userData = fei_persist.get_user_data()
    chatData = fei_persist.get_chat_data()
    userConv = fei_persist.get_conversations('-1001177209024')

    uDataFile = open(r"userData.txt", "w")
    cDataFile = open(r"chatData.txt", "w")
    cnvDataFile = open(r"convData.txt", "w")

    uDataFile.write(str(userData))
    uDataFile.close()
    cDataFile.write(str(chatData))
    cDataFile.close()
    cnvDataFile.write(str(userConv))
    cnvDataFile.close()
    
    pp = PicklePersistence(filename='botwo.txt')

    token = '1005480770:AAHZLpw1vclOGq2nwNlStt5aDbqrIiNsxYI'
    updater = Updater(token, use_context=True, defaults=defaults, request_kwargs={'read_timeout': 900, 'connect_timeout': 900})
    job_queue = updater.job_queue
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    SELF_CHAT_ID = '@' + updater.bot.get_me().username
    print("SELF_CHAT_ID"+SELF_CHAT_ID)
    print("CHATID"+str(CHATID))


    dp.add_handler(CommandHandler('start', start, pass_args=True))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    dp.add_handler(CommandHandler('admin', admin))
    dp.add_handler(CommandHandler('getlist', getlist))
    dp.add_handler(CommandHandler('setitem', setitem))
    #dp.add_handler(CommandHandler('total', total))
    dp.add_handler(CommandHandler('clear', clear_images))
    dp.add_handler(CommandHandler('delete', delete))
    dp.add_handler(CommandHandler('approve', approve))
    dp.add_handler(CommandHandler('showlist', showlist))
    dp.add_handler(CommandHandler('set', set))
    dp.add_handler(CommandHandler('categories', categories))

    dp.add_handler(CommandHandler('catmenu', catmenu))

    dp.add_handler(MessageHandler(Filters.photo, listimages))
    #dp.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
    show_data_handler = CommandHandler('show_data', show_data)
    dp.add_handler(show_data_handler)
    dp.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(new_item, pattern="^restart|start$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(MessageHandler(Filters.document.category("video/mp4") | Filters.document.category("video") | Filters.video, upload_video, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    #dp.add_handler(CommandHandler('setitem', setitem, filters=Filters.chat(CHATID)))
    #dp.add_handler(CommandHandler('clear', clear_images, filters=Filters.chat(CHATID)))
    #dp.add_handler(CommandHandler('total', total, filters=Filters.chat(CHATID)))
    #dp.add_handler(CallbackQueryHandler(help, pattern="^help$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    #dp.add_handler(CommandHandler('adminhelp', adminhelp, filters=Filters.chat(CHATID)))
    dp.add_handler(MessageHandler(Filters.photo, listimages))
    #dp.add_handler(MessageHandler(Filters.document, upload_video))
    dp.add_handler(MessageHandler(Filters.user('@bottwoilbot') and Filters.entity(MessageEntity.TEXT_LINK) and (Filters.entity(MessageEntity.URL)) and (Filters.text | Filters.video | Filters.photo | Filters.document), all_messages))
    #dp.add_handler(MessageHandler(Filters.update, any_message))
    dp.add_handler(MessageHandler(Filters.command, unknown))  # Filters unknown commands
    #dp.add_handler(MessageHandler(Filters.update, messages))
    dp.add_error_handler(error)

    ######## SEARCH MENU HANDLER ################################

    cursor = db_buttons.find({})
    for btn in cursor:
        word = str(btn['ButtonCb'])
        dp.add_handler(CallbackQueryHandler(search, pattern=word, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(catmenu, pattern="cb_search", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(restart, pattern="cb_back", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(new_item, pattern="cb_create", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(support, pattern="cb_support", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(rules, pattern="cb_rules", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(privacy, pattern="cb_privacy", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(help, pattern="^cb_help$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(myposts, pattern="cb_myposts", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(getlist, pattern="cb_latest", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(bots_advert, pattern="cb_bots", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(admin_menu, pattern="cb_admin_menu", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(pendingPosts, pattern="cb_pending_posts", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(mainmenu, pattern="cb_main_menu", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))

    dp.add_handler(CallbackQueryHandler(manage_categories, pattern='^cb_manage_categories$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(delete_category, pattern='^cb_delete_category$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(add_category, pattern='^cb_add_category$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(back_to_main_menu, pattern='^cb_main_menu$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))

    # Add handler for handling category name input
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.user, handle_category_name))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.user, handle_new_category_name))

    dp.add_handler(CallbackQueryHandler(cancel_delete, pattern='^cb_cancel_delete$'))
    dp.add_handler(CallbackQueryHandler(cancel_add_category, pattern='^cb_cancel_add_category$'))
    dp.add_handler(CallbackQueryHandler(select_category, pattern=r'^select_category_'))
    
    dp.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':

    main()
