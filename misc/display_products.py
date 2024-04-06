# def display_products(update, context):
#     query = update.callback_query.data

#     chat_id = update.message.chat_id
#     user_id = update.message.from_user.id
#     username = update.message.from_user.username
#     message_date = update.message.date
#     message_id = update.message.message_id
#     text = update.message.text



#     item = {
#         "MessageId":message_id,
#         "MessageText":text
#     }

#     if db.images.count_documents({'MessageId': message_id}, limit=1) > 0:
#         print("הודעה רשומה כבר!" + str(message_id))
#         pass
#     else:
#         db.messages.insert_one(item)
#         print("ההודעה נשמרה ;-)" + str(message_id))

#     PhotoId = ""
#     imageText = ""
#     imageDate = ""

#     for image in db.images.find({}):

#         PhotoId = image['PhotoId']
#         imageText = image['ImageText']
#         imageDate = image['ImageDate']
#         #print(imageUrl)

#         msg = emojize(" :key: קוד בחירה: "+str(imageText)+"\n" + " :watch: פורסם בתאריך: " +str(imageDate)+"\n")
#         #time.sleep(1)
#         #context.bot.send_message(chat_id, text=msg, timeout=30)

#         #bot.send_media_group(chat_id, img)

#         update.message.send_photo(chat_id, photo=img, caption=msg, timeout=60)
