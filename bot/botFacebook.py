import random
import requests
import mysql.connector
from bot.database import *
from function_list import *

# Auto Posting Halaman Facebook
def autoPostingFacebook():
    if(funtion('autoPostingFacebook')[0]['is_active'] == 1) :
        query = "SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post"
        database_post = db_connection(query)
        random_index = random.randrange(len(database_post))
        
        shopeid =1

        page_id= 105258409090407 
        facebook_access_token= 'EAAS1MRIVS4gBAFTx5PpZBtpFdm0TBLn60bBRq4EE4YR9fZB4ji6C9RZAiksiZBzp97001TrM1qUxvWMJ7WkibysHu6CCZBxyD0pWyaGyNuKMYYmn8TpzZAVPwD0VJeHkupoxZBAeHYiieXdexbd1KAkZCtHLZB082ME26y16CSVRKaQz8P2f5BMm0'
        statusTweet = "‼ PROMO DISKON ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'],shopeid, "idmyfashion", "Facebook" ))
        # post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
        post_url = 'https://graph.facebook.com/v5.0/{}/photos'.format(page_id)
        imgUrl = database_post[random_index]['product_img']

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
    
def shortLinkShopee(link, idshopee, akun, sosialmedia):
  query = "SELECT id, appid, rahasia FROM account_shopeeaff WHERE id={}".format(idshopee)
  account_shopee = db_connection(query)

  from shopee_affiliate import ShopeeAffiliate    
  sa = ShopeeAffiliate(account_shopee[0]['appid'], account_shopee[0]['rahasia'])
  res = sa.generateShortLink(link, akun, sosialmedia)
  res = res.replace("shope", "shpe")
  return(res)