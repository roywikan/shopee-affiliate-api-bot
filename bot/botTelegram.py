import tweepy as twitter
import time
from datetime import datetime
import pandas as pd
import random
import urllib.request
from PIL import Image
import requests
import schedule
from py3pin.Pinterest import Pinterest
import mysql.connector

# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="shopee_aff"
)

def autoPostingTelegram():
    print("\n\n🟧 AUTO POSTING : {}\n".format(datetime.now()))

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved")

    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")

    database_post = mycursor.fetchall()

    shopeid =1

    random_index = random.randrange(len(database_post))

    # upload image
    urllib.request.urlretrieve('{}'.format(database_post[random_index][4]), "imagePost.png")

    # Post Telegram
    try:
        statusTelegram = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3], shopeid, "racunshopee", "Telegram" ))
        message = 'https://api.telegram.org/bot5479078966:AAECnT7JEy4hNpjHGUzdZtSTsgOOjN22O_8/sendPhoto?chat_id=-1001658353827&photo={}&caption={}'.format(database_post[random_index][4], statusTelegram)
        requests.post(message)
    except:
        pass