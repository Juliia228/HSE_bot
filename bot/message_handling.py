from telebot import types
from functions import update_from
from functions import update_in
from functions import print_requests_to_chat
from functions import print_request_to_chats
from functions import check_index
from functions import check
from functions import select_corps
from functions import bot

def chat_functions(message):
    bd, chats = update_from()
    if str(message.chat.id) not in chats:
        if message.text[:4] == "/add":
            chats.append(str(message.chat.id))
            update_in(bd, chats)
            bot.send_message(message.chat.id, "Чат успешно добавлен")
            functions = 'Функции бота:\n"/help" - список функций бота\n"/print" - напишите, чтобы увидеть список ' \
                        'всех текущих запросов от пользователей\n"/delX" - напишите, чтобы удалить запрос под ' \
                        'номером X из списка текущих запросов, если эту проблему кто-то решает или уже решил. Пример ' \
                        'вызова данной функции: /del2 - удалится второй запрос\n\nС вопросами и предложениями писать @iuliia_kom'
            bot.send_message(message.chat.id, functions)
        else:
            bot.send_message(message.chat.id, "Добавьте данный чат в рассылку специальной командой")

    elif message.text[:5] == "/help":
        functions = 'Функции бота:\n"/help" - список функций бота\n"/print" - напишите, чтобы увидеть список ' \
                    'всех текущих запросов от пользователей\n"/delX" - напишите, чтобы удалить запрос под ' \
                    'номером X из списка текущих запросов, если эту проблему кто-то решает или уже решил. Пример ' \
                    'вызова данной функции: /del2 - удалится второй запрос\n\nС вопросами и предложениями писать @iuliia_kom'
        bot.send_message(message.chat.id, functions)

    elif message.text[:6] == "/print":
        reply = 'Текущие запросы:\n'
        print_requests_to_chat(message.chat.id, reply)

    elif message.text[:4] == "/del":
        text = message.text[4:]
        if text[-1] == ' ':
            text = text[:len(text) - 1]
        if text[0] == ' ':
            text = text[1:]
        try:
            index = int(text)
            ind = 1
            flag = True
            for i in list(bd.keys()):
                if flag:
                    for j in range(3, len(bd[i])):
                        if bd[i][j][-1]:
                            if ind == index:
                                if len(bd[i]) > 4:
                                    bd[i].pop(j)
                                    flag = False
                                    break
                                elif len(bd[i]) == 4:
                                    bd.pop(i, None)
                                    flag = False
                                    break
                            ind += 1
                else:
                    break
            update_in(bd, chats)
            reply = 'Текущие запросы после удаления:\n'
            for chat in chats:
                print_requests_to_chat(chat, reply)
        except ValueError:
            bot.send_message(message.chat.id, 'Неверная команда')

