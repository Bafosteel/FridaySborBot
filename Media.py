import requests
from bs4 import BeautifulSoup

class Media(object):
    def __init__(self):
        self.type = 'lxml'
        self.films = {'data':list(dict())}
        self.promos = list()

    def give_me_soup(self, link):
        url = requests.get(link)
        soup = BeautifulSoup(url.text, self.type)
        return soup

class Movies(Media):

    def get_films(self):
        url = 'https://kinoteatr.ru/raspisanie-kinoteatrov/belaya-dacha/#'
        soup = self.give_me_soup(url)
        for div in soup.findAll("div",attrs={"class":['shedule_movie','bordered ','gtm_movie']}):
            final_data = dict()
            final_data["Название фильма"] = div['data-gtm-list-item-filmname']
            final_data["Возрастной рейтинг"] = div.find('i', class_=['raiting_sub']).text
            final_data['Изображение'] = div.find('img', class_=['shedule_movie_img'])['src']
            raw_duration = div.findAll('span', class_=['title'])
            if raw_duration:
                raw = str(raw_duration[1].text).replace('\n','')
                final_data["Длительность"] = ' '.join(raw.split())
            movie_times = div.findAll('span', class_=['shedule_session_time'])
            mov_t = []
            for movie_time in movie_times:
                mov_t.append(' '.join(movie_time.text.split()))
            final_data["Сеансы"] = mov_t
            mov_p = []
            movie_prices = div.findAll('span', class_=['shedule_session_price'])
            for movie_price in movie_prices:
                mov_p.append(' '.join(movie_price.text.split()))
            final_data["Цена"] = mov_p
            self.films['data'].append(final_data)

        return self.films

class Food(Media):

    def get_food(self):
        url = 'https://www.delivery-club.ru/moscow'
        soup = self.give_me_soup(url)
        for span in soup.findAll('span', attrs=['vendor-collection-item__img', 'lazyloaded']):
            print(span['data-src'])
            self.promos.append(span['data-src'])
        return self.promos
