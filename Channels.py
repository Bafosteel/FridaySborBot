import requests
from Settings import header, cookies, y_token
from datetime import date, timedelta, datetime

class MasterChannel(object):
    def __init__(self):
        self.header = header
        self.cookies = cookies
        self.info = None
        self.token = y_token

    def get_json(self, channel_id):
        response = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&' + \
                                'channelId='+str(channel_id)+ \
                                '&maxResults=10&publishedAfter='+str(date.today() - timedelta(days=5)) + \
                                'T00%3A00%3A00Z&key=' + self.token, headers=self.header,
                                cookies=self.cookies)
        data = response.json()['items']
        return data


class YChannel(MasterChannel):

    def extract_data(self, url):
        data = self.get_json(url)
        for i, v in enumerate(data):
            if date.today().day - (
            datetime.strptime(v['snippet']['publishedAt'][:str(v['snippet']['publishedAt']).find('T')],
                              '%Y-%m-%d')).date().day <= 5:
                print(v['snippet']['publishedAt'][:str(v['snippet']['publishedAt']).find('T')])
                self.info = v['id']['videoId']
        return self.info

