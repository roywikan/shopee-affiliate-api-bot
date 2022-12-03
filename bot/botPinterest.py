import random
from py3pin.Pinterest import Pinterest
import mysql.connector

# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="shopee_aff"
)

# Login Pinters
pinterest = Pinterest(email='fresmaazz@gmail.com', password='Azzukhruf26', username='id_myfashion', cred_root='cred_root')

# Auto Posting Pinterest
def autoPostingPinterest():
  mycursor = mydb.cursor(dictionary=True)
  mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
  database_post = mycursor.fetchall()

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
  mycursor = mydb.cursor(dictionary=True)
  mycursor.execute("SELECT id, appid, rahasia FROM account_shopeeaff WHERE id={}".format(idshopee))
  account_shopee = mycursor.fetchall()

  from shopee_affiliate import ShopeeAffiliate    
  sa = ShopeeAffiliate(account_shopee[0]['appid'], account_shopee[0]['rahasia'])
  res = sa.generateShortLink(link, akun, sosialmedia)
  res = res.replace("shope", "shpe")
  return(res)