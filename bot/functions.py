import json
import telebot
from telebot import types
from bot_token import token

bot = telebot.TeleBot(token)

def check_index(index):
    bd, chats = update_from()
    for i in list(bd.keys()):
        if i == index:
            return True
    bd[index] = ['', '', '', ['', '', '', False]]  # ['фио', 'телефон', что ждем на ввод, ['корпус', 'аудитория', 'описание проблемы', True-запрос дописан/False- не дописан], ['корпус', 'аудитория', 'описание проблемы', True-запрос дописан/False- не дописан], ...]
    update_in(bd, chats)
    return False

def check(atr1, atr2):
    bd, chats = update_from()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Проблема возникла по адресу ' + bd[atr1][-1][0] + ' в аудитории ' + bd[atr1][-1][1] + \
               ', ее описание следующее: "' + bd[atr1][-1][2] + '", а ваши контактные данные: ' + bd[atr1][0] + \
               ', ' + bd[atr1][1] + '?'
    bot.send_message(atr2.chat.id, text=question, reply_markup=keyboard)

def select_corps(atr2):
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
    bot.send_message(atr2.chat.id, text="Выберите корпус", reply_markup=keyboard)

def print_requests_to_chat(id, text):
    bd, chats = update_from()
    ind = 1
    for i in list(bd.keys()):
        for j in range(3, len(bd[i])):
            if bd[i][j][-1]:
                text += str(ind) + ') ' + bd[i][0] + ' ' + bd[i][1] + '\nКорпус: ' + bd[i][j][0] + \
                        ', аудитория: ' + bd[i][j][1] + ', проблема: ' + bd[i][j][2] + '\n'
                ind += 1
    bot.send_message(id, text)

    count_of_requests = 0  # количество запросов
    for i in list(bd.keys()):
        count_of_requests += (len(bd[i]) - 3)

    if count_of_requests > 30:
        bot.send_message(id, "Во избежание зависания бота, удалите некоторые запросы. "
                                   "Чтобы посмотреть все запросы, напишите /print")

def print_request_to_chats(id):
    bd, chats = update_from()
    request = bd[id][0] + ' ' + bd[id][1] + '\nКорпус: ' + bd[id][-1][0] + \
              ', аудитория: ' + bd[id][-1][1] + ', проблема: ' + bd[id][-1][2] + '\n'

    count_of_requests = 0  # количество запросов
    for i in list(bd.keys()):
        count_of_requests += (len(bd[i]) - 3)

    for chat in chats:
        bot.send_message(chat, "Добавлен новый запрос")
        bot.send_message(chat, request)
        if count_of_requests > 30:
            bot.send_message(chat, "Во избежание зависания бота, удалите некоторые запросы. "
                                   "Чтобы посмотреть все запросы, напишите /print")

def update_from():
    with open('requests.json', mode='r') as file:
        bd = json.load(file)
    with open('chats_of_staff.json', mode='r') as file:
        chats = json.load(file)
    return bd, chats

def update_in(bd, chats):
    with open('requests.json', mode='w') as file:
        json.dump(bd, file)
    with open('chats_of_staff.json', mode='w') as file:
        json.dump(chats, file)
