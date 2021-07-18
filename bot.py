import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('1835870307:AAHlXuytmI_rtPbjNLj3PzBU3oaeGe7yboY')


# Получение списка администраторов
def get_administrators():
    list = []
    for i in get_db_connection().execute('SELECT * FROM administrators').fetchall():
        list.append(i[1])
    return list


def get_db_connection():
    conn = sqlite3.connect('bot_db')
    conn.row_factory = sqlite3.Row
    return conn


def get_welcome_message():
    information_about_company = get_db_connection().execute('SELECT * FROM welcome')
    text = ''
    for i in information_about_company:
        text = ''.join(i)
    return text

def get_start_message():
    information_about_company = get_db_connection().execute('SELECT * FROM start_message')

    for i in information_about_company:
        return i[0]

def send_new_admin(admin):
    conn = sqlite3.connect('bot_db')
    conn.row_factory = sqlite3.Row

    conn.execute('INSERT INTO administrators(admin_id) VALUES  (?) ', (admin, )).fetchall()
    conn.commit()
    conn.close()

def edit_start_message(message):
    try:
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Напишите новый текст стартового сообщения')
        bot.register_next_step_handler(msg, edit_start_message_next_step)
    except:
        bot.send_message(chat_id, 'Что-то пошло не так')


def edit_start_message_next_step(message):
    try:
        conn = sqlite3.connect('bot_db')
        chat_id = message.chat.id
        text = message.text
        conn.execute('UPDATE start_message SET title = (?) WHERE ROWID=1', (text, ))
        conn.commit()
        bot.send_message(chat_id, 'Стартовое сообщение было успешно изменено')
        conn.close()
    except:
        bot.send_message(chat_id, 'Что-то пошло не так')


def edit_information_company(message):
    try:
        chat_id = message.chat.id
        bot.send_message(chat_id, get_welcome_message())
        msg = bot.send_message(chat_id, 'Напишите новый текст приветствия')
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        bot.register_next_step_handler(msg, edit_information_company_next_step)

    except:
        bot.send_message(chat_id, 'Что-то пошло не так')


def edit_information_company_next_step(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE welcome SET title=?', (text,))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, 'Сообщение приветствия было успешно изменено')
    except:
        bot.send_message(chat_id, 'Что-то пошло не так')


def show_last_post():
    list = []
    for i in get_db_connection().execute('SELECT * FROM bot ORDER BY ID DESC LIMIT 1').fetchall():
        for j in range(len(i)):
            list.append(i[j])
    text = f'Название вакансии: {list[1]}\n\n' \
        f'Описание вакансии: {list[2]}\n\n' \
        f'Локализация: {list[3]}\n\n' \
        f'Почасовая ставка: {list[4]}'

    return text


# Редактирование вакансии

id = int

def edit_offer(message):
    try:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Напиши ID поста для редактирования')
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        bot.register_next_step_handler(msg, edit_offer_next_step)
    except:
        bot.send_message(chat_id, 'Что-то пошло не так')


def edit_offer_next_step(message):
    try:
        global id
        chat_id = message.chat.id
        id = message.text
        bot.send_message(chat_id, show_offer(id))
        if message.text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        msg = bot.send_message(chat_id, 'Напиши новое название вакансии:')
        bot.register_next_step_handler(msg, edit_offer_title)
    except:
        bot.send_message(chat_id, 'Какая-то ошибка')


def edit_offer_title(message):
    try:
        global id
        chat_id = message.chat.id
        title = message.text
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        if title.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET title=(?) WHERE id=(?)', (title, id))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Теперь введите описание')
        bot.register_next_step_handler(msg, edit_offer_description)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def edit_offer_description(message):
    try:
        global id
        chat_id = message.chat.id
        text = message.text
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        if text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET description=(?) WHERE id=(?)', (text, id))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Теперь введите местоположение работы')
        bot.register_next_step_handler(msg, edit_offer_location)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def edit_offer_location(message):
    try:
        global id
        chat_id = message.chat.id
        text = message.text
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        if text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET location=(?) WHERE id=(?)', (text, id))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Теперь введите почасову оплату')
        bot.register_next_step_handler(msg, edit_offer_salary)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def edit_offer_salary(message):
    try:
        global id
        chat_id = message.chat.id
        text = message.text
        if text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET salary=(?) WHERE id=(?)', (text, id))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Вакансия была успешно отредактирована')
        id = int
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


# Удаление вакансии
def remove_offer(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, 'Введите ID вакансии, которую хотите удалить')
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        bot.register_next_step_handler(msg, remove_offer_next_step)
    except:
        bot.reply_to(message, 'Что-то пошло не так')


