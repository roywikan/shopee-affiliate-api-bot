import random
from py3pin.Pinterest import Pinterest
import mysql.connector
from bot.database import *

# Login Pinters
pinterest = Pinterest(email='fresmaazz@gmail.com', password='Azzukhruf26', username='id_myfashion', cred_root='cred_root')

# Auto Posting Pinterest
def autoPostingPinterest():
  if(funtion('autoPostingPinterest')[0]['is_active'] == 1) :
    query = "SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post"
    database_post = db_connection(query)

    random_index = random.randrange(len(database_post))

    shopeeid=1

    board_id='1089800878518777159'
    section_id=None
    image_url= database_post[random_index]['product_img']
    description='#racunshopee #racuntiktok #racunshopeecheck #racunshopeehaul #racunshopeecheckout #racunshopeemurah #racuntiktokcheck #racunbelanja #racunootd #ootdindonesia #ootdindo #ootdindomen #ootdindokece #ootdcowok #outfitkekinian #outfitmurah #fashionpria #lokalbrand #lokalpride #lokalbrandindonesia #lokalprideindonesia #lokalproduk #brandlokal #produklokal #brandlokalindonesia #brandlocal #brandlocalindonesia'
    title= database_post[random_index]['product_name']
    alt_text='alt text'
    link= shortLinkShopee(database_post[random_index]['product_link'], shopeeid, "idmyfashion", "Pinterest")

    try:
      pinterest.pin(board_id=board_id, image_url=image_url, description=description, title=title, link=link)
      print("✅ - Posting Berhasil\n")
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