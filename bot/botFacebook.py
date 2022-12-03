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

def autoPostingFacebook():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()
    random_index = random.randrange(len(database_post))
    shopeid =1
    
    page_id= 105258409090407 
    facebook_access_token= 'EAAS1MRIVS4gBAFTx5PpZBtpFdm0TBLn60bBRq4EE4YR9fZB4ji6C9RZAiksiZBzp97001TrM1qUxvWMJ7WkibysHu6CCZBxyD0pWyaGyNuKMYYmn8TpzZAVPwD0VJeHkupoxZBAeHYiieXdexbd1KAkZCtHLZB082ME26y16CSVRKaQz8P2f5BMm0'
    statusTweet = "‼ PROMO DISKON ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3],shopeid, "idmyfashion", "Facebook" ))
    # post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
    post_url = 'https://graph.facebook.com/v5.0/{}/photos'.format(page_id)
    imgUrl = database_post[random_index][4]

    payload = {
        'message': statusTweet,
        'access_token': facebook_access_token,
        'url': imgUrl
    }
    try:
        posting = requests.post(post_url, data=payload)
        print("✅ - Posting Berhasil\n")
    except:
        pass