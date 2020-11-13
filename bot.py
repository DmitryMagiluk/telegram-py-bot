import telebot
import pyowm
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config


config_dict = get_default_config()
config_dict['language'] = 'ru'  # your language here

owm = pyowm.OWM('75adb8db999a207142aaa3b73e2dd7a7', config_dict)
bot = telebot.TeleBot('1105051578:AAEXicRiKmjmlQbydo1PSEnxBMM709DrRPs');

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, я бот-синоптик. Введи название города в котором ты хочешь узнать текущую погоду)")

@bot.message_handler(content_types=['text']) 
def get_text_messages(message): 

	try:
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(message.text)
		w = observation.weather

		status = w.detailed_status
		temp = w.temperature('celsius')["temp"]
		wind = w.wind()["speed"]
		humidity = w.humidity

		answer = "ПОГОДА СЕГОДНЯ" + "\n"
		answer += "В городе " + message.text + " сейчас " + status + "\n"
		answer += "Температура: " + str(round(temp,1)) + " *С" + "\n"
		answer += "Скорость ветра: " + str(wind) + " м/с" + "\n"
		answer += "Влажность воздуха: " + str(humidity) + " %"

		bot.send_message(message.from_user.id, answer) 
	except:
		answer = "Ой, не могу найти этот город. " + message.chat.first_name + ", вы точно не ошиблись с названием ?"
		bot.send_message(message.from_user.id, answer) 
	
bot.polling(none_stop = True)
