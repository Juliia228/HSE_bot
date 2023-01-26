import json
from message_handling import chat_functions
from message_handling import make_request
from message_handling import handle_call
from functions import update_from
from functions import bot

requests = {}
chats = []
with open('requests.json', 'w+') as file:
    json.dump(requests, file)
with open('chats_of_staff.json', 'w+') as file:
    json.dump(chats, file)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
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

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    requests, chats = update_from()
    if str(call.from_user.id) in requests:
        try:
            handle_call(call)
        except:
            bot.send_message(call.message.chat.id, text='Неверный запрос. Если вы думаете, что произошла ошибка, сообщите о ней @iuliia_kom')

bot.polling(none_stop=True, interval=0)