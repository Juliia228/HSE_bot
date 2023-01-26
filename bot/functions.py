import json
import telebot
from telebot import types
from bot_token import token

bot = telebot.TeleBot(token)

def check_index(index):
    requests, chats = update_from()
    for i in list(requests.keys()):
        if i == index:
            return True
    requests[index] = ['', '', '', ['', '', '', False]]  # ['фио', 'телефон', что ждем на ввод, ['корпус', 'аудитория', 'описание проблемы', True-запрос дописан/False- не дописан], ['корпус', 'аудитория', 'описание проблемы', True-запрос дописан/False- не дописан], ...]
    update_in(requests, chats)
    return False

def check(attribute1, attribute2):
    requests, chats = update_from()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Проблема возникла по адресу ' + requests[attribute1][-1][0] + ' в аудитории ' + requests[attribute1][-1][1] + \
               ', ее описание следующее: "' + requests[attribute1][-1][2] + '", а ваши контактные данные: ' + requests[attribute1][0] + \
               ', ' + requests[attribute1][1] + '?'
    bot.send_message(attribute2.chat.id, text=question, reply_markup=keyboard)

def select_corps(attribute2):
    keyboard = types.InlineKeyboardMarkup()
    key_rod = types.InlineKeyboardButton(text='Родионова, 136', callback_data='rod')
    keyboard.add(key_rod)
    key_bp = types.InlineKeyboardButton(text='Большая Печёрская, 25/12', callback_data='bp')
    keyboard.add(key_bp)
    key_kos = types.InlineKeyboardButton(text='Костина, 2', callback_data='kos')
    keyboard.add(key_kos)
    key_lvov = types.InlineKeyboardButton(text='Львовская, 1В', callback_data='lvov')
    keyboard.add(key_lvov)
    key_sorm = types.InlineKeyboardButton(text='Сормовское шоссе, 30', callback_data='sorm')
    keyboard.add(key_sorm)
    bot.send_message(attribute2, text="Выберите корпус", reply_markup=keyboard)

def print_requests_to_chat(id, text):
    requests, chats = update_from()
    cur_ind = 1
    for i in list(requests.keys()):
        for j in range(3, len(requests[i])):
            if requests[i][j][-1]:
                text += str(cur_ind) + ') ' + requests[i][0] + ' ' + requests[i][1] + '\nКорпус: ' + requests[i][j][0] + \
                        ', аудитория: ' + requests[i][j][1] + ', проблема: ' + requests[i][j][2] + '\n'
                cur_ind += 1
    bot.send_message(id, text)

    count_of_requests = 0
    for i in list(requests.keys()):
        count_of_requests += (len(requests[i]) - 3)

    if count_of_requests > 30:
        bot.send_message(id, text="Во избежание зависания бота, удалите некоторые запросы. "
                                   "Чтобы посмотреть все запросы, напишите /print")

def print_request_to_chats(id):
    requests, chats = update_from()
    request = requests[id][0] + ' ' + requests[id][1] + '\nКорпус: ' + requests[id][-1][0] + \
              ', аудитория: ' + requests[id][-1][1] + ', проблема: ' + requests[id][-1][2] + '\n'

    count_of_requests = 0
    for i in list(requests.keys()):
        count_of_requests += (len(requests[i]) - 3)

    for chat in chats:
        bot.send_message(chat, text="Добавлен новый запрос")
        bot.send_message(chat, text=request)
        if count_of_requests > 30:
            bot.send_message(chat, text="Во избежание зависания бота, удалите некоторые запросы. "
                                   "Чтобы посмотреть все запросы, напишите /print")

def update_from():
    with open('requests.json', mode='r') as file:
        requests = json.load(file)
    with open('chats_of_staff.json', mode='r') as file:
        chats = json.load(file)
    return requests, chats

def update_in(requests, chats):
    with open('requests.json', mode='w') as file:
        json.dump(requests, file)
    with open('chats_of_staff.json', mode='w') as file:
        json.dump(chats, file)