def remove_offer_next_step(message):
    text = message.text
    if text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Действие отменено')
        return
    if not text.isdigit():
        msg = bot.reply_to(message, 'Ошибка. ИД включает в себя только номерные знаки.')
        bot.register_next_step_handler(msg, remove_offer_next_step)
        return
    try:
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('DELETE FROM bot WHERE id = ?', (int(text),))
        conn.commit()
        conn.close()
        msg = bot.reply_to(message, 'Вакансия была успешно удалена', reply_markup=admin_keyboard())
    except:
        msg = bot.reply_to(message, 'Какая-то ошибка')
# конец удаления вакансии


# Добавление новой вакансии
def add_new_offer(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.send_message(chat_id, 'Напишите название новой вакансии: ')
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        bot.register_next_step_handler(msg, add_title)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def add_title(message):
    try:
        chat_id = message.chat.id
        title = message.text
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        if title.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('INSERT INTO bot(title) VALUES (?)', (title,))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Теперь введите описание')
        bot.register_next_step_handler(msg, add_description)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def add_description(message):
    try:
        chat_id = message.chat.id
        description = message.text
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        if description.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET description=(?) where id = (select MAX(id) from bot)', (description,))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Введите местоположение работы')
        bot.register_next_step_handler(msg, add_location)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def add_location(message):
    try:
        chat_id = message.chat.id
        location = message.text
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        if location.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET location=(?) where id = (select MAX(id) from bot)', (location,))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Напишите почасовую ставку для данной вакансии')
        bot.register_next_step_handler(msg, add_salary)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def add_salary(message):
    try:
        chat_id = message.chat.id
        salary = message.text
        if salary.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bot SET salary=(?) where id = (select MAX(id) from bot)', (salary,))
        conn.commit()
        conn.close()
        msg = bot.send_message(chat_id, 'Вакансия была успешно добавлена')
        bot.reply_to(msg, show_last_post())
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


