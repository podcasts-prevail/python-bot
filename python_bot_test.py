import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove
from config import BOT_TOKEN

import json
import math

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Да, и готов поделиться своей геолокацией", request_location=True)
    markup.add(button)
    bot.reply_to(message, "Хочешь найти ближайшую спешлти-кофейню в Тбилиси?".format(message.from_user)
  ,parse_mode='html',reply_markup=markup)

@bot.message_handler(content_types=['location'])
def location (message):
    if message.location is not None:
        user_coordinates = [message.location.latitude, message.location.longitude]

        f = open('coffee_houses.json')
        data = json.load(f)

        if len(data)>0:
            dist = math.dist(data["coffee_houses"][0]["coordinates"], user_coordinates)
            result_name = data["coffee_houses"][0]["name"]
            result_location = data["coffee_houses"][0]["coordinates"]
            for coffee_place in data["coffee_houses"]:
                test_dist = math.dist(coffee_place["coordinates"], user_coordinates)
                if test_dist < dist:
                    result_name = coffee_place["name"]
                    result_location = coffee_place["coordinates"]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            bot.reply_to(message, "Ближайшая к тебе кофейня — "+ result_name+ ".\n\nВот она где ↓".format(message.from_user)
  ,parse_mode='html')
            bot.send_location(message.chat.id, result_location[0], result_location[1], reply_markup=ReplyKeyboardRemove())

bot.polling(none_stop=True)
