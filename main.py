import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6543567848:AAEvl2uCJlXK-NJNB0PuAgagHpZnaIrndIE",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Привет!"  # Можно менять текст
text_button_1 = "Игра в кальмара"  # Можно менять текст
text_button_2 = "История девятихвостого лиса"  # Можно менять текст
text_button_3 = "Винченцо"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Приветик! Что будем делать? Я могу рассказать тебе о моих любимых дорамах!<3',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Для начала давай познакомимся, как тебя зовут?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! А сколько лет?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию! :)', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Сон Ги-хун уже немолод, разведён, по уши погряз в долгах и сидит на шее у старенькой матери. Даже выигранные на скачках деньги в его руках долго не задерживаются, и однажды он встречает в метро загадочного незнакомца, который сначала предлагает сыграть в детскую игру, а затем вручает Ги-хуну немалую сумму и визитку. Но радость мужчины сменятся отчаянием, когда он узнаёт, что бывшая жена с новым мужем собираются увезти его дочь в Америку. Он звонит по номеру с визитки и становится последним участником тайных игр на выживание с призом в 40 миллионов долларов...",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Ли Ён — божество, живущее в горах, которое принимает человеческий облик, чтобы навести порядок в мире людей. А вот его сводный брат Ли Ран — кумихо, который людей ненавидит. Именно на них выходит продюсер экстремального шоу Нам Джи-а. Она давно охотится за девятихвостым лисом, чтобы заснять его для одного из выпусков.",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                 "В восьмилетнем возрасте Пак Чу-хён был усыновлён итальянской семьёй. Теперь парень вырос, его зовут Винченцо Касано, и он работает адвокатом и советником мафиозной семьи. Из-за войны кланов ему приходится вернуться на историческую родину.",
                 reply_markup=menu_keyboard)  # Можно менять текст

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()