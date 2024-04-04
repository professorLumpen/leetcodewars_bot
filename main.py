import json
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from random import shuffle
from bot_token import TOKEN

with open('tasks_db.txt', 'r') as file:
    tasks = json.loads(file.read())

bot = TeleBot(TOKEN)


our_tasks = {key: item for key, item in tasks.items()}
difficulty_levels = {'Beginner', 'Easy', 'Medium', 'Hard'}


@bot.message_handler(commands=['start', 'help'])
def send_categories(message):
    print(message)
    markup = ReplyKeyboardMarkup(row_width=len(tasks))
    for category in our_tasks:
        print(category)
        item_button = KeyboardButton(category)
        markup.add(item_button)
    bot.send_message(message.chat.id, 'Choose a category: ', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in difficulty_levels)
def send_chosen_tasks(message):
    global our_tasks
    cur_category = message.text
    our_tasks = our_tasks[cur_category]
    shuffle(our_tasks)
    for task in our_tasks[:3]:
        bot.send_message(message.chat.id, task)
    our_tasks = {key: item for key, item in tasks.items()}
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(KeyboardButton('/start'))
    bot.send_message(message.chat.id, 'Do you wanna start new session?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in our_tasks)
def send_subcategories(message):
    global our_tasks
    cur_category = message.text
    our_tasks = our_tasks[cur_category]
    markup = ReplyKeyboardMarkup(row_width=len(tasks))
    for category in our_tasks:
        print(category)
        item_button = KeyboardButton(category)
        markup.add(item_button)
    bot.send_message(message.chat.id, 'Choose a category: ', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def send_subcategories(message):
    bot.reply_to(message, 'I dont know :c')


bot.infinity_polling()
