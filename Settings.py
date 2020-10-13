from enum import Enum
import telebot

class States(Enum):
    """
    Мы используем словарь, в которой храним всегда строковые данные,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_SEND_STICKER = "1"
    S_SEND_VLAD = '2'
    S_SBOR = '3'
    S_CINEMA = '4'
    S_FOOD = '5'
    S_CINEMA_YES = '6'

y_token = 'AIzaSyDx7DF8Ti7hS25eArrqOYUZJIWxz8fD1jY'
token = '1377498450:AAEyKxe5ZfwjrNWW-rc6Na2HGj7dDKo8VeM'

stickers = {1:'CAACAgIAAxkBAAEBJMVfKSa4sXF8U5Cr6S5g9-5VBaV8jwACGQEAAtLdaQVS6DvPqWaenxoE',
            2:'CAACAgIAAxkBAAEBJMdfKSbcR4hiQgRsQ9HivZ9oK6qhzAACFwEAAtLdaQXeYl54aAbKphoE',
            3:'CAACAgIAAxkBAAEBJMlfKSb80g5D4_R1zdiBZb5fAAEVnPwAAqsFAAIjBQ0AAQUOVw5eneNPGgQ',
            4:'CAACAgIAAxkBAAEBJMtfKScO1Aybt6uG320Xq8__m_K5EwAC1wUAAiMFDQABGQ0adjCjOEsaBA',
            5:'CAACAgIAAxkBAAEBJM9fKSdNWiG4mJiiJfhoPyoOGdlIYwACEgADdVCBE26opWd1F-9VGgQ',
            6:'CAACAgIAAxkBAAEBJNFfKSdZHkaYKoMPQ1eAFkTOoC9SRgACLgAD4djSAAH6uc0pGAABXwkaBA',
            7:'CAACAgIAAxkBAAEBJNNfKSd24KT1fJVkn2zrRLkwJZMJ2QACFQADg0cqOFMI5b7VynSqGgQ',
            8:'CAACAgIAAxkBAAEBJNVfKSecyCrPQHQbosB6f-RbwzkK1wACFAADNIWFDOGRzqE72ijUGgQ',
            9:'CAACAgIAAxkBAAEBJNdfKSfONquRlqHmwwtrhzwyofI3tgACIAADFvHqEqDWa0lrY0FgGgQ',
            10:'CAACAgIAAxkBAAEBJNlfKSfdCFp9yCiCrdMxKRI9yDSlxwAC2gAD_OXdAAEiZoo4l1XxNhoE',
            11:'CAACAgIAAxkBAAEBJRhfKUUbwt4YJCPdnjy3VbuHCLjJ1gACSwAD3B1fMs8xSfx3nsMwGgQ'}

header = {'User-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:79.0)'+ \
                           ' Gecko/20100101 Firefox/79.0', # Создаем заголовок, чтобы сайты не воспринимали нас как бота
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'}

cookies = dict(cookies_are='session=4b082e00-074c-75f7-4761-4fb12bbb343b; __utma=12798129.510440631.1596800516.'
                               '1596800516.1596800516.1; __utmc=12798129;' + \
                               ' __utmz=12798129.1596800516.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|' + \
                               'utmctr=(not%20provided); __gads=ID=19506182921d16b7:T=1596800516:S=ALNI' + \
                               '_MY-XwLcuZvDvxMnb7lEx3kAG7ideQ; __qca=P0-23977826-1596800516655;' + \
                               ' _ga=GA1.2.1387315142.1596800524; _gid=GA1.2.525403005.1596800524')

soup_type = 'lxml'
data_and_queue = {"data": None,"raw_data":None}
state = {}
sbor_dates = {"date":"0"}

sites = {'Чикен Карри':'https://www.youtube.com/channel/UCn9bv143ECsDMw-kJCNN7QA',
         'LABELCOM':'https://www.youtube.com/channel/UCNqktdxgAADBj36dC7VGOgg',
         'varlamov':'https://www.youtube.com/channel/UC101o-vQ2iOj9vr00JUlyKw',
         'вДудь':'https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA',
         'Редакция':'https://www.youtube.com/channel/UC1eFXmJNkjITxPFWTy6RsWg',
         'ДИГГЕР ДАНИИЛ ДАВЫДОВ':'https://www.youtube.com/channel/UCrc2oY9Trr97eYNkSbUBlQg',
         'MoscowWalks':'https://www.youtube.com/channel/UCPvoket8Npuv2HTPhcFhuZg'}


bot = telebot.TeleBot(token)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Привет','Пока', 'Когда сбор?')
keyboard.row('Кино',"Жрачка")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Назад',)

keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Расписание', 'Взять билет', 'Назад')

keyboard_movie = telebot.types.ReplyKeyboardMarkup(True)
keyboard_movie.row('Получить сеанс', 'Получить все расписание', 'Вернуться')

keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row('Какие есть скидки')
keyboard3.row('Заказать', 'Назад')

keyboard_inline = telebot.types.InlineKeyboardMarkup(True)
url_button =  telebot.types.InlineKeyboardButton(text="Перейти на сайт",
                                        url="https://kinoteatr.ru/raspisanie-kinoteatrov/belaya-dacha/")
keyboard_inline.add(url_button)

keyboard_inline1 = telebot.types.InlineKeyboardMarkup(True)
url_button1 =  telebot.types.InlineKeyboardButton(text="Перейти на сайт",
                                        url="https://www.delivery-club.ru/moscow")
keyboard_inline1.add(url_button1)

