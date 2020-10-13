from Channels import YChannel
from bs4 import  BeautifulSoup
import requests

def channel_update(channel_id):
    yt = YChannel()
    info = yt.extract_data(channel_id)
    return info
