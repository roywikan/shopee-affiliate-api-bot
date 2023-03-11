import tweepy as twitter
import pandas as pd
import random
import urllib.request
import requests
import schedule
import mysql.connector

# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="shopee_aff"
)

userID = "tanyakanrl"

# API BotTwitter
def botTwitter():
    API_KEY = "TDsus5T6nqDikv70sNR3lkxx6"
    API_SECRET_KEY = "WCBet8FJBVTsTV12MuTv7EBKV56yPqwQctJ4Ga8ekizYkQ6zXp"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAAzx0z5tcY43qve6JUby%2BJeU5kCwM%3DkXHXPkdCE7hhnRtfCDr44dBIcNTy25lfPnUqQ3QMklgfpQXJAl"
    ACCESS_TOKEN = "975213506696855553-T4nK2ZGtevzbt5aHi59P3ejjasZtHof"
    SECRET_ACCESS_TOKEN = "CsEmqJBTrGFrMwEKjCSwaqXWuW4Y77x5QOXjyeYjfUhd3"
    
    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
    
    return API

def posting():
    print("\n\n🟧 AUTO POSTING\n")

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved")
    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()

    shopeid =1
    
    tweets = botTwitter().user_timeline(screen_name=userID, count=20)
    random_index = random.randrange(len(tweets))
    replayTweetId = tweets[random_index].id

    for account in accountResult:
        try :
            auth = twitter.OAuthHandler(account['API_KEY'], account['API_SECRET_KEY'])
            auth.set_access_token(account['ACCESS_TOKEN'], account['SECRET_ACCESS_TOKEN'])
            api = twitter.API(auth)

            profile = api.update_profile()
            print("\nAccount : {}".format(profile.name) + " ({})".format(profile.screen_name))

            random_index = random.randrange(len(database_post))

            # Download Image
            urllib.request.urlretrieve('{}'.format(database_post[random_index]['product_img']), "imagePost.png")

            try:
                statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'], shopeid, "idmyfashion", "Twitter" ))
                media = api.media_upload("imagePost.png")
                api.update_status(status=statusTweet, media_ids=[media.media_id], in_reply_to_status_id=replayTweetId, auto_populate_reply_metadata=True)
                
                print("✅ - Posting Berhasil")
            except:
                print('Error posting')
                pass
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