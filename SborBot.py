from random import randrange
from YoutubeCheck import channel_update
import time
from Settings import stickers, States, bot
from Settings import keyboard, keyboard1, keyboard2, keyboard3, keyboard_inline, keyboard_inline1, keyboard_movie
from Settings import state, sites, sbor_dates, data_and_queue
from Media import Movies, Food
from collections import deque
from os import listdir, remove, environ
environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
import moviepy.editor as moviepy

def get_current_state(user_id):
    try:
        return state[user_id]
    except KeyError:  # Если такого ключа почему-то не оказалось
        return States.S_START.value


@bot.message_handler(commands=['vlad'])
def vlad(message):
    bot.send_message(message.chat.id,'Влад пидарас',reply_markup=keyboard)
    doc = open('Vlad\\'+str(randrange(1, 4))+'.jpg','rb')
    bot.send_photo(message.chat.id, doc,)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Привет {}, чтобы получить список команд, напиши: /help'.format(message.from_user.first_name)
                     ,reply_markup=keyboard)
    state[message.chat.id] = States.S_START.value

@bot.message_handler(commands=['sbor'])
def sbor(message):
    bot.send_message(message.chat.id,'А ты смышленный, {}. Ну что же, задавай сбор.'.format(message.from_user.first_name)
                     ,reply_markup=keyboard)
    state[message.chat.id] = States.S_SBOR.value


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_SBOR.value)
def set_sbor(message):
    if message.text.lower() == 'назад':
        set_reset(message)
    else:
        if message.text == "0":
            bot.send_message(message.chat.id, "Сбор сброшен",reply_markup=keyboard1)
            sbor_dates['date'] = message.text
        else:
            bot.send_message(message.chat.id, "Cбор назначен в {}".format(message.text),reply_markup=keyboard1)
            sbor_dates['date'] = message.text

@bot.message_handler(commands=['help'])
def get_help(message):
    c = ('/start', '/help', '/sticker', '/check', '/reset','/vlad')
    bot.send_message(message.chat.id,'Список команд: \n'
                                     '' + str(c[0]) + ' - Запуск бота\n'
                                     '' + str(c[1]) + ' - Запросить список команд\n'
                                     '' + str(c[2]) + ' - Получить случайный стикер\n'
                                     '' + str(c[3]) + ' - Разовая проверка каналов\n'
                                     '' + str(c[4]) + ' - Сброс к началу диалога\n'
                                     '' + str(c[5]) + ' - На случай, если влад опять проебался\n',reply_markup=keyboard)

@bot.message_handler(commands=['reset'])
def set_reset(message):
    state[message.chat.id] = States.S_START.value
    bot.send_message(message.chat.id, 'OK', reply_markup=keyboard)

@bot.message_handler(commands=['sticker'])
def sticker(message):
    bot.send_message(message.chat.id, '{}, Отправь мне какой-нибудь стикер,'.format(message.from_user.first_name) + \
                     'а я тебе скину скину какой-нибудь другой в ответ',reply_markup=keyboard1)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')
    state[message.chat.id] = States.S_SEND_STICKER.value

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_SEND_STICKER.value)
@bot.message_handler(content_types='sticker')
def send_st(message):
    try:
        if message.text.lower() == 'назад':
            set_reset(message)
        else:
            bot.send_sticker(message.chat.id, stickers[randrange(1, 12)],reply_markup=keyboard1)
    except AttributeError:
        bot.send_sticker(message.chat.id, stickers[randrange(1, 12)], reply_markup=keyboard1)


@bot.message_handler(commands=['webm'])
def check_data(message):
    bot.send_message(message.chat.id, str('{}, ща все будет'.format(message.from_user.first_name)))
    webms = list()
    for elem in listdir(path='/sup2ch/'):
        if '.mp4' or '.webm' in elem:
            if '.zip' not in elem:
                webms.append(elem)
    for elem in listdir(path='/sup2ch/webm/webm/'):
        webms.append(elem)
    random_vid = webms[randrange(1, len(webms))]
    if 'webm' in random_vid:
        try:
            bot.send_message(message.chat.id, str('{}, пришла webm. Сейчас обработаю и вышлю'.format(message.from_user.first_name)))
            clip = moviepy.VideoFileClip('/sup2ch/' + str(random_vid))
            clip.write_videofile("myvideo.mp4")
            bot.send_video(message.chat.id,
                              open("myvideo.mp4", 'rb'), supports_streaming=True)
        except OSError as ex:
            print(ex.args[0])
            clip = moviepy.VideoFileClip('/sup2ch/webm/webm/' + str(random_vid))
            clip.write_videofile("myvideo.mp4")
            bot.send_video(message.chat.id,
                              open("myvideo.mp4", 'rb'), supports_streaming=True)
    else:
        bot.send_video(message.chat.id,
                   open('/sup2ch/'+str(random_vid), 'rb'),
                   supports_streaming=True)
    return remove("myvideo.mp4")


