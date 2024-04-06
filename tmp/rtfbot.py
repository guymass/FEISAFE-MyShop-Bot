#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This RTF Network Bot was Developed by Guy Mass
import motor.motor_asyncio
import asyncio
import urllib
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
import fasttext
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

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'

directory = '/uploads'

username = urllib.parse.quote_plus('guy')
password = urllib.parse.quote_plus('OVc8EBd@guy!')
#mongo_connection = 'mongodb://%s:%s@206.189.21.199:27017/' % (username, password)
client = MongoClient('mongodb://%s:%s@localhost:27017/' % (username, password), unicode_decode_error_handler='ignore')
#client = motor.motor_asyncio.AsyncIOMotorClient(mongo_connection)
db = client.mateder

admin_list = [583505750, 671752791]
CHATID = -1001145942387



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

db.images = db.images
db.categories = db.categories
db.tmp_product = db.tmp_product
db.products = db.products
db.messages = db.messages
db.buttons = db.buttons
db.logo = db.logo
db.videos = db.videos

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

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))



"""@run_async
def mainmenu(update, context):
    chat_id = update.effective_chat.id
    message = "\U0001F3C1 תפריט ראשי \U0001F3C1"
    #bio = emojize("\U0001F9EC סדנת ביו-האקינג בגולן")
    biosession = emojize("\U0001F9EC הרצאת ביו-האקינג")
    biohealth = emojize("\U0001F6B4 ביו-האקינג למטפלים ושוחרי בריאות")
    bioorg = emojize("\U0001F465 ביו-האקינג לארגונים")
    biotodo = emojize("\U0001F9EE יש מה לעשות - דיגיטאלי")
    bioscreen = emojize("\U0001F5A5 הפחתת נזקי מסכים - דיגיטאלי")
    biobody = emojize("\U0001F4AA סגולות החשמל של הגוף")
    products = emojize("\U0001F6D2 לחנות")
    cancel = emojize("\U0000274c ביטול")
    #buttons = [[InlineKeyboardButton(bio, callback_data="cb_bio")]]
    buttons = [[InlineKeyboardButton(biosession, callback_data="cb_session")]]
    buttons += [[InlineKeyboardButton(biohealth, callback_data="cb_health")]]
    buttons += [[InlineKeyboardButton(bioorg, callback_data="cb_org")]]
    buttons += [[InlineKeyboardButton(biotodo, callback_data="cb_digital")]]
    buttons += [[InlineKeyboardButton(bioscreen, callback_data="cb_screen")]]
    buttons += [[InlineKeyboardButton(biobody, callback_data="cb_body")]]
    buttons += [[InlineKeyboardButton(products, callback_data="cb_products")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]

    start_keyboard = list(buttons)
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    message,
    reply_markup=reply_markup_start
    )"""


