import telebot
import config
import dbworker
import user_data

bot = telebot.TeleBot(config.token)

empty_keyboard = telebot.types.ReplyKeyboardRemove()

sex_keyboard = telebot.types.ReplyKeyboardMarkup()
sex_keyboard.row('Чоловіча', 'Жіноча')

menu_keyboard = telebot.types.ReplyKeyboardMarkup()
menu_keyboard.row('/info', '/settings')

settings_keyboard = telebot.types.ReplyKeyboardMarkup()
settings_keyboard.row('/reset_name', '/reset_age')
settings_keyboard.row('/reset_sex', '/back')

back_keyboard = telebot.types.ReplyKeyboardMarkup()
back_keyboard.row('/back_to_settings')

new_sex_keyboard = telebot.types.ReplyKeyboardMarkup()
new_sex_keyboard.row('Чоловіча', 'Жіноча')
new_sex_keyboard.row('/back_to_settings')

@bot.message_handler(commands=['start'])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "То як твоє ім'я?")
    elif state == config.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id, 'То скільки тобі років?')
    elif state == config.States.S_ENTER_SEX.value:
        bot.send_message(message.chat.id, 'То якої ти статі?')
    elif state == 0:
        bot.send_message(message.chat.id, 'Привіт! Як тебе звуть?')
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
    else:
        bot.send_message(message.chat.id, 'Ми вже знайомі')

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    if len(message.text) < 2:
        bot.send_message(message.chat.id, "Закоротке ім'я, спообуй ще раз!")
        return

    elif len(message.text) > 20:
        bot.send_message(message.chat.id, "Задовге ім'я, спообуй ще раз!")
        return

    elif str(message.text).startswith('/'):
        bot.send_message(message.chat.id, "Недопустиме ім'я")
        return 

    else:
        bot.send_message(message.chat.id, 'Чудово! Скільки тобі років?')
        user_data.set_user_data(message.chat.id, config.user_name, str(message.text))
        dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_AGE.value)
def user_entering_age(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Щось пішло не так! Введи будь ласка свій вік цифрами')
        return

    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, 'Недопустимі значення! Введи будь ласка свій вік')
        return

    else:
        bot.send_message(message.chat.id, 'Добре! Обери стать', reply_markup=sex_keyboard)
        user_data.set_user_data(message.chat.id, config.user_age, str(message.text))
        dbworker.set_state(message.chat.id, config.States.S_ENTER_SEX.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_SEX.value)
def menu(message):
    if message.text == 'Чоловіча' or message.text == 'Жіноча':
        user_data.set_user_data(message.chat.id, config.user_sex, str(message.text))
        bot.send_message(message.chat.id, 'Головне меню', reply_markup=menu_keyboard)
        dbworker.set_state(message.chat.id, config.States.S_MENU.value)
    else:
        bot.send_message(message.chat.id, 'Вкажи будь ласка стать', reply_markup=sex_keyboard)


@bot.message_handler(commands=['info'])
def cmd_info(message):
    bot.send_message(message.chat.id, "Тебе звуть " + user_data.get_user_data(message.chat.id, config.user_name) +
                                        "\nТобі " + user_data.get_user_data(message.chat.id, config.user_age) +
                                        "\nТвоя стать " + str.lower(user_data.get_user_data(message.chat.id, config.user_sex)))

@bot.message_handler(commands=['settings'])
def cmd_settings(message):
    bot.send_message(message.chat.id, 'Налаштування', reply_markup=settings_keyboard)

#Change name
@bot.message_handler(commands=['reset_name'])
def reset_users_name(message):
    bot.send_message(message.chat.id, "Добре! Введи інше ім'я", reply_markup=back_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_NEW_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_NEW_NAME.value)
def set_user_name(message):
    if str(message.text).startswith('/back_to_settings'):
        bot.send_message(message.chat.id, 'Налаштування', reply_markup=settings_keyboard)
        dbworker.set_state(message.chat.id, config.States.S_MENU.value)
    elif str(message.text).startswith('/'):
        bot.send_message(message.chat.id, "Недопустиме ім'я")
    else:
        if user_data.get_user_data(message.chat.id, config.user_sex) == 'Чоловіча':
            user_data.set_user_data(message.chat.id, config.user_name, str(message.text))
            bot.send_message(message.chat.id, "Ти змінив ім'я на " + user_data.get_user_data(message.chat.id, config.user_name), reply_markup=menu_keyboard)
        else:
            user_data.set_user_data(message.chat.id, config.user_name, str(message.text))
            bot.send_message(message.chat.id, "Ти змінила ім'я на " + user_data.get_user_data(message.chat.id, config.user_name), reply_markup=menu_keyboard)
        dbworker.set_state(message.chat.id, config.States.S_MENU.value)

#Change age
@bot.message_handler(commands=['reset_age'])
def reset_users_name(message):
    bot.send_message(message.chat.id, "Добре! Введи інший вік", reply_markup=back_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_NEW_AGE.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_NEW_AGE.value)
def set_user_name(message):
    if str(message.text).startswith('/back_to_settings'):
        bot.send_message(message.chat.id, 'Налаштування', reply_markup=settings_keyboard)
        dbworker.set_state(message.chat.id, config.States.S_MENU.value)
    elif not message.text.isdigit():
        bot.send_message(message.chat.id, "Недопустимий вік")
        dbworker.set_state(message.chat.id, config.States.S_NEW_AGE.value)
    elif int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "Недопустимий вік")
        dbworker.set_state(message.chat.id, config.States.S_NEW_AGE.value)
    else:
        if user_data.get_user_data(message.chat.id, config.user_sex) == 'Чоловіча':
            user_data.set_user_data(message.chat.id, config.user_age, str(message.text))
            bot.send_message(message.chat.id, "Ти змінив вік на " + user_data.get_user_data(message.chat.id, config.user_age), reply_markup=menu_keyboard)
        else:
            user_data.set_user_data(message.chat.id, config.user_age, str(message.text))
            bot.send_message(message.chat.id, "Ти змінила вік на " + user_data.get_user_data(message.chat.id, config.user_age), reply_markup=menu_keyboard)
        dbworker.set_state(message.chat.id, config.States.S_MENU.value)

#Change sex
@bot.message_handler(commands=['reset_sex'])
def reset_users_name(message):
    if user_data.get_user_data(message.chat.id, config.user_sex) == 'Чоловіча':
        user_data.set_user_data(message.chat.id, config.user_sex, 'Жіноча')
        bot.send_message(message.chat.id, "Ти змінила стать на жіночу", reply_markup=menu_keyboard)
    elif user_data.get_user_data(message.chat.id, config.user_sex) == 'Жіноча':
        user_data.set_user_data(message.chat.id, config.user_sex, 'Чоловіча')
        bot.send_message(message.chat.id, "Ти змінив стать на чоловічу", reply_markup=menu_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_MENU.value)

@bot.message_handler(commands=['back_to_settings'])
def cmd_back(message):
    bot.send_message(message.chat.id, 'Налаштування', reply_markup=settings_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_SETTING.value)

@bot.message_handler(commands=['back'])
def cmd_back(message):
    bot.send_message(message.chat.id, 'Головне меню', reply_markup=menu_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_MENU.value)


bot.polling()