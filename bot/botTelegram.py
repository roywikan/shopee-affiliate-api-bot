import pandas as pd
import random
import requests
import mysql.connector
from bot.database import *

def autoPostingTelegram():
  if(funtion('autoPostingTelegram')[0]['is_active'] == 1) :
    print("\n🟧 AUTO POSTING")

    query = "SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post"
    database_post = db_connection(query)

    shopeid =1
    
    idChannelTelegrams = ['-1001658353827', '-1001866060533']

    for channelTelegram in idChannelTelegrams:
      try:
          random_index = random.randrange(len(database_post))
          statusTelegram = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'], shopeid, "racunshopee", "Telegram" ))
          message = 'https://api.telegram.org/bot5479078966:AAECnT7JEy4hNpjHGUzdZtSTsgOOjN22O_8/sendPhoto?chat_id={}&photo={}&caption={}'.format(channelTelegram, database_post[random_index]['product_img'], statusTelegram)
          requests.post(message)

          print("✅ - Posting Berhasil")
      except:
          pass

def shortLinkShopee(link, idshopee, akun, sosialmedia):
  query = "SELECT id, appid, rahasia FROM account_shopeeaff WHERE id={}".format(idshopee)
  account_shopee = db_connection(query)

  from shopee_affiliate import ShopeeAffiliate    
  sa = ShopeeAffiliate(account_shopee[0]['appid'], account_shopee[0]['rahasia'])
  res = sa.generateShortLink(link, akun, sosialmedia)
  res = res.replace("shope", "shpe")
  return(res)