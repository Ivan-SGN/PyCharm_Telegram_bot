import telebot
from random import choice
from Weather_Loader import *

TOKEN = "some telegram bot token..."
triggers_hallo = ['привет', 'хай', 'ку']
triggers_howru = ['как дела', 'как жизнь', 'как идет']
triggers_joke = ['анекдот', 'шутка', 'прикол']
triggers_weather = ['погод', 'температур', 'за окном']


class Bot:
    def __init__(self):
        self.__sticker_pack = self.get_sticker_pack()
        self.__jokes = self.get_jokes()
        self.__bot = telebot.TeleBot(TOKEN)
        self.__weather = Weather()

    def get_sticker_pack(self):
        with open("stricker_pack", 'r') as f:
            res = f.readlines()
        res = self.delete_delivers(res)
        return res

    def get_jokes(self):
        with open("jokes", 'r') as f:
            res = f.readlines()
        res = self.delete_delivers(res)
        return res

    def delete_delivers(self, lines):
        for i in range(len(lines)):
            if '\n' in lines[i]:
                lines[i] = lines[i].replace('\n', '')
        return lines

    def run(self):
        self.send_welcome_mes()
        self.react()
        self.__bot.infinity_polling()

    def get_weather_mes(self, weather):
        mes = (f"Погода в городе:{weather.city} \n"
               f"Температура:{int(weather.temperature)}C°\n"
               f"Ощущается как:{int(weather.feels_temperature)}C°\n"
               f"Влажность:{weather.humidity}%\n"
               f"Скорость ветра:{weather.wind_speed}м/с\n"
               )
        return mes

    def send_message(self, message):
        is_triggered = False
        for word in triggers_hallo:
            if word in message.text.lower():
                self.__bot.send_message(message.from_user.id, 'ку-ку, ' + message.from_user.first_name + '!')
                is_triggered = True
                break
        for word in triggers_howru:
            if word in message.text.lower():
                self.__bot.send_message(message.from_user.id, 'нормально!')
                is_triggered = True
                break
        for word in triggers_joke:
            if word in message.text.lower():
                self.__bot.send_message(message.from_user.id, choice(self.__jokes))
                is_triggered = True
                break
        for word in triggers_weather:
            if word in message.text.lower():
                self.__weather.get_weather()
                mes = self.get_weather_mes(self.__weather)
                self.__bot.send_message(message.from_user.id, mes)
                is_triggered = True
                break
        if not is_triggered:
            self.__bot.send_message(message.from_user.id, 'не понял тебя(')

    def send_welcome_mes(self):
        @self.__bot.message_handler(commands=['start'])
        def welcome(message):
            mes = (f"Добро пожаловать, {message.from_user.first_name}!\n"
                "я - твой собеседник, ты можешь:\n"
                "поздароваться со мной,\n"
                "спросить как у меня дела, \n"
                "попросить меня рассказать тебе анекдот \n"
                "попросить меня рассказать тебе погоду  \n"
                "или просто отреагировать на твою фотку или голосовое)) \n")
            self.__bot.send_message(message.from_user.id, mes)

    def react(self):
        @self.__bot.message_handler(content_types=['text', 'photo', 'video', 'sticker', 'voice'])
        def text(message):
            if message.content_type == 'text':
                self.send_message(message)
            else:
                self.__bot.send_sticker(message.from_user.id, choice(self.__sticker_pack))
