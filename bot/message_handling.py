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
    requests, chats = update_from()
    if str(message.chat.id) not in chats:
        if message.text[:4] == "/add":
            chats.append(str(message.chat.id))
            update_in(requests, chats)
            bot.send_message(message.chat.id, text="Чат успешно добавлен")
            functions = 'Функции бота:\n"/help" - список функций бота\n"/print" - напишите, чтобы увидеть список ' \
                        'всех текущих запросов от пользователей. Если бот пришлёт не все фотографии, прикрепленные к ' \
                        'запросам, вызовите эту функцию ещё раз\n"/delX" - напишите, чтобы удалить запрос под ' \
                        'номером X из списка текущих запросов, если эту проблему кто-то решает или уже решил. Пример ' \
                        'вызова данной функции: /del2 - удалится второй запрос\n\nПо вопросам и предложениям ' \
                        'обращайтесь к @iuliia_kom'
            bot.send_message(message.chat.id, text=functions)
        else:
            bot.send_message(message.chat.id, text="Добавьте данный чат в рассылку специальной командой")

    elif message.text[:5] == "/help":
        functions = 'Функции бота:\n"/help" - список функций бота\n"/print" - напишите, чтобы увидеть список ' \
                    'всех текущих запросов от пользователей. Если бот пришлёт не все фотографии, прикрепленные к ' \
                    'запросам, вызовите эту функцию ещё раз\n"/delX" - напишите, чтобы удалить запрос под ' \
                    'номером X из списка текущих запросов, если эту проблему кто-то решает или уже решил. Пример ' \
                    'вызова данной функции: /del2 - удалится второй запрос\n\nПо вопросам и предложениям ' \
                    'обращайтесь к @iuliia_kom'
        bot.send_message(message.chat.id, text=functions)

    elif message.text[:6] == "/print":
        reply = '*Текущие запросы:*\n'
        print_requests_to_chat(message.chat.id, reply)

    elif message.text[:4] == "/del":
        number = message.text[4:]
        if number[-1] == ' ':
            number = number[:len(number) - 1]
        if number[0] == ' ':
            number = number[1:]
        try:
            index = int(number)
            cur_ind = 1
            flag = True
            for i in list(requests.keys()):
                if flag:
                    for j in range(3, len(requests[i])):
                        if requests[i][j][-1]:
                            if cur_ind == index:
                                if len(requests[i]) > 4:
                                    requests[i].pop(j)
                                    flag = False
                                    break
                                elif len(requests[i]) == 4:
                                    requests.pop(i, None)
                                    flag = False
                                    break
                            cur_ind += 1
                else:
                    break
            update_in(requests, chats)
            reply = '*Текущие запросы после удаления:*\n'
            for chat in chats:
                print_requests_to_chat(chat, reply)
        except ValueError:
            bot.send_message(message.chat.id, text='Неверная команда')

