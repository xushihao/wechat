from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
gf_birthday = os.environ['GFBIRTHDAY']
bf_birthday = os.environ['BFBIRTHDAY']
gk_date = os.environ['GK_DATE']
xd_date = os.environ['XD_DATE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

bf_user_id = os.environ["BF_USER_ID"]
gf_user_id = os.environ["GF_USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_loveday_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days + 1

def get_gf_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + gf_birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_bf_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + bf_birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_gk_day_left():
  next = datetime.strptime(str(date.today().year) + "-" + gk_date, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_xd_day_left():
  next = datetime.strptime(str(date.today().year) + "-" + xd_date, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_loveword():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_loveword()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_loveday_count()},
        "gf_birthday_left":{"value":get_gf_birthday()},"bf_birthday_left":{"value":get_bf_birthday()},
        "gk_day_left":{"value":get_gk_day_left()},"words":{"value":get_loveword(), "color":get_random_color()}}
res = wm.send_template(bf_user_id, template_id, data)
res = wm.send_template(gf_user_id, template_id, data)
print(res)