@run_async
def start(update, context):
    result = db.images.find_one_and_delete({"ImageText": "logo"})
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

    if db.messages.count_documents({'MessageId': message_id}, limit=1) > 0:
        print("הודעה רשומה כבר!" + str(message_id))
        pass
    else:
        db.messages.insert_one(item)
        print("ההודעה נשמרה ;-)" + str(message_id))


    res = db.logo.find_one({"PhotoCode":"logo"})
    url = res['ImageId']
    msg = "\n\n\U0001F505 שלום {} \U0001F505\n\n וברוכים הבאים אל החנות של מעלים את התדר 528 בטלאגרם.".format(username) + "\n\n" \
    "\U0001F3C1 סדנאות וקורסים תכנית הדגל - 'יש מה לעשות!' - להפחתת נזקים בריאותיים בעולם הדיגיטלי המתועש - [לפרטים נוספים](https://ahava528.com/yesh-ma-laasot/)\n\n"
    message = emojize(str(msg))
    user_full_details = emojize(str(user_id) + " - " + str(username))
    file = 'AgACAgQAAxkBAAN4Xq7SIAnqyJpF7HeERO85vbZO20UAAsSyMRtxBHlR92Y6E8j9txHB_D0kXQADAQADAgADbQADJC8AAhkE'
    context.bot.send_photo(chat_id, url)
    context.bot.send_photo(chat_id, file, message, parse_mode='markdown')
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
            "ImageId":"",
            "VideoCode":"",
            "Price":0.0,
            "Category":"category",
            "Quantity":"", #from button selection
            "Mobile":"", #from button selection
            "Address":"", #from contact location optional!
            "Location":"",
            "Status":"Pending", # Dispatched/Delivered
            "Date":message_date
        }
    db.tmp_product.insert_one(tmp_product)

    reply_text = ""

    if context.user_data:
        reply_text += "\U0001F505 ברוכים השבים {} \U0001F505".format(username)
        #reply_text += message

    else:
        reply_text += message

    #bio = emojize("\U0001F9EC סדנת ביו-האקינג בגולן")
    biosession = emojize("\U0001F9EC הרצאת ביו-האקינג")
    biohealth = emojize("\U0001F6B4 ביו-האקינג למטפלים ושוחרי בריאות")
    bioorg = emojize("\U0001F465 ביו-האקינג לארגונים")
    biotodo = emojize("\U0001F9EE יש מה לעשות - דיגיטאלי")
    bioscreen = emojize("\U0001F5A5 הפחתת נזקי מסכים - דיגיטאלי")
    biobody = emojize("\U0001F4AA סגולות החשמל של הגוף")
    products = emojize("\U0001F6D2 לחנות")
    cancel = emojize("\U0000274c ביטול")
    #buttons = [[InlineKeyboardButton(bio, callback_data="cb_bio")]]
    buttons = [[InlineKeyboardButton(biosession, callback_data="cb_session")]]
    buttons += [[InlineKeyboardButton(biohealth, callback_data="cb_health")]]
    buttons += [[InlineKeyboardButton(bioorg, callback_data="cb_org")]]
    buttons += [[InlineKeyboardButton(biotodo, callback_data="cb_todo")]]
    buttons += [[InlineKeyboardButton(bioscreen, callback_data="cb_screen")]]
    buttons += [[InlineKeyboardButton(biobody, callback_data="cb_body")]]
    buttons += [[InlineKeyboardButton(products, callback_data="cb_products")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    start_keyboard = list(buttons)
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    reply_text,
    reply_markup=reply_markup_start
    )


@run_async
def bio(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = ""
    if data == "cb_bio":
        message += "*סדנת ביו האקינג*\n\n" \
        "דרך טבעית מבוססת מדע לבריאות אופטימלית ושגשוג בעולם המודרני\n\n" \
        "זוכרים כשהייתם ילדים, איך הסתובבתם ערומים? יחפים על האדמה? בשמש? לא היה לכם קר ולא מלוכלך, לא הפחידו אתכם עם סרטן העור ולא עם חול מה קרה מאז? העולם השתנה!!! הבורגנות והמודרניות כרסמו בבריאות ובביולוגיה שלנו והילדים שלנו ואנחנו משלמים מחיר כבד על כך.\n\n" \
        "ביו-האקינג = שימוש בנתוני הסביבה הטבעיים, על מנת לשפר את היכולת הביולוגית של האדם וע\"י כך לשפר את הבריאות, להפחית דלקות ומחלות ולהיות בבריאות אופטימלית.\n\n" \
        "*בבני יהודה, דרום רמת הגולן*\n זוהי הסדנא היחידה בישראל שנותנת מענה לכל קשת האתגרים, כמעט, שיש כיום בעולם המודרני. אנחנו ניגע בכל תחום שמשפיע ישירות על הביולוגיה שלכם. אור ותאורה, מים, מזון, מגנטיות, קרינה, המטען החשמלי של תאי הגוף והשדה האלקטרומגנטי שאנו חיים בו. הבריאות שלכם נמצאת בתשתית הפיסיקלית הנכונה לגוף שלכם.\n\n" \
        "זהו סופ\"ש של שגשוג והעלאת רמת האנרגיה הפיזית, הרגשית והמנטלית שלכם ושל המשפחה\n\n" \
        "זוהי סדנא ייחודית, שתיתן לכם כלים אמיתיים לקחת לחיי היומיום ולהעביר את הידע והכלים הללו לדורות הבאים.\n\n" \
        "*חשוב לדעת:*\n\n זוהי סדנא אינטימית (עד 10 משתתפים!!) באווירה ביתית מועבר בה ידע נדיר, שנשאר איתכם לעד. לינה משותפת באוהל טבילה בבריכת מים חיים טבילה במעיין ארוחות נקיות ומפנקות בתדר גבוה קרקוע בהייה בשמש ואיך אפשר בלי טעימה מצלילי קערות הקריסטל\n\n" \
        "עלות הסדנא במחיר מיוחד\nלרוכשים הראשונים לעונה 1,848 ש\"ח בלבד (או בשישה תשלומים של 308 ש\"ח) * קוד הנחה לזוגות (200 שח): zoog200 * עלות התכנית כוללת רשימת הבונוסים המופיעה למטה\n\n" \
        " להצתרפות לסדנא ולהרשמה מהירה בחרו את אחת האפשרויות ועקבו אחר ההוראות עד קבלת אישור ההזמנה. אנו מקווים לראותכם איתנו בקרוב.\n\n"

        date1= emojize("\U000021AA להתצרפות לסדנא בתאריך:")
        date2 = emojize("\U000021AA להתצרפות לסדנא בתאריך:")
        date3 = emojize("\U000021AA להתצרפות לסדנא בתאריך:")
        back = emojize("\U000021AA חזרה")
        cancel = emojize("\U0000274c ביטול")

        buttons = [[InlineKeyboardButton(date1, callback_data="cb_date1")]]
        buttons += [[InlineKeyboardButton(date2, callback_data="cb_date2")]]
        buttons += [[InlineKeyboardButton(date3, callback_data="cb_date3")]]
        buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
        buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
        bio_keyboard = list(buttons)
        reply_markup_bio = InlineKeyboardMarkup(bio_keyboard)

        query.edit_message_text(message, reply_markup=reply_markup_bio, parse_mode="markdown")

@run_async
def workshop(update, context):
    query = update.callback_query
    data = query.data
    user_id = query.message.from_user.id
    chat_id = update.effective_chat.id

    if data == "cb_date1":
        query.edit_message_text("\U00002757 אין כרגע סדנאות פתוחות בתאריך זה! {}\n".format(data))
    elif data == "cb_date2":
        query.edit_message_text("\U00002757 אין כרגע סדנאות פתוחות בתאריך זה! {}\n".format(data))
    elif data == "cb_date3":
        query.edit_message_text("\U00002757 אין כרגע סדנאות פתוחות בתאריך זה! {}\n".format(data))
    mainmenu(update, context)

@run_async
def pmenu(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "לפניכם רשימת מוצרים שאנו מוכרים ומשווקים לקהל העוקבים שלנו. הזמנה שתתקבל דרך הבוט תשלח לאחר קבלת התשלום. החיוב אינו מתבצע דרך הבוט, רק ההזמנה, אנו נחזור אליכם ברגע קבלת ההזמנה.\n\n"

    water_filter= emojize("\U0001F6B0 מזקק מים איכותי")
    live_water = emojize("\U0001F4A6 מתקני מים חיים לבית")
    blue_light = emojize("\U0001F4A1 הגנה מתאורה כחולה")
    radiation = emojize("\U00002622 מד קרינה")
    crystal = emojize("\U0001F963 דיסק 528 עם קערות קריסטל")
    air_cleaner = emojize("\U0001F32C מטהר ומחטא אויר לבית")
    silver_water = emojize("\U000026F2 מכונה להכנת מי כסף")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    if data == "pmenu":

        buttons = [[InlineKeyboardButton(water_filter, callback_data="cb_water")]]
        buttons += [[InlineKeyboardButton(live_water, callback_data="cb_live")]]
        buttons += [[InlineKeyboardButton(blue_light, callback_data="cb_blue")]]
        buttons += [[InlineKeyboardButton(radiation, callback_data="radiation")]]
        buttons += [[InlineKeyboardButton(crystal, callback_data="cb_crystal")]]
        buttons += [[InlineKeyboardButton(air_cleaner, callback_data="cb_cleaner")]]
        buttons += [[InlineKeyboardButton(silver_water, callback_data="cb_silver")]]
        buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
        buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
        products_keyboard = list(buttons)
        reply_markup_products = InlineKeyboardMarkup(products_keyboard)
        if message == "":
            query.message.reply_text(text=message, reply_markup=reply_markup_products, parse_mode="markdown")
        else:
            query.message.reply_text(text=message, reply_markup=reply_markup_products, parse_mode="markdown")
@run_async
def productsmenu(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "לפניכם רשימת מוצרים שאנו מוכרים ומשווקים לקהל העוקבים שלנו. הזמנה שתתקבל דרך הבוט תשלח לאחר קבלת התשלום. החיוב אינו מתבצע דרך הבוט, רק ההזמנה, אנו נחזור אליכם ברגע קבלת ההזמנה.\n\n"

    water_filter= emojize("\U0001F6B0 מזקק מים איכותי")
    live_water = emojize("\U0001F4A6 מתקני מים חיים לבית")
    blue_light = emojize("\U0001F4A1 הגנה מתאורה כחולה")
    radiation = emojize("\U00002622 מד קרינה")
    crystal = emojize("\U0001F963 דיסק 528 עם קערות קריסטל")
    air_cleaner = emojize("\U0001F32C מטהר ומחטא אויר לבית")
    silver_water = emojize("\U000026F2 מכונה להכנת מי כסף")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    if data == "cb_products":

        buttons = [[InlineKeyboardButton(water_filter, callback_data="cb_water")]]
        buttons += [[InlineKeyboardButton(live_water, callback_data="cb_live")]]
        buttons += [[InlineKeyboardButton(blue_light, callback_data="cb_blue")]]
        buttons += [[InlineKeyboardButton(radiation, callback_data="radiation")]]
        buttons += [[InlineKeyboardButton(crystal, callback_data="cb_crystal")]]
        buttons += [[InlineKeyboardButton(air_cleaner, callback_data="cb_cleaner")]]
        buttons += [[InlineKeyboardButton(silver_water, callback_data="cb_silver")]]
        buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
        buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
        products_keyboard = list(buttons)
        reply_markup_products = InlineKeyboardMarkup(products_keyboard)

        query.edit_message_text(message, reply_markup=reply_markup_products, parse_mode="markdown")

@run_async
def article(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']
    message = "להלן תוצאות החיפוש שלכם:\n\n"
    order_bio = emojize("\U000021AA הזמן עכשיו")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    buttons = [[InlineKeyboardButton(order_bio, callback_data="cb_order_bio")]]
    buttons += [[InlineKeyboardButton(back, callback_data="cb_back")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    bioarticle_keyboard = list(buttons)
    reply_markup_bioarticle = InlineKeyboardMarkup(bioarticle_keyboard)
    cb_list = ['cb_session', 'cb_org', 'cb_body', 'cb_todo', 'cb_health', 'cb_screen', 'radiation', 'cb_crystal', 'cb_cleaner', 'cb_digital', 'cb_screen']

    if data in cb_list:
        context.bot.send_message(chat_id, message, parse_mode="HTML")
        biocursor = db.videos.find({})
        for bio in biocursor:
            video_id = bio['VideoId']
            video_text = bio['VideoText']
            file_type = bio['FileType']
            category = bio['Category']
            callback = bio['MenuCb']
            print(callback)
            print(file_type)
            if file_type == 'video/mp4' and data == callback:
                context.bot.send_video(chat_id, video=video_id, caption=video_text, reply_markup=reply_markup_bioarticle, parse_mode='HTML')
                result1 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ProductText':video_text}})
                result2 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'VideoCode':video_id}})
                result3 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Price':0.0}})
                result4 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':category}})
            elif file_type == 'document' and data == callback:
                context.bot.send_document(chat_id, document=video_id, caption=video_text, reply_markup=reply_markup_bioarticle, parse_mode='HTML')
                result1 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ProductText':video_text}})
                result2 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'VideoCode':video_id}})
                result3 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Price':0.0}})
                result4 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':category}})
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")

@run_async
def water(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "להלן תוצאות החיפוש שלכם:\n\n"
    order_water = emojize("\U000021AA הזמן עכשיו")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    buttons = [[InlineKeyboardButton(order_water, callback_data="cb_order_water")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    water_keyboard = list(buttons)
    reply_markup_water = InlineKeyboardMarkup(water_keyboard)

    #query.edit_message_text(message, reply_markup=reply_markup_water, parse_mode="markdown")

    if data == "cb_water":
        cursor = db.videos.find({})
        for v in cursor:
            video_id = v['VideoId']
            video_text = v['VideoText']
            file_type = v['FileType']
            category = v['Category']
            if file_type == 'video/mp4' and v['Category'] == 'פילטרים':
                context.bot.send_video(chat_id, text=message, video=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
            elif file_type == 'document' and v['Category'] == 'פילטרים':
                context.bot.send_document(chat_id, text=message, document=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")
@run_async
def live(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "להלן תוצאות החיפוש שלכם:\n\n"
    order_halfinch = emojize("\U0001F4A6 מתקן חצי אינצ' (לבית) - 3300 ש\"ח")
    order_3q = emojize("\U0001F4A6 מתקן 3/4 אינצ' (לבית) 4400ש\"ח")
    order_1in = emojize("\U0001F4A6 מתקן 1 אינצ' (שימוש חקלאי / תעשייתי)")
    order_125 = emojize("\U0001F4A6 מתקן 1.25 אינצ' (שימוש חקלאי / תעשייתי)")
    order_2in = emojize("\U0001F4A6 מתקן 2 אינצ' (שימוש חקלאי / תעשייתי)")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")
    buttons = [[InlineKeyboardButton(order_halfinch, callback_data="cb_halfinch")]]
    buttons += [[InlineKeyboardButton(order_3q, callback_data="cb_3q")]]
    buttons += [[InlineKeyboardButton(order_1in, callback_data="cb_1in")]]
    buttons += [[InlineKeyboardButton(order_125, callback_data="cb_125")]]
    buttons += [[InlineKeyboardButton(order_2in, callback_data="cb_2in")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    water_keyboard = list(buttons)
    reply_markup_water = InlineKeyboardMarkup(water_keyboard)

    #query.edit_message_text(message, reply_markup=reply_markup_water, parse_mode="markdown")

    if data == "cb_live":
        cursor = db.videos.find({})
        for v in cursor:
            video_id = v['VideoId']
            video_text = v['VideoText']
            file_type = v['FileType']
            category = v['Category']
            if file_type == 'video/mp4' and v['Category'] == 'מים חיים':
                context.bot.send_video(chat_id, text=message, video=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
            elif file_type == 'document' and v['Category'] == 'מים חיים':
                context.bot.send_document(chat_id, text=message, document=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")

@run_async
def bluelight(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = query.message.from_user.id
    message = "להלן תוצאות החיפוש שלכם:\n\n"

    uvexlow = emojize("UVEX Low End 150ש\"ח")
    uvexsq = emojize("UVEX מרובעות 420ש\"ח")
    uvexround = emojize("UVEX עגולים - 420ש\"ח")
    redlight = emojize("אור אדום - 140ש\"ח כולל משלוח")
    iristech = emojize("IRIS TECH APP")
    raoptics = emojize("RA OPTICS 600-1000ש\"ח לזוג")
    blueblox = emojize("BLUE BLOX HI END - 300-500ש\"ח לזוג")
    blueblock = emojize("BLUE BLOCKER - 300-700ש\"ח לזוג")
    screen = emojize("מגן מסך - 70-500ש\"ח לפי גודל")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(uvexlow, callback_data="cb_uvexlow")]]
    buttons += [[InlineKeyboardButton(uvexsq, callback_data="cb_uvexsq")]]
    buttons += [[InlineKeyboardButton(uvexround, callback_data="cb_uvexround")]]
    buttons += [[InlineKeyboardButton(redlight, callback_data="cb_redlight")]]
    buttons += [[InlineKeyboardButton(iristech, callback_data="cb_iristech")]]
    buttons += [[InlineKeyboardButton(raoptics, callback_data="cb_raoptics")]]
    #buttons += [[InlineKeyboardButton(blueblox, callback_data="cb_blueblox")]]
    #buttons += [[InlineKeyboardButton(blueblock, callback_data="cb_blueblock")]]
    buttons += [[InlineKeyboardButton(screen, callback_data="screen")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    bluelight_keyboard = list(buttons)
    reply_markup_water = InlineKeyboardMarkup(bluelight_keyboard)

    if data == "cb_blue":
        cursor = db.videos.find({})
        for v in cursor:
            video_id = v['VideoId']
            video_text = v['VideoText']
            file_type = v['FileType']
            category = v['Category']
            if file_type == 'video/mp4' and v['Category'] == 'משקפי מגן':
                context.bot.send_video(chat_id, text=message, video=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
            elif file_type == 'document' and v['Category'] == 'משקפי מגן':
                context.bot.send_document(chat_id, text=message, document=video_id, caption=video_text, reply_markup=reply_markup_water, parse_mode='HTML')
    else:
        query.edit_message_text("לא נמצאו מוצרים בקטגוריה זו.")


@run_async
def approve_order(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']

    if data == 'approve_order':
        cursor = db.tmp_product.find({'UserId':user_id})
        for res in cursor:
            username = str(res['UserName'])
            user_id = str(res['UserId'])
            fullname = str(res['FullName'])
            product = str(res['ProductText'])
            category = str(res['Category'])
            image_id = str(res['ImageId'])
            price = str(res['Price'])
            date = str(res['Date'])
            status = str(res['Status'])
    order_number = ''.join(choice(ascii_uppercase) for i in range(12))


    one_completed_order = {

        "OrderNumber":order_number,
        "UserId":user_id,
        "UserName":username,
        "FullName":fullname,
        "Product":product,
        "Category":category,
        "ImageId":image_id,
        "VideoId":"",
        "Quantity":"",
        "Price":0.0,

        "Mobile":"",
        "Address":"",
        "Location":"",
        "Status":"הזמנה חדשה",
        "Date":date,

    }
    db.products.insert_one(one_completed_order)
    context.bot.send_message(user_id, "תודה שרכשתם בחנות של \"מעלים את התדר 528\" \nאנו קבלנו את הזמנתכם וניצור עמכם קשר בהקדם האפשרי לתאום תשלום ומשלוח. להתראות.")

    sleep(5)
    delete_messages(update, context)



@run_async
def purchase_item(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']
    username = update.effective_message.from_user.username
    firstname = update.effective_message.from_user.first_name
    lastname = update.effective_message.from_user.last_name
    date = datetime.datetime.utcnow()

    print(user_id)

    cursor = db.tmp_product.find_one({'UserId':user_id})

    for res in cursor:
        username = str(res['UserName'])
        user_id = str(res['UserId'])
        fullname = str(res['FullName'])
        product = str(res['ProductText'])
        category = str(res['Category'])
        image_id = str(res['ImageId'])
        price = str(res['Price'])
        date = str(res['Date'])
        status = str(res['Status'])

    message = "אלו הם פרטי ההזמנה:\n\n"
    message += "שם המזמין: @"+ username + "\n"
    message += "קוד זיהוי: " + user_id+"\n"
    message += "שם מלא: "+fullname+"\n"
    message += "קטגורית מוצר: "+category+"\n"
    message += "פרטי המוצר:\n\n"+product+"\n\n"
    message += "מחיר: "+price+"\n"
    message += "תאריך הזמנה: "+date+"\n"
    message += "סטטוס הזמנה: "+status+"\n\n"
    message += "לחיצה על אישור מהווה הסכמה לרכישה. אין אנו מבצעים גבייה כעת. אנו ניצור עמכם קשר לחיוב וקבלת פרטי משלוח."

    approve = emojize("\U0001F44D אישור")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(approve, callback_data="approve_order")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    approve_keyboard = list(buttons)
    reply_markup_approve = InlineKeyboardMarkup(approve_keyboard)
    context.bot.send_message(chat_id, text=message, reply_markup=reply_markup_approve, parse_mode="HTML")

@run_async
def handle_bio_menu(update, context):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_chat.id
    user_id = context.user_data['user_id']
    date = datetime.datetime.utcnow()
    cblist = ['cb_health', 'cb_crystal', 'cb_todo', 'radiation', 'cb_cleaner', 'cb_screen', 'cb_org', 'cb_body', 'cb_digital', 'cb_order_bio', 'cb_silver', 'cb_live', 'cb_blue', 'cb_water']


    if data in cblist:
        result_handler = db.tmp_product.find({})
        for h in result_handler:
            if h['UserId'] == user_id:

                username = h['UserName']
                user_id = h['UserId']
                fullname = h['FullName']
                product = h['ProductText']
                category = h['Category']
                image_id = h['ImageId']
                price = h['Price']
                date = h['Date']
                status = h['Status']
    message = "אלו הם פרטי ההזמנה:\n\n"
    message += "שם המזמין: @"+ username + "\n"
    message += "קוד זיהוי: " + str(user_id)+"\n"
    message += "שם מלא: "+fullname+"\n"
    message += "קטגורית מוצר: "+category+"\n"
    message += "פרטי המוצר:\n\n"+product+"\n\n"
    message += "מחיר: "+str(price)+"\n"
    message += "תאריך הזמנה: "+str(date)+"\n"
    message += "סטטוס הזמנה: "+status+"\n\n"
    message += "לחיצה על אישור מהווה הסכמה לרכישה. אין אנו מבצעים גבייה כעת. אנו ניצור עמכם קשר לחיוב וקבלת פרטי משלוח."

    approve = emojize("\U0001F44D אישור")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(approve, callback_data="approve_order")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    approve_keyboard = list(buttons)
    reply_markup_approve = InlineKeyboardMarkup(approve_keyboard)
    context.bot.send_message(chat_id, text=message, reply_markup=reply_markup_approve, parse_mode="HTML")

@run_async
def uvexmenu(update, context):
    query = update.callback_query
    data = query.data
    text = query.message.text
    chat_id = update.effective_chat.id
    date = datetime.datetime.utcnow()


    purchase = emojize("\U0001F4B3 המשך לרכישה")
    back = emojize("\U000021AA חזרה")
    cancel = emojize("\U0000274c ביטול")

    buttons = [[InlineKeyboardButton(purchase, callback_data="cb_purchase")]]
    buttons += [[InlineKeyboardButton(back, callback_data="pmenu")]]
    buttons += [[InlineKeyboardButton(cancel, callback_data="cancel")]]
    bluelight_keyboard = list(buttons)
    reply_markup_uvex = InlineKeyboardMarkup(bluelight_keyboard)
    context.bot.send_message(chat_id, text="*הזמינו עכשיו*", reply_markup=reply_markup_uvex, parse_mode="HTML")
    cblist = ['cb_uvexround', 'cb_uvexsq', 'cb_uvexlow', 'cb_redlight', 'cb_iristech', 'cb_raoptics', 'cb_blueblox', 'cb_blueblock', 'screen']
    cursor = db.images.find({})
    for res in cursor:
        if res['MenuCb'] == data and data in cblist:
            user_id = context.user_data['user_id']
            cursor2 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ProductText':res['PhotoText']}})
            cursor3 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'ImageId':res['PhotoId']}})
            cursor4 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Category':res['Category']}})
            cursor5 = db.tmp_product.find_one_and_update({'UserId':user_id}, {'$set':{'Price':0.0}})




@run_async
def showlist(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    query.message.reply_text("אלו המוצרים הזמינים בקטגוריה זו.\n")
    result = db.images.find({'MenuCb': data})
    list = ['cb_uvexround', 'cb_uvexsq', 'cb_uvexlow', 'cb_redlight', 'cb_iristech', 'cb_raoptics', 'cb_blueblox', 'cb_blueblock', 'screen']
    for res in result:
        if data in list:

            owner = res['Owner']
            photoId = res['PhotoId']
            photoCap = res['PhotoText']
            uploaded_date = res['UploadDate']
            category = res['Category']
            state = res['State']

            message = emojize("משיוך אל: @"+str(owner)+"\nפרטי המודעה:\n"+str(photoCap)+"\nתאריך פרסום: "+str(uploaded_date)+"\nקטגוריה: "+str(category)+"\nמצב הפריט: "+str(state)+"\n")
            context.bot.send_photo(chat_id, photo=photoId, caption=message, parse_mode='HTML')
            sleep(1)
    uvexmenu(update,context)


@restricted
@run_async
def upload_photo(update, context):
    message = update.message.chat.type
    chat_id = update.effective_chat.id
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    first_name = update.effective_message.from_user.first_name
    last_name = update.effective_message.from_user.last_name
    fullname = str(first_name) +' '+ str(last_name)

    upload_date = update.effective_message.date
    msg_id = update.effective_message.message_id
    text = update.effective_message.caption

    m = update.message
    if m.photo:
        file_id = m.photo[0].file_id
        print(file_id)


    if username != "" and fullname != "":
        current_time = datetime.datetime.utcnow()

        userId = str(user_id)
        date = str(upload_date)
        photoId = str(file_id)
        cap = str(text)
        photo_owner = str(username)
        randomNum = randStr(N=10)
        photo_code = str(userId+randomNum)
        photo_item = {
            "Owner":photo_owner,
            "UserId":user_id,
            "PhotoId":photoId,
            "PhotoText":cap,
            "PhotoCode":photo_code,
            "UploadDate":upload_date,
            "Category":"category",
            "MenuCb":"cb",
            "Price":0.0,
            "Quantity":0,
            "Width":0.0,
            "Length":0.0,
            "Height":0.0,
            "Weight":0.0,
            "Color":"צבע",
            "State":"חדש",
            "Status":"ממתין"

        }
        db.images.insert_one(photo_item)

        photo_details = emojize("Upload Date: "+str(upload_date)+"\n"
                                +"File Owner: "+"@"+str(username)+"\n"
                                +"Photo Code: "+str(photo_code)+"\n"
                                +"Photo ID: "+str(photoId)+"\n----------------\n")

        photo_details += cap

        context.bot.send_photo(chat_id, photo=file_id, caption=photo_details, parse_mode='HTML')


@restricted
@run_async
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
    pprint(document)
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

    """cursor = db.videos.find({})
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
                "MenuCb":"cb",
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
            db.videos.insert_one(video_item)

            video_details = emojize("Upload Date: "+str(upload_date)+"\n"
                                    +"File Owner: "+"@"+str(username)+"\n"
                                    +"Post Code: "+str(video_code)+"\n----------------\n")
            video_details += cap

            if document == 'video/mp4':

                context.bot.send_video(chat_id, video=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "עותק זה נשלח על ידי הבוט בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_video(user_id, video=file_id, caption=video_details, parse_mode='HTML')
            elif document == 'document':
                context.bot.send_document(chat_id, document=file_id, caption=video_details, parse_mode='HTML')
                user_msg = "עותק זה נשלח על ידי הבוט בשל מודעה שיצרתם. אנא שימרו על קוד המודעה שלכם, רק איתו תוכלו לבצע פעולות ניהול כמו מחיקה ועדכון."
                context.bot.send_document(user_id, document=file_id, caption=video_details, parse_mode='HTML')

            context.bot.send_message(chat_id, "הפוסט שלכם נשמר בהצלחה ויופיע במאגר החיפוש החל מהיום.\n שמרו את פרטי המודעה ובפרט את קוד המודעה שהונפק עבורה, רק איתה תוכלולנהל את המודעה שלכם.\nעל מודעות שנענו ונמכרו, על אחריות המוכר לשלוח את פקודת ההסרה.\nמודעות מעל חודש יוסרו מהרשימה באופן אוטומטי אלא אם כן נשלחה פקודת חידוש.")
            pass
        else:
            context.bot.send_message(chat_id, text="משהו קרה והקובץ לא נשמר, נסו שנית.")
            pass
    else:
        context.bot.send_message("אנא וודאו שיש לכם לפחות שם משתמש רשום שאוכל להשתמש בו לרישום המודעות שלכם.\n וודאו שכל השדות בפרופיל שלכם בטלאגרם מלאים עם שם לזיהוי במערכת שלנו.\n תוכלו לחזור ולנסות שנית בכל עת שתרצו, תודה שהייתם אצלנו, להתראות.")
    update.message.reply_text("הצאט יתנקה תוך שניות ספורות, אנא שמרו את קוד המודעה.\nחשוב מאוד לא לאבד אותו, זכרו! ללא הקוד לא תוכלו לנהל את המודעה.")

    sleep(3)

    mainmenu(update, context)


@run_async
def clear_chat(update, context):
    query = update.callback_query
    if query != "NoneType" and query != "":
        data = query.data
    else:
        pass
    #message_id = update.callback_query.message.message_id
    #chat_id = query.message.chat.id
    chat_id = update.effective_message.chat_id
    cursor = db.messages.find({})
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


    cur = db.messages.find_one({"UserId": user_id})
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

    x = db.messages.delete_many({})
    y = db.tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    welcome(update, context)

@run_async
def restart(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data

    clear_chat(update, context)

@run_async
def new_item(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    #query.edit_message_text(data)

    main_message = emojize("יופי \U0001F63A אני אשמח לקבל פריט חדש, בואו נתחיל.\n כל שעליכם לעשות הוא לשלוח לי סרטונים קצרים של הפריטים וכתבו בהודעה את כל הפרטים הרלוונטים\nכולל מחיר, מחיר משלוח אם קיים וכל  פרט חשוב.\nאתם יכולים להשתמש באימוג'ים ובכיתוב <b>להדגשת טקסט</b>.\nאנא וודאו כי צילמתם סרטון איכותי וקחו את הזמן לצלם לפחות עד 20 שניות.'")

    new_item_keyboard = emojize("פריט חדש")
    search = emojize("חיפוש")
    cancel = emojize("ביטול")

    replay_markup_keyboard = [[InlineKeyboardButton("חזרה", callback_data="cb_back"),
                                InlineKeyboardButton("ביטול", callback_data=str("cancel"))
                                ]]

    markup_keyboard = InlineKeyboardMarkup(replay_markup_keyboard)
    query.edit_message_text(str(main_message), reply_markup=markup_keyboard, parse_mode="HTML")

@run_async
def privacy(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    if data == "cb_privacy":
        message = "מדיניות הפרטיות:\n\n" \
                "הבוט הזה שנקרא \"הבוט\" פותח בעבור הקהילה ובאופן חינמי ועל מנת לספק שרות עבור כל אחד ואחת שירצו לפרסם כל מוצר למכירה או מסירה.\n\n" \
                "המידע המפורסם במודעה הינה על אחריות המפרסם ותפקידו לנהל את המודעות שלו ולדאוג לתקשורת ישירה מול הרוכש. אין אנו אחראים למפורסם ו\או לכל עניין שבין המוכר לקונה. אנו רק מספקים פלטפורמה ודואגים לתפעולה.\n\n" \
                "אנו נעשה את כל המאמצים לוודא שרק מודעות שיעמדו בכללי המערכת יפורסמו למאגר החיפוש. במידה ונתקלתם במודעה עם תוכן פוגעני עבורכם וברצונכם להתלונן על כך, תוכלו לעשות זאת בקבוצת התמיכה.\n\n" \
                "לכל מודעה שתפורסם יצורף קישור להתקשרות ישירה עם המפרסם. בדרך זו תוכלו להתקשר בצאט ישיר אל המוכר\קונה ולסגור את פרטי העסקה ביניכם. אין אנו אחראים להסרת מודעות לאחר גמר המכירה, אנו מבקשים מכם לוודא שהסרתם את המודעה שלם בעזרת הפקודה המיועדת לכך בסיום העסקה.\n\n" \
                "מעבר לפרסום שם המשתמש של המפרסם בטלאגרם אין אנו מפרסמים שום מידע אחר ואת קוד המודעה שהינו פרטי לכל מודעה עליכם לשמור למעקב וניהול. עניין זה באחריותכם בלבד.\n\n" \
                "כמו כן כל מידע אחר כמו מספרי טלפון וכתובות לאספקה ומשלוח הינו על אחריות המפרסם בלבד ואין מידע זה מפורסם על ידינו כלל. אנו תמיד ממליצים לשמור על בטיחות ברשת ולא לחשוף פרטים מעבר לנדרש.\n\n" \
                "אנו נשתדל לעשות כל שביכולתינו לעמוד לרשותכם ולעזור לכם למצוא את מבוקשכם. מכיוון שזו מערכת חדשה יתכנו באגים ותקלות קטנות שאותן נפתור בהקדם האפשרי.\n\n" \
                "נשמח לענות לכל שאלה \בקשה בקבוצה התמיכה, אנו מקווים לראותכם איתנו בקרוב.\n בברכה, צוות הבוט"
        context.bot.send_message(chat_id, text=message)
    sleep(3)
    mainmenu(update,context)

@run_async
def rules(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    if data == "cb_rules":
        message = "כללי שימוש:\n\n" \
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

@run_async
def support(update, context, *args, **kwargs):
    query = update.callback_query
    chat_id = update.effective_chat.id
    #context.answer_callbak_query(update.callback_query.id)
    data = query.data

    if data == "cb_support":
        context.bot.send_message(chat_id, text='https://t.me/joinchat/IseXVlYcbdoJ4FWiueCKWw')
@run_async
def search(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    cursor = db.buttons.find_one({"ButtonCb":data})
    text = cursor['ButtonName']

    context.bot.send_message(chat_id, text="מחפש מודעות בקטגוריה {}".format(text))
    mainmenu(update,context)

@run_async
def catmenu(update, context):
    query = update.callback_query
    #data = query.data
    chat_id = update.effective_chat.id
    buttons = []
    menu_count = db.buttons.count()
    reply_text = "תפריט לחיפוש קטגוריות:\n"
    for b in db.buttons.find({}):
        button_name = b['ButtonName']
        button_cb = b['ButtonCb']

        #btn_name = emojize(" \U0001f31f " + button_name)

        buttons += [[InlineKeyboardButton(str(button_name), callback_data=str(button_cb))]]

    buttons += [[InlineKeyboardButton(str("חזרה"), callback_data="cb_back")]]
    menu_buttons = list(buttons)
    main_keyboard = InlineKeyboardMarkup(menu_buttons)
    query.edit_message_text(
    reply_text,
    reply_markup=main_keyboard,
    timeout=60
    )





@restricted
def user_order_details(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))
    return "\n".join(facts).join(['\n', '\n'])

@run_async
def typing_name(update, context):

    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['ordername'] = text
    category = context.user_data['ordername']



    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)
    if category != 0:

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"FullName": category}
        },upsert=True
        )

        order.append(category)

        #update.message.reply_text("אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n הנה מה שקבלתי עד כה:\n{}\n אנא כתבו ושלחו לי את הנייד שלכם להתקשרות".format(context.user_data), reply_markup=reply_markup_cancel)
        update.message.reply_text("אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n\n 💬 אנא כתבו ושלחו לי את הנייד שלכם להתקשרות, אני ממתין...⏳", reply_markup=reply_markup_cancel)

    return THIRD

@run_async
def typing_order_address(update, context):
    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['mobile'] = text
    category = context.user_data['mobile']


    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)
    if category != 0:

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Mobile": category}
        },upsert=True
        )

        order.append(category)
        #update.message.reply_text("אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n הנה מה שקבלתי עד כה:\n{}\nאנא כתבו ושלחו לי את הכתובת למשלוח.".format(context.user_data), reply_markup=reply_markup_cancel)
        update.message.reply_text("אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n\n 💬 אנא שלחו לי כתובת מלאה למשלוח. אפשר גם לשלוח קישור של מיקום, אני ממתין...⏳", reply_markup=reply_markup_cancel)
    return FORTH

@run_async
def welcome(update, context):

    query = update.callback_query
    res = db.logo.find_one({"PhotoCode":"logo"})
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
    return ConversationHandler.END



@run_async
def ending_order(update, context):
    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['address'] = text
    category = context.user_data['address']

    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("✅ אישור", callback_data="done")], [InlineKeyboardButton("❌ ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)

    if category != 0:

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Address": category}
        },upsert=True
        )

        order.append(category)
        #update.message.reply_text("מעולה! אלו הם פרטי ההזמנה עד כה: \n{}\n לאישור ההזמנה לחצו על אישור והשליח יצא לדרך...".format(context.user_data), reply_markup=reply_markup_cancel)
        update.message.reply_text("אתם יכולים לבטל את ההזמנה בכל שלב על ידי לחיצה על ביטול!\n\n 💬 תודה רבה שרכשתם אצלנו, לאישור ההזמנה לחצו על אישור.", reply_markup=reply_markup_cancel)
    return FIFTH

@run_async
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
    db.completed_orders.insert_one(one_completed_order)
    completed_order = emojize( "מספר הזמנה: " + str(order_number) + "\n" +
                    "\n זיהוי משתמש: " + str(data['user_id']) +
                    "\n שם משתמש: " + str(data['username']) +
                    "שם מלא:" + str(data['fullname']) +
                    "\n\nמוצר\שרות שהוזמן: \n\n" + str(data['product']) +"\n\n" +
                    "כמות: " + str(data['quantity']) +
                    "\n\n פרטי המזמין: \n\n טלפון: " + str(data['mobile']) +
                    "\nכתובת: \n" + str(data['address']) +
                    "\n\nמצב הזמנה: " + str("הזמנה חדשה ממתינה") +
                    "\n תאריך: " + str(message_date))

    context.bot.send_message(CHATID, "הזמנתכם התקבלה במערכת ואנו פועלים להוציא אליכם שליח במהירות. אנא היו זמינים לעדכון ממני מתי  להיות מוכנים להגעת השליח.\n\nלהלן פרטי ההזמנה:\n\n {}".format(completed_order))

    sleep(5)
    delete_messages(update, context)


#@run_async
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

@run_async
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

@run_async
def delete_messages(update, context):
    query = update.callback_query
    #message_id = update.callback_query.message.message_id
    #chat_id = query.message.chat.id
    chat_id = update.effective_message.chat_id
    cursor = db.messages.find({})
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

    x = db.messages.delete_many({})
    y = db.tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    welcome(update, context)


@run_async
def all_messages(update, context):

    msgId = update.message.message_id
    text = update.message.text

    item = {
        "MessageId":msgId,
        "MessageText":text
    }

    if db.messages.count_documents({'MessageId': msgId}, limit=1) > 0:
        print("הודעה רשומה כבר!")
        pass
    else:
        db.messages.insert_one(item)
        print(str(msgId) + " >>>>>>> פרטי ההודעה נשמרו! <<<<<<<<<<")

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

@run_async
def cancel(update, context):
    query = update.callback_query
    query.answer()

    username = query.from_user.username

    if username == None:
        firstName = query.from_user.first_name
        lastName = query.from_user.last_name
        username = str(firstName) + " " +  str(lastName)
    query.message.reply_text("להתראות {}".format(username))
    chat_id = update.effective_message.chat_id
    cursor = db.messages.find({})
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
    x = db.messages.delete_many({})
    y = db.tmp_product.delete_many({})
    print("ההודעות נמחקו!\n")
    sleep(2)
    welcome(update, context)



@run_async
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
@run_async
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="סליחה אבל הפקודה הזאת אינה מוכרת לי\nאנא כתבו את הפקודה /help בכדי לקבל רשימת הפקודות האפשריות.\n")

def help(update, context):
    chat_id = update.effective_message.chat_id
    msg = emojize("להלן רשימת הפקודות של הבוט\n\n" +
                                "/start - על מנת לקבל את התפריט הראשי\n\n"+
                                "לביטול לחצו על ביטול\n\n" +
                                "/getlist - לרשימת מודעות שפורסמו לאחרונה.\n\n" +
                                "/categories - לקבלת רשימת קטגוריות לשיוך מודעות\n\n" +
                                "/setcategory - לשיוך מודעתכם לאחת הקטגוריות. יש להוסיף את קוד המודעה שלכם + רווח ולהוסיף את שם הקטגוריה.\n\n" +
                                "/myposts - להצגת רשימה של המודעות שפירסמתם\n\n" +
                                "/delete - למחיקת מודעה הוסיפו את קוד המודעה יחד עם פקודה זו. אתם יכולים למחוק רק הודעות שמשוייכות אל החשבון איתו יצרתם את המודעה.\n\n" +
                                "/help - על מנת לקבל את ההודעה הזו.\n\n"+
                                "** בקרוב סדרת פקודות נוספות לניהול וחיפוש **")
    context.bot.send_message(chat_id, msg)
    sleep(3)
    mainmenu(update,context)

@restricted
@run_async
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

@run_async
def myposts(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    query.edit_message_text("מביא את רשימת המודעות שלך, אנא המתן...\n")
    user_id = update.callback_query.from_user.id
    cursor = db.videos.find({})
    print(user_id)
    for item in cursor:
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

            message = emojize("משיוך אל: @"+owner+"\n"+"קוד מודעה: "+video_code+"\n"+"הועלה בתאריך: "+date+"\n"+"קטגוריה: "+cat+"\n"+"מצב פריט: "+state+"\n"+"סטטוס מודעה: "+status+"\n"+video_text)

            if file_type == 'video/mp4':
                context.bot.send_video(chat_id, video=video_id, caption=message, parse_mode='HTML')
            elif file_type == 'document':
                context.bot.send_document(chat_id, document=video_id, caption=message, parse_mode='HTML')
        else:
            query.edit_message_text("לא נמצאו מודעות שפרסמתם! או שקוד המודעה אינו משוייך אליכם.\n אנא בדקו שרשמתם את קוד המודעה המתאים ושהמודעה משוייכת לחשבון ממנו אתם מחוברים.")
    sleep(3)
    mainmenu(update,context)

@run_async
def setcategory(update, context):
    user_id = update.effective_message.from_user.id
    args = []
    i=1
    context_len = len(context.args)

    if context_len == 2:
        cat_name = str(context.args[1])
    if context_len == 3:
        cat_name = str(context.args[1]) + ' ' +  str(context.args[2])

    cursor = db.videos.find({})
    for v in cursor:
        if v['UserId'] == user_id:
            if v['VideoCode'] == context.args[0]:
                db.videos.update_one({'VideoCode': str(context.args[0])}, {'$set': {'Category': str(cat_name)}})
    update.message.reply_text("המודעה עודכנה ושויכה לקטגוריה {}.".format(cat_name))


@run_async
def categories(update, context):
    cursor = db.buttons.find({})
    catlist = ""
    words = ""
    for b in cursor:
        catlist += str(b['ButtonName']) + "\n"
        words += str(b['ButtonCb']) + " | "
    print(words)
    text = "אלו הקטגוריות האפשריות לשיוך מודעות. אנא השתמשו בפקודת העריכה לקטגוריות ובחרו את הקטגוריה המתאימה עבורה המודעה שלכם.\n\n"
    message = text + catlist
    update.message.reply_text(message)
    sleep(3)
    mainmenu(update,context)


@restricted
@run_async
def delete_ad(update, context):
    user_id = update.effective_message.from_user.id
    code = str(context.args[0])
    cursor = db.videos.find({})

    for vid in cursor:
        if vid['UserId'] == user_id and vid['VideoCode'] == code:
            cur = db.videos.find_one_and_delete({"VideoCode": code})
            update.message.reply_text("מודעה עם קוד {} נמחקה מהמאגר!".format(code))
        elif vid['UserId'] != user_id or vid['UserId'] == "":
            update.message.reply_text("מודעה עם קוד {} לא נמצאה או שהקוד שגוי או שמודעה זו אינה משוייכת אל החשבון ממנו אתם מחוברים. אנא בדקו את הפרטים ונסו שנית.".format(code))


@restricted
@run_async
def approve(update, context):

    code = str(context.args[0])
    cur = db.videos.find_one_and_update({"VideoCode": code},
                                    {"$set": {"Status": "approved"}})
    update.message.reply_text("מודעה עם קוד {} אושרה!".format(code))


@run_async
def quickstart(update, context):
    result = db.images.find_one_and_delete({"ImageText": "logo"})
    query = update.callback_query

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message_date = update.message.date
    message_id = update.message.message_id

    text = ""
    res = db.logo.find_one({"PhotoCode":"logo"})
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
    result = db.videos.find({})
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

            message = emojize("משיוך אל: @"+str(owner)+"\nפרטי המודעה:\n"+str(vidCap)+"\nתאריך פרסום: "+str(uploaded_date)+"\nקטגוריה: "+str(category)+"\nמצב הפריט: "+str(state)+"\n")

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
@restricted
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
    context.bot.send_message(chat_id, msg)

@restricted
def clear_images(update, context):
    chat_id = update.effective_message.chat_id
    msg = "כל התמונות נמחקו, אנא עדכנו תמונות חדשות על ידי העלאה לצאט."
    x = db.images.delete_many({})
    context.bot.send_message(chat_id, msg)

@restricted
def listimages(update, context):

    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id
    message_types = ['photo', 'video']
    upload_date = update.effective_message.date
    caption = update.message.caption
    #caption = caption.lower()

    #if helpers.effective_message_type(update.message) in message_types:
    if caption == "logo":
        res = db.logo.delete_many({})
        update.message.reply_text(" תמונת לוגו התקבלה!")
        file_id = update.message.photo[0].file_id
        current_time = datetime.datetime.utcnow()
        context.bot.send_message(chat_id, str(upload_date))
        context.bot.send_message(chat_id, file_id)
        context.bot.send_photo(chat_id, file_id)
        context.bot.send_message(chat_id, str(caption))

        cursor = db.images.find({})
        for img in cursor:
            if img['PhotoCode'] == "logo":
                res = db.logo.delete_many({})
                pass
            elif db.images.count() == 0:
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
            "PhotoCode":image_code,
            "ImageDate":date

        }
        db.logo.insert_one(imageItem)

    else:

        file_id = update.message.photo[0].file_id
        current_time = datetime.datetime.utcnow()
        context.bot.send_message(chat_id, str(upload_date))
        context.bot.send_message(chat_id, file_id)
        context.bot.send_photo(chat_id, file_id)
        context.bot.send_message(chat_id, str(caption))

    cursor = db.images.find({})
    for img in cursor:
        if img['PhotoCode'] == "p1":
            image_code = "p2"
            pass
        elif img['PhotoCode'] == "p2":
            image_code = "p3"
            pass
        elif img['PhotoCode'] == "p3":
            image_code = "p4"
            pass
        elif img['PhotoCode'] == "p4":
            image_code = "p1"
            pass
        elif img['PhotoCode'] == "":
            image_code = "p1"

    if db.images.count() == 0:
        image_code = "p1"

    userId = str(user_id)
    date = str(upload_date)
    imgId = str(file_id)
    cap = str(caption)
    imageItem = {
        "UserId":user_id,
        "ImageId":imgId,
        "ImageText":cap,
        "PhotoCode":image_code,
        "ImageDate":date

    }
    db.images.insert_one(imageItem)

def main():


    dp.add_handler(CommandHandler('start', start, pass_args=True))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    dp.add_handler(CommandHandler('admin', admin))
    dp.add_handler(CommandHandler('getlist', getlist))
    dp.add_handler(CommandHandler('setitem', setitem))
    dp.add_handler(CommandHandler('total', total))
    dp.add_handler(CommandHandler('clear', clear_images))
    dp.add_handler(CommandHandler('delete', delete))
    dp.add_handler(CommandHandler('approve', approve))
    dp.add_handler(CommandHandler('showlist', showlist))
    dp.add_handler(CommandHandler('setcategory', setcategory))
    dp.add_handler(CommandHandler('categories', categories))

    dp.add_handler(CommandHandler('catmenu', catmenu))

    show_data_handler = CommandHandler('show_data', show_data)
    dp.add_handler(show_data_handler)
    dp.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(new_item, pattern="^restart|start$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(MessageHandler(Filters.document.category("video/mp4") | Filters.document.category("video") | Filters.video, upload_video, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(MessageHandler(Filters.photo, upload_photo, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))


    dp.add_handler(MessageHandler(Filters.photo, listimages))

    dp.add_handler(MessageHandler(Filters.user('@bottwoilbot') and Filters.entity(MessageEntity.TEXT_LINK) and (Filters.entity(MessageEntity.URL)) and (Filters.text | Filters.video | Filters.photo | Filters.document), all_messages))

    dp.add_handler(MessageHandler(Filters.command, unknown))  
    dp.add_error_handler(error)

    ######## SEARCH MENU HANDLER ################################

    cursor = db.buttons.find({})
    for btn in cursor:
        word = str(btn['ButtonCb'])
        dp.add_handler(CallbackQueryHandler(search, pattern=word, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))

    dp.add_handler(CallbackQueryHandler(workshop, pattern="cb_date1", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(workshop, pattern="cb_date2", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(workshop, pattern="cb_date3", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(productsmenu, pattern="cb_products", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(water, pattern="cb_water", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(live, pattern="cb_live", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(bluelight, pattern="cb_blue", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(help, pattern="cb_help", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(myposts, pattern="cb_myposts", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(getlist, pattern="cb_latest", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(mainmenu, pattern="cb_back", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))


    ## BIO MENU ITEMS DP ###
    dp.add_handler(CallbackQueryHandler(bio, pattern="cb_bio", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_session", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_org", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_health", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_body", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_todo", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_screen", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="radiation", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_crystal", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_cleaner", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_digital", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(article, pattern="cb_screen", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))


    ## PRODUCTS CALLBACKS ####
    dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_uvexround", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_uvexsq", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_uvexlow", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_redlight", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_iristech", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_raoptics", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    #dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_blueblox", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    #dp.add_handler(CallbackQueryHandler(showlist, pattern="cb_blueblock", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(showlist, pattern="screen", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))

    dp.add_handler(CallbackQueryHandler(purchase_item, pattern="cb_purchase", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(approve_order, pattern="approve_order", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(handle_bio_menu, pattern="cb_order_bio", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    dp.add_handler(CallbackQueryHandler(pmenu, pattern="pmenu", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