# Получение вакансии
def get_offer(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM bot WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if post is None:
        return 'Nie ma takiej oferty'
    return post


def show_offer(id):
    try:
        list = []
        for i in get_db_connection().execute('SELECT * FROM bot WHERE id = ?', (int(id),)).fetchall():
            for j in range(len(i)):
                list.append(i[j])
                list.append('\n')
        text = ''
        text = ''.join(list[1::])
        return text
    except:
        return


# Добавление нового администратора

def add_admin(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, 'Напишите ID аккаунта, который хотите добавить в администраторы: ')
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        if not text.isdigit():
            msg = bot.reply_to(message, 'Ошибка. ИД включает в себя только номерные знаки.')
            bot.register_next_step_handler(msg, process_age_step)
            return
        try:
            conn = sqlite3.connect('bot_db')
            conn.row_factory = sqlite3.Row
            conn.execute('INSERT INTO administrators(admin_id) VALUES (?)', (int(text),)).fetchall()
            conn.commit()
            conn.close()
            msg = bot.reply_to(message, 'Администратор был успешно добавлен', reply_markup=admin_keyboard())
        except:
            msg = bot.reply_to(message, 'Какая-то ошибка')
    except:
        bot.reply_to(message, 'oooops')
# конец добавлние администратора

# Удаление администратора

def remove_admin(message):
    try:
        chat_id = message.chat.id
        name = message.text
        bot.send_message(message.chat.id, str(get_administrators()))
        msg = bot.reply_to(message, 'Напишите ID аккаунта, который хотите удалить из администраторов: ')
        bot.send_message(chat_id, 'Для отмены напиши \"Отмена\" без кавычек')
        bot.register_next_step_handler(msg, remove_admin_next_step)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так %s' % (e))


def remove_admin_next_step(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text.lower() == 'отмена':
            bot.send_message(chat_id, 'Действие отменено')
            return
        if not text.isdigit():
            msg = bot.reply_to(message, 'Ошибка. ИД включает в себя только номерные знаки.')
            bot.register_next_step_handler(msg, process_age_step)
            return
        try:
            conn = sqlite3.connect('bot_db')
            conn.row_factory = sqlite3.Row
            conn.execute('DELETE FROM administrators WHERE admin_id=?', (int(text),)).fetchall()
            conn.commit()
            conn.close()
            msg = bot.reply_to(message, 'Администратор был успешно удален', reply_markup=admin_keyboard())
        except:
            msg = bot.reply_to(message, 'Какая-то ошибка')
    except:
        bot.reply_to(message, 'ooooops')


# Конец удаление администраторе
def show_contact_list(message):
    try:
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        chat_id = message.chat.id
        list = []
        text = ''
        for i in conn.execute('SELECT * FROM contact'):
            for j in i:
                list.append(str(j) + ' ')
            list.append('\n')
        text = text.join(list)
        bot.send_message(chat_id, text)
        conn.close()
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


def contact(message):
    try:
        conn = sqlite3.connect('bot_db')
        conn.row_factory = sqlite3.Row
        chat_id = message.chat.id
        text = message.text
        bot.send_message(get_administrators()[0], 'Поступила новая заявка: \n' + text)
        conn.execute('INSERT INTO contact(text) VALUES (?)', (text,))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, 'Ваша заявка была успешно отправлена')
    except:
        bot.send_message(chat_id, 'Что-то пошло не так')


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    about = types.KeyboardButton(text='Информация о фирме')
    offers = types.KeyboardButton(text='Предложения по работе')
    contact = types.KeyboardButton(text='Сконтактироваться')
    keyboard.add(about, offers, contact)
    return keyboard


def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    add_offer = types.KeyboardButton(text='Добавить новую вакансию')
    delete_offer = types.KeyboardButton(text='Удалить вакансию')
    add_admin = types.KeyboardButton(text='Добавить администратора')
    delete_admin = types.KeyboardButton(text='Удалить администратора')
    edit_offer = types.KeyboardButton(text='Редактировать вакансию')
    list_admins = types.KeyboardButton(text='Список администраторов')
    edit_info_about_company = types.KeyboardButton(text='Редактировать информацию о фирме')
    show_contact_list = types.KeyboardButton(text='Показать список заявок')
    edit_start_message = types.KeyboardButton(text='Редактировать стартовое сообщение')
    keyboard.add(add_offer, edit_offer, delete_offer, add_admin, delete_admin, list_admins, edit_info_about_company,
                 show_contact_list, edit_start_message)
    return keyboard


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    bot.send_message(message.chat.id, get_start_message() , reply_markup=start_keyboard())


@bot.message_handler(commands=["adminmenu"])
def adminmenu(message):
    if message.from_user.id in get_administrators():
        bot.send_message(message.from_user.id, text='Добро пожаловать в меню администратора',
                         reply_markup=admin_keyboard())
    else:
        bot.send_message(message.from_user.id, text='У тебя нет прав для входа в это меню')


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Предложения по работе':
        keyboard = types.InlineKeyboardMarkup()
        for i in get_db_connection().execute('SELECT * FROM bot').fetchall():
            keyboard.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
        bot.send_message(message.from_user.id,
                         text='Список актуальных вакансий \n(нажми на интересующую тебя вакансию чтобы получить подробную информацию): ',
                         reply_markup=keyboard)
    elif message.text == 'Информация о фирме':
        bot.send_message(message.chat.id, text=get_welcome_message(), reply_markup=start_keyboard())
    elif message.text == 'Сконтактироваться':
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        'Введите свое Имя, номер телефона, и напишите какая вакансия вас интересует.'),
                                       contact)
    elif message.text == 'Список администраторов' and message.chat.id in get_administrators():
        bot.send_message(message.chat.id, text=str(get_administrators()), reply_markup=admin_keyboard())
    elif message.text == 'Добавить администратора' and message.chat.id in get_administrators():
        add_admin(message)
    elif message.text == 'Удалить администратора' and message.chat.id in get_administrators():
        remove_admin(message)
    elif message.text == 'Показать список заявок' and message.chat.id in get_administrators():
        show_contact_list(message)
    elif message.text == 'Добавить новую вакансию' and message.chat.id in get_administrators():
        add_new_offer(message)
    elif message.text == 'Редактировать информацию о фирме' and message.chat.id in get_administrators():
        edit_information_company(message)
    elif message.text == 'Редактировать стартовое сообщение' and message.chat.id in get_administrators():
        edit_start_message(message)
    elif message.text == 'Редактировать вакансию' and message.chat.id in get_administrators():
        keyboard = types.InlineKeyboardMarkup()
        for i in get_db_connection().execute('SELECT * FROM bot').fetchall():
            keyboard.add(types.InlineKeyboardButton(text=f'id = {i[0]} // {i[1]}', callback_data=i[0]))
        msg = bot.send_message(message.from_user.id, text='Cписок актуальных вакансий: ', reply_markup=keyboard)
        edit_offer(message)
    elif message.text == 'Удалить вакансию' and message.chat.id in get_administrators():
        keyboard = types.InlineKeyboardMarkup()
        for i in get_db_connection().execute('SELECT * FROM bot').fetchall():
            keyboard.add(types.InlineKeyboardButton(text=f'id = {i[0]} // {i[1]}', callback_data=i[0]))
        bot.send_message(message.from_user.id, text='Список актуальных вакансий: ', reply_markup=keyboard)
        remove_offer(message)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю вас...')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    toInt = int(call.data)
    if type(toInt) == int:
        msg = get_offer(toInt)
        a = f'Название вакансии: {msg[1]}\n\n' \
            f'Описание вакансии: {msg[2]}\n\n' \
            f'Локализация: {msg[3]}\n\n' \
            f'Почасовая ставка: {msg[4]}'
        bot.send_message(call.message.chat.id, a)


bot.polling(none_stop=True)
