from databese import *
import telebot
import config
room = 0
# conctants
bot = telebot.TeleBot(config.tg_api_key)
group_id = config.test_id
create_table()

'''----bot commands----'''
@bot.message_handler(commands=["start"])
# func for command /start: Starts user registration
def start(message):
    chat_id = message.chat.id
    if str(chat_id)[:4] == "-100":
        bot.send_message(chat_id, f'@{message.from_user.username}, скажи, пожалуйста, номер своей комнаты🙏')
    else:
        bot.send_message(chat_id, '''Привет! Скажи, пожалуйста, номер своей комнаты🙏''')


@bot.message_handler(commands=["corridor_warning"])
# func for command /corridor_warning: Creates a selection of points in corridor
def corridor_warning(message):
    chat_id = message.chat.id
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    # create buttons for markup
    ledder_left = telebot.types.InlineKeyboardButton("Левая лестница", callback_data="ledder_left")
    ledder_right = telebot.types.InlineKeyboardButton("Правая лестница", callback_data="ledder_right")
    coller = telebot.types.InlineKeyboardButton("Кулер", callback_data="coller")
    # create markup
    markup.add(ledder_left, coller, ledder_right)
    # send message
    bot.send_message(chat_id, "Выберете место в коридоре, где находятся вожатые", reply_markup=markup)


@bot.message_handler(commands=['warning'])
# func for command /warning: Creates a warning mailinh list for group and messages
def warning(message):
    global room
    chat_id = message.chat.id
    username = message.from_user.username
    usernames = getUserFromDB()
    print(usernames)
    if chat_id != group_id:  # Если сообщение не из группы
        room = getRoomByID(chat_id)
    else:  # Если сообщение из группы
        room = getRoomByUsername(username) if username else "неизвестной"

    if room:
        char = ''
        for name_tuple in usernames:
            if name_tuple[0]:
                for name in name_tuple:
                    char += f'@{name}, '
        bot.send_message(group_id, f'''Вожатые в {room} комнате, {char[:-2]}!''')
        

        chat_list = getIDsFromDB()
        for id in chat_list:
            bot.send_message(id, f'''Вожатые в {room} комнате!''')
    else:
        bot.send_message(chat_id, "Не удалось определить комнату")


@bot.message_handler(commands=["show_3_floor"])
def show_3_floor(message):
    global room
    # room = 314
    chat_id = message.chat.id
    if str(chat_id)[:4] == "-100":
        username = message.from_user.username
        bot.send_photo(chat_id, open(f"3_floor\\{room}.jpg","rb"), caption=f"@{username}, лови)")
    else:
        bot.send_photo(chat_id, open(f"3_floor\\{room}.jpg","rb"), caption="Лови)")
        bot.send_message(chat_id, "Если что, красный кружок — это и есть местоположение вожатых")


'''----callback handler by corridor----'''
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global room
    current_place = ""
    if call.message:
        match call.data:
            case "ledder_left":
                current_place = "левой лестницы"
            case "coller":
                current_place = "кулера"
            case "ledder_right":
                current_place = "правой лестницы"
        bot.delete_message(group_id,
                           message_id=call.message.message_id)
        usernames = getUserFromDB()
        for name in usernames:
            if name[0]:  # Проверяем, что username существует
                bot.send_message(group_id, f'''Вожатые у {current_place}, @{name[0]}!''')


'''----message handler----'''
@bot.message_handler(func=lambda message: True, content_types=['text'])
def msg_answer(message):
    global room
    chat_id = message.chat.id
    if str(chat_id)[:4] != "-100":
        chat_list = getIDsFromDB()
        if chat_id in chat_list:
            bot.send_message(chat_id, f'''Ты уже зарегестрирован в боте''')
        else:
            username = message.from_user.username
            room = message.text
            # validation for room
            try:
                int(room)
                if 314 >= int(room) and int(room) >= 300:
                    stack_db(chat_id, username, room)
                    bot.send_message(chat_id, f'''✅ Вы успешно зарегестрированы''')
            except ValueError:
                bot.send_message(chat_id, "Ты ввёл не номер комнаты! Напиши правильно, например, 308")


if __name__ == "__main__":
    bot.infinity_polling()