def make_request(message):
    bd, chats = update_from()
    if message.text[:6] in ["/start", "Привет", "привет"]:
        exist = check_index(str(message.from_user.id))
        bd, chats = update_from()
        if exist:
            if not bd[str(message.from_user.id)][-1][-1]:
                bd[str(message.from_user.id)][-1][-1] = True
                update_in(bd, chats)
                print_request_to_chats(str(message.from_user.id))
            bd[str(message.from_user.id)].append(['', '', '', False])
        bot.send_message(message.chat.id, "Здравствуйте!")
        bd[str(message.from_user.id)][2] = 'korp'
        select_corps(message)

    elif str(message.from_user.id) in bd:
        if bd[str(message.from_user.id)][-1][1] == '':  # аудитория
            bd[str(message.from_user.id)][-1][1] = message.text
            if bd[str(message.from_user.id)][2] == 'change':
                bd[str(message.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(message.from_user.id), message)
            elif bd[str(message.from_user.id)][0] == '':
                bot.send_message(message.chat.id, "Введите ваши ФИО одним сообщением")
            else:
                bot.send_message(message.chat.id, "Опишите проблему одним сообщением")
        elif bd[str(message.from_user.id)][0] == '':  # фио
            bd[str(message.from_user.id)][0] = message.text
            if bd[str(message.from_user.id)][2] == 'change':
                bd[str(message.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(message.from_user.id), message)
            else:
                bot.send_message(message.chat.id, "Введите ваш номер телефона")
        elif bd[str(message.from_user.id)][1] == '':  # телефон
            bd[str(message.from_user.id)][1] = message.text
            if bd[str(message.from_user.id)][2] == 'change':
                bd[str(message.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(message.from_user.id), message)
            else:
                bot.send_message(message.chat.id, "Опишите проблему одним сообщением")
        elif bd[str(message.from_user.id)][-1][2] == '':  # описание проблемы
            bd[str(message.from_user.id)][-1][2] = message.text
            bd[str(message.from_user.id)][2] = 'check'
            update_in(bd, chats)
            check(str(message.from_user.id), message)
        else:
            bot.send_message(message.chat.id, "Чтобы добавить запрос, напишите привет или /start")
    else:
        bot.send_message(message.chat.id, "Чтобы добавить запрос, напишите привет или /start")
    update_in(bd, chats)


def handle_call(call):
    bd, chats = update_from()
    if bd[str(call.from_user.id)][2] == 'korp':
        if call.data == 'rod':
            bd[str(call.from_user.id)][-1][0] = 'Родионова, 136'
            if bd[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                bd[str(call.from_user.id)][2] = ''
            else:  # изменяем
                bd[str(call.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'bp':
            bd[str(call.from_user.id)][-1][0] = 'Большая Печёрская, 25/12'
            if bd[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                bd[str(call.from_user.id)][2] = ''
            else:  # изменяем
                bd[str(call.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'kos':
            bd[str(call.from_user.id)][-1][0] = 'Костина, 2'
            if bd[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                bd[str(call.from_user.id)][2] = ''
            else:  # изменяем
                bd[str(call.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'lvov':
            bd[str(call.from_user.id)][-1][0] = 'Львовская, 1В'
            if bd[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                bd[str(call.from_user.id)][2] = ''
            else:  # изменяем
                bd[str(call.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'sorm':
            bd[str(call.from_user.id)][-1][0] = 'Сормовское шоссе, 30'
            if bd[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                bd[str(call.from_user.id)][2] = ''
            else:  # изменяем
                bd[str(call.from_user.id)][2] = 'check'
                update_in(bd, chats)
                check(str(call.from_user.id), call.message)

    elif bd[str(call.from_user.id)][2] == 'check':
        if call.data == 'yes':
            bd[str(call.from_user.id)][-1][-1] = True
            bd[str(call.from_user.id)][2] = ''
            bot.send_message(call.message.chat.id, "Ответ записан")
            update_in(bd, chats)
            print_request_to_chats(str(call.from_user.id))
        elif call.data == 'no':
            bd[str(call.from_user.id)][2] = 'change'
            keyboard = types.InlineKeyboardMarkup()
            key1 = types.InlineKeyboardButton(text='Корпус', callback_data='korp')
            keyboard.add(key1)
            key2 = types.InlineKeyboardButton(text='Аудиторию', callback_data='aud')
            keyboard.add(key2)
            key3 = types.InlineKeyboardButton(text='Описание проблемы', callback_data='probl')
            keyboard.add(key3)
            key4 = types.InlineKeyboardButton(text='ФИО', callback_data='fio')
            keyboard.add(key4)
            key5 = types.InlineKeyboardButton(text='Номер телефона', callback_data='phone')
            keyboard.add(key5)
            bot.send_message(call.message.chat.id, text="Выберите, что хотите изменить", reply_markup=keyboard)

    elif bd[str(call.from_user.id)][2] == 'change':
        if call.data == 'korp':
            bd[str(call.from_user.id)][2] = 'korp'
            select_corps(call.message)
        elif call.data == 'aud':
            bd[str(call.from_user.id)][-1][1] = ''
            bot.send_message(call.message.chat.id, text="Введите аудиторию")
        elif call.data == 'probl':
            bd[str(call.from_user.id)][-1][2] = ''
            bot.send_message(call.message.chat.id, "Опишите проблему одним сообщением")
        elif call.data == 'fio':
            bd[str(call.from_user.id)][0] = ''
            bot.send_message(call.message.chat.id, "Введите ваши ФИО одним сообщением")
        elif call.data == 'phone':
            bd[str(call.from_user.id)][1] = ''
            bot.send_message(call.message.chat.id, "Введите ваш номер телефона")
    update_in(bd, chats)