@bot.message_handler(commands=['check'])
def check_data(message):
    for site in sites:
        info = channel_update(sites[site].replace('https://www.youtube.com/channel/',''))
        if info != '' and info is not None:
            bot.send_message(message.chat.id, str('{}, Последние видео на канале:'.format(message.from_user.first_name)))
            bot.send_message(message.chat.id, str('Канал "{}"'.format(site)) + '\n' + \
                             str('https://www.youtube.com/watch?v=')+info)
        else:
            bot.send_message(message.chat.id,
                             str('{},'.format(message.from_user.first_name)) +
                             str(' Новых видео у канала "{}" нет'.format(str(site))))


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_CINEMA.value)
def get_cinema(message):
    if message.text.lower() == 'назад':
        set_reset(message)
    elif message.text.lower() == 'расписание':
        film = Movies()
        data = film.get_films()
        data_and_queue['data'] = deque(data['data'])
        data_and_queue['raw_data'] = data
        bot.send_message(message.chat.id,'Выберите требуемую опцию',reply_markup=keyboard_movie)
        state[message.chat.id] = States.S_CINEMA_YES.value
    elif message.text.lower() == 'взять билет':
        bot.send_message(message.chat.id,"Отправил тебе ссылку для заказа билетов",
                         reply_markup=keyboard_inline)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_CINEMA_YES.value)
def cinema_options(message):
    if message.text.lower() == 'получить сеанс':
        try:
            new_data = data_and_queue['data'].popleft()
            bot.send_photo(message.chat.id, new_data['Изображение'])
            bot.send_message(message.chat.id, new_data['Название фильма'] + \
                             " " + new_data['Возрастной рейтинг'] + "\n" + \
                             "Длительность: " + new_data['Длительность'] + " Доступные сеансы: \n")
            for y, z in zip(new_data["Сеансы"], new_data['Цена']):
                bot.send_message(message.chat.id, y + ": " + z)
        except (IndexError, UnboundLocalError) as ex:
            print("Error wsa occurred: " + ex.args[0])
            bot.send_message(message.chat.id,"Список закончился")
    elif message.text.lower() == 'вернуться':
        bot.send_message(message.chat.id,'Ок',reply_markup=keyboard2)
        state[message.chat.id] = States.S_CINEMA.value
    elif message.text.lower() == 'получить все расписание':
        data = data_and_queue['raw_data']
        bot.send_message(message.chat.id, 'Текущие сеансы')
        for i, v in enumerate(data['data']):
            print(v)
            bot.send_photo(message.chat.id, v['Изображение'])
            bot.send_message(message.chat.id, v['Название фильма'] + " " + v['Возрастной рейтинг'] + "\n" + \
                     "Длительность: " + v['Длительность'] + " Доступные сеансы: \n")
            for y, z in zip(v["Сеансы"], v['Цена']):
                bot.send_message(message.chat.id, y + ": " + z)
            time.sleep(5)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_FOOD.value)
def get_dc_food(message):
    if message.text.lower() == 'назад':
        set_reset(message)
    elif message.text.lower() == 'какие есть скидки':
        fd = Food()
        food = fd.get_food()
        bot.send_message(message.chat.id, "Текущие скидки: (Внимание! Получение происходит без авторизации," + \
                         " поэтому некоторые скидки могут быть не актуальны.")
        for i, v in enumerate(food):
            bot.send_photo(message.chat.id, v)
            time.sleep(5)
    elif message.text.lower() == 'заказать':
        bot.send_message(message.chat.id, "Отправил тебе ссылку для заказа eды",
                         reply_markup=keyboard_inline1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id,'Здарова, {}'.format(message.from_user.first_name),reply_markup=keyboard)
        bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAEBJL1fKSNQxKEaoHIvimcOgvPGomud6gACZwADcQtCBbSvNtH6NZIvGgQ')

    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id,'Пока, {}'.format(message.from_user.first_name),reply_markup=keyboard)

        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJL9fKSRgVm-X3HeIvq4vI8A9jJOCAAMgAQAC0t1pBSOWz2dcShYvGgQ')

    elif message.text.lower() == 'когда сбор?':
        if sbor_dates['date'] == str("0"):
            bot.send_message(message.chat.id,'А хуй его знает, {}'.format(message.from_user.first_name),
                             reply_markup=keyboard)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBMglfNVWRvwgbT9LuiAt8hdr2WCd2xgACGwADaJpdDLpW8dsSnhZGGgQ')
        else:
            bot.send_message(message.chat.id, '{}, сбор будет в {}'.format(message.from_user.first_name
                                                                           ,sbor_dates['date']), reply_markup=keyboard)
    elif message.text.lower() == 'кино':
        bot.send_message(message.chat.id,'Короче, {}, расклад такой:'.format(message.from_user.first_name),
                         reply_markup=keyboard2)
        state[message.chat.id] = States.S_CINEMA.value

    elif message.text.lower() == 'жрачка':
        bot.send_message(message.chat.id,'Короче, {}, расклад такой:'.format(message.from_user.first_name),
                         reply_markup=keyboard3)
        state[message.chat.id] = States.S_FOOD.value
    else:
        bot.send_message(message.chat.id, 'Прости, я тебя не понимаю')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJMFfKSUEzuXlw-KDLC8ZAT-jHfMbEQACGAEAAtLdaQV3nTANMOlAPxoE')



bot.polling()
