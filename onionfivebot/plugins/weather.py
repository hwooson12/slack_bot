import re
import os
import json
import datetime

from slackbot.bot import respond_to
import requests
from bs4 import BeautifulSoup

from onionfivebot import bot, sched


weather_url = 'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109'


def get_weatherinfo():
    url = 'http://api.openweathermap.org/data/2.5/weather'

    api_key = os.environ.get('WEATHER_API')
    city = 'Seoul'

    params = {'q': city,
            'APPID': api_key}

    r = requests.get(url, params=params)

    weather = json.loads(r.text)

    temp = weather['main']['temp'] - 273.15
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']
    clouds = weather['clouds']['all']
    rain = weather.get('rain')
    rain_fall = rain['rain.3h'] if rain else 0
    snow = weather.get('snow')
    snow_fall = snow['snow.3h'] if snow else 0
    now = datetime.datetime.utcfromtimestamp(weather.get('dt')) + datetime.timedelta(hours=9)
    nowtime = now.strftime('%Y년 %m월 %d일 %H시 %M분')

    inform = '`{0}` 서울 기상상황 알려드립니다.\n>>>기온    `{1:0.2f}도`\n습도    `{2}%`\n구름량 `{3}%`\n풍속    `{4}m/s`\n강우량 `{5}`\n강설량 `{6}`'.format(nowtime, temp, humidity, clouds, wind_speed, rain_fall, snow_fall)
    return inform


@sched.scheduled_job('cron', day_of_week='mon-fri', hour='9-19/5')
def notify_weather_info():
    slack_client = getattr(bot, "_client", None)
    channel_id = slack_client.find_channel_by_name('general')
    slack_client.send_message(channel_id, get_weatherinfo())


@respond_to('^날씨$', re.IGNORECASE)
def today_weather_info(message):
    message.send(get_weatherinfo())
