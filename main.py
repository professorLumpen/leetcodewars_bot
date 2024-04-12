import json
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from random import shuffle
from bot_token import TOKEN
from typing import Dict, List, Any, Optional


def get_tasks_from_db() -> Optional[Dict[str, Dict[str, Dict[str, List[str]]]]]:
    with open('tasks_db.txt', 'r') as file:
        tasks = json.loads(file.read())
    return tasks


all_tasks = get_tasks_from_db()
bot = TeleBot(TOKEN)
difficulty_levels = {'Beginner', 'Easy', 'Medium', 'Hard'}


@bot.message_handler(commands=['start', 'help'])
def send_categories(message: Any) -> None:
    markup = ReplyKeyboardMarkup(row_width=len(all_tasks))
    for category in all_tasks:
        item_button = KeyboardButton(category)
        markup.add(item_button)
    bot.send_message(message.chat.id, 'Choose a category: ', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in difficulty_levels)
def send_chosen_tasks(message: Any) -> None:
    global all_tasks
    cur_category = message.text
    all_tasks = all_tasks[cur_category]
    shuffle(all_tasks)
    for task in all_tasks[:3]:
        bot.send_message(message.chat.id, task)
    all_tasks = get_tasks_from_db()
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(KeyboardButton('/start'))
    bot.send_message(message.chat.id, 'Do you wanna start new session?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in all_tasks)
def send_subcategories(message: Any) -> None:
    global all_tasks
    cur_category = message.text
    all_tasks = all_tasks[cur_category]
    markup = ReplyKeyboardMarkup(row_width=len(all_tasks))
    for category in all_tasks:
        item_button = KeyboardButton(category)
        markup.add(item_button)
    bot.send_message(message.chat.id, 'Choose a category: ', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def send_subcategories(message: Any) -> None:
    bot.reply_to(message, 'I dont know :c')


bot.infinity_polling()
