import json
import os.path
from message_handling import chat_functions
from message_handling import make_request
from message_handling import handle_call
from message_handling import get_photo
from functions import update_from
from functions import bot

if not(os.path.exists('requests.json')) or os.path.getsize('requests.json') == 0:
    requests = {}
    with open('requests.json', 'w+') as file:
        json.dump(requests, file)

if not(os.path.exists('chats_of_staff.json')) or os.path.getsize('chats_of_staff.json') == 0:
    chats = []
    with open('chats_of_staff.json', 'w+') as file:
        json.dump(chats, file)

@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group':
        try:
            chat_functions(message)
        except:
            bot.send_message(message.chat.id, text='Неверный запрос. Если вы думаете, что произошла ошибка, сообщите о ней @iuliia_kom')
    elif message.chat.type == 'private':
        try:
            make_request(message)
        except:
            bot.send_message(message.chat.id, text='Неверный запрос. Если вы думаете, что произошла ошибка, сообщите о ней @iuliia_kom')
    else:
        bot.send_message(message.chat.id, text='Неверный запрос. Если вы думаете, что произошла ошибка, сообщите о ней @iuliia_kom')

@bot.message_handler(content_types=['photo'])
def photo_messages(message):
    requests, chats = update_from()
    if message.chat.type == 'private' and str(message.from_user.id) in requests:
        try:
            get_photo(message)
        except:
            bot.send_message(message.chat.id, text='Неверный запрос. Если вы думаете, что произошла ошибка, сообщите о ней @iuliia_kom')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    requests, chats = update_from()
    if str(call.from_user.id) in requests:
        try:
            handle_call(call)
        except:
            bot.send_message(call.message.chat.id, text='Неверный запрос. Если вы думаете, что произошла ошибка, сообщите о ней @iuliia_kom')

bot.polling(none_stop=True, interval=0)