def make_request(message):
    requests, chats = update_from()
    if message.text[:6] in ["/start", "Привет", "привет", "start"]:
        bot.send_message(message.chat.id, text="*Привет!*\nНа связи бот технической поддержки сотрудников НИУ ВШЭ - "
                                               "Нижний Новгород.\nЗаполните информационные поля, чтобы отправить запрос!", parse_mode="Markdown")
        exist = check_index(str(message.from_user.id))
        requests, chats = update_from()
        if exist:
            if not requests[str(message.from_user.id)][-1][-1]:
                requests[str(message.from_user.id)][-1][-1] = True
                update_in(requests, chats)
                print_request_to_chats(str(message.from_user.id))
            requests[str(message.from_user.id)].append(['', '', '', [], False])
        requests[str(message.from_user.id)][2] = 'korp'
        update_in(requests, chats)
        select_corps(message.chat.id)

    elif requests[str(message.from_user.id)][2] == 'del_photo':
        index = int(message.text) - 1
        requests[str(message.from_user.id)][-1][3].pop(index)
        bot.send_message(message.chat.id, text="Фото удалено")
        requests[str(message.from_user.id)][2] = 'check'
        update_in(requests, chats)
        check(str(message.from_user.id), message)

    elif str(message.from_user.id) in requests and requests[str(message.from_user.id)][2] != 'korp':
        if requests[str(message.from_user.id)][-1][1] == '':
            requests[str(message.from_user.id)][-1][1] = message.text
            if requests[str(message.from_user.id)][2] == 'change':
                requests[str(message.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(message.from_user.id), message)
            elif requests[str(message.from_user.id)][0] == '':
                bot.send_message(message.chat.id, text="Введите ваши ФИО одним сообщением")
            else:
                bot.send_message(message.chat.id, text="Опишите проблему одним сообщением")
        elif requests[str(message.from_user.id)][0] == '':
            requests[str(message.from_user.id)][0] = message.text
            if requests[str(message.from_user.id)][2] == 'change':
                requests[str(message.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(message.from_user.id), message)
            else:
                bot.send_message(message.chat.id, text="Введите ваш номер телефона")
        elif requests[str(message.from_user.id)][1] == '':
            requests[str(message.from_user.id)][1] = message.text
            if requests[str(message.from_user.id)][2] == 'change':
                requests[str(message.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(message.from_user.id), message)
            else:
                bot.send_message(message.chat.id, text="Опишите проблему одним сообщением")
        elif requests[str(message.from_user.id)][-1][2] == '':
            requests[str(message.from_user.id)][-1][2] = message.text
            if requests[str(message.from_user.id)][2] == 'change':
                requests[str(message.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(message.from_user.id), message)
            else:
                requests[str(message.from_user.id)][2] = 'photo'
                update_in(requests, chats)
                keyboard = types.InlineKeyboardMarkup()
                key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
                keyboard.add(key_yes)
                key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
                keyboard.add(key_no)
                bot.send_message(message.chat.id, text="Вы можете прислать фото, чтобы ускорить решение вашей проблемы. "
                                                       "Хотите сделать это?", reply_markup=keyboard)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_button = types.KeyboardButton(text="start")
            markup.add(start_button)
            bot.send_message(message.chat.id, text="Чтобы добавить запрос, напишите привет или нажмите на кнопку start",
                             reply_markup=markup)
        update_in(requests, chats)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton(text="start")
        markup.add(start_button)
        bot.send_message(message.chat.id, text="Чтобы добавить запрос, напишите привет или нажмите на кнопку start",
                         reply_markup=markup)

def get_photo(message):
    requests, chats = update_from()
    fileID = message.photo[-1].file_id
    requests[str(message.from_user.id)][-1][3].append(fileID)
    requests[str(message.from_user.id)][2] = 'photo'
    update_in(requests, chats)

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.chat.id, text='Хотите добавить еще одно фото?', reply_markup=keyboard)

def handle_call(call):
    requests, chats = update_from()
    if requests[str(call.from_user.id)][2] == 'korp':
        if call.data == 'rod':
            requests[str(call.from_user.id)][-1][0] = 'Родионова, 136'
            if requests[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                requests[str(call.from_user.id)][2] = ''
            else:
                requests[str(call.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'bp':
            requests[str(call.from_user.id)][-1][0] = 'Большая Печёрская, 25/12'
            if requests[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                requests[str(call.from_user.id)][2] = ''
            else:
                requests[str(call.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'kos':
            requests[str(call.from_user.id)][-1][0] = 'Костина, 2'
            if requests[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                requests[str(call.from_user.id)][2] = ''
            else:
                requests[str(call.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'lvov':
            requests[str(call.from_user.id)][-1][0] = 'Львовская, 1В'
            if requests[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                requests[str(call.from_user.id)][2] = ''
            else:
                requests[str(call.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(call.from_user.id), call.message)
        elif call.data == 'sorm':
            requests[str(call.from_user.id)][-1][0] = 'Сормовское шоссе, 30'
            if requests[str(call.from_user.id)][-1][1] == '':
                bot.send_message(call.message.chat.id, text="Теперь введите аудиторию")
                requests[str(call.from_user.id)][2] = ''
            else:
                requests[str(call.from_user.id)][2] = 'check'
                update_in(requests, chats)
                check(str(call.from_user.id), call.message)
        update_in(requests, chats)

    elif requests[str(call.from_user.id)][2] == 'check':
        if call.data == 'yes':
            requests[str(call.from_user.id)][-1][-1] = True
            requests[str(call.from_user.id)][2] = ''
            update_in(requests, chats)
            bot.send_message(call.message.chat.id, text="Ответ записан")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_button = types.KeyboardButton(text="start")
            markup.add(start_button)
            bot.send_message(call.message.chat.id, text="Чтобы добавить еще один запрос, напишите привет или нажмите "
                                                        "на кнопку start", reply_markup=markup)
            print_request_to_chats(str(call.from_user.id))
        elif call.data == 'no':
            requests[str(call.from_user.id)][2] = 'change'
            update_in(requests, chats)
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
            key6 = types.InlineKeyboardButton(text='Фото', callback_data='photo')
            keyboard.add(key6)
            bot.send_message(call.message.chat.id, text="Выберите, что хотите изменить", reply_markup=keyboard)

    elif requests[str(call.from_user.id)][2] == 'change':
        if call.data == 'korp':
            requests[str(call.from_user.id)][2] = 'korp'
            select_corps(call.message.chat.id)
        elif call.data == 'aud':
            requests[str(call.from_user.id)][-1][1] = ''
            bot.send_message(call.message.chat.id, text="Введите аудиторию")
        elif call.data == 'probl':
            requests[str(call.from_user.id)][-1][2] = ''
            bot.send_message(call.message.chat.id, text="Опишите проблему одним сообщением")
        elif call.data == 'fio':
            requests[str(call.from_user.id)][0] = ''
            bot.send_message(call.message.chat.id, text="Введите ваши ФИО одним сообщением")
        elif call.data == 'phone':
            requests[str(call.from_user.id)][1] = ''
            bot.send_message(call.message.chat.id, text="Введите ваш номер телефона")
        elif call.data == 'photo':
            keyboard = types.InlineKeyboardMarkup()
            key1 = types.InlineKeyboardButton(text='Удалить фото', callback_data='delete_photo')
            keyboard.add(key1)
            key2 = types.InlineKeyboardButton(text='Добавить еще фото', callback_data='add_photo')
            keyboard.add(key2)
            bot.send_message(call.message.chat.id, text="Выберите, что хотите сделать", reply_markup=keyboard)
        elif call.data == 'delete_photo':
            requests[str(call.from_user.id)][2] = 'del_photo'
            bot.send_message(call.message.chat.id, text="Напишите номер фотографии, которую хотите удалить")
            for i in range(len(requests[str(call.from_user.id)][-1][3])):
                fileID = requests[str(call.from_user.id)][-1][3][i]
                file_info = bot.get_file(fileID)
                file = bot.download_file(file_info.file_path)
                bot.send_photo(call.message.chat.id, file, str(i+1))
        elif call.data == 'add_photo':
            bot.send_message(call.message.chat.id, text="Пришлите еще одно фото")
            requests[str(call.from_user.id)][2] = 'photo'
        update_in(requests, chats)

    elif requests[str(call.from_user.id)][2] == 'photo':
        if call.data == 'yes':
            if requests[str(call.from_user.id)][-1][3] == []:
                bot.send_message(call.message.chat.id, text="Присылайте фотографии по одной")
            else:
                bot.send_message(call.message.chat.id, text="Пришлите еще одно фото")
        elif call.data == 'no':
            requests[str(call.from_user.id)][2] = 'check'
            update_in(requests, chats)
            check(str(call.from_user.id), call.message)
