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


def autopostingAkunBackUp():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup")
    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()

    for account in accountResult:
        random_index = random.randrange(len(database_post))
        
        try:
            urllib.request.urlretrieve('{}'.format(database_post[random_index]['product_img']), "imagePost.png")
                
            media = botTwitter().media_upload("imagePost.png", additional_owners=[account['id']])

            auth = twitter.OAuth1UserHandler(
                "TDsus5T6nqDikv70sNR3lkxx6", "WCBet8FJBVTsTV12MuTv7EBKV56yPqwQctJ4Ga8ekizYkQ6zXp",
                account['access_token'], account['access_token_secret']
            )
            api = twitter.API(auth)

            statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'],account['id_shopee'], account['id'] , "Twitter" ))

            try:
                api.update_status(status=statusTweet, media_ids=[media.media_id])
                print(account['username'])
                print("✅ - Posting Berhasil\n")
            except:
                pass   
        except:
            pass
           
# Repost akun backUp Ayah ke masitowae
def autoRepostAkunAyah() :
    userIDaccount = "masitowae"
    tweets = botTwitter().user_timeline(screen_name=userIDaccount, count=100, include_rts=False, tweet_mode='extended')

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT id_shopee, no, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=2 AND username <> 'imamto2003'")
    accountResult = mycursor.fetchall()

    for account in accountResult:
        auth = twitter.OAuth1UserHandler(
            "TDsus5T6nqDikv70sNR3lkxx6", "WCBet8FJBVTsTV12MuTv7EBKV56yPqwQctJ4Ga8ekizYkQ6zXp",
            account['access_token'], account['access_token_secret']
        )
        api = twitter.API(auth)

        print("Account : {}".format(account['username']))

        totalRetweet = 2
        for index in tweets:
            if totalRetweet != 0:
                try :
                    random_index = random.randrange(len(tweets))
                    api.unretweet(id =tweets[random_index].id)
                    api.retweet(id=tweets[random_index].id)
                    print("✅ - Repost Berhasil")
                    totalRetweet = totalRetweet - 1
                except twitter.TweepyException as e:
                    pass
                    print(e) 
            else:
                break
                
def autopostingTrendingTopik():
    API = botTwitter()

    #Scrap Trending ======================================================
    WOEID = 1047378

    top_trends = API.get_place_trends(WOEID)

    final = []

    for i in range(len(top_trends[0]['trends'])):
        # if(top_trends[0]['trends'][i]['tweet_volume']):
        name = top_trends[0]['trends'][i]['name']
        volume = top_trends[0]['trends'][i]['tweet_volume']
        final.append([name,volume])
    
    trending = ""

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup")
    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()

    for account in accountResult:
        random_index = random.randrange(len(database_post))
        urllib.request.urlretrieve('{}'.format(database_post[random_index]['product_img']), "imagePost.png")
        media = API.media_upload("imagePost.png", additional_owners=[account['id']])

        auth = twitter.OAuth1UserHandler(
            "TDsus5T6nqDikv70sNR3lkxx6", "WCBet8FJBVTsTV12MuTv7EBKV56yPqwQctJ4Ga8ekizYkQ6zXp",
            account['access_token'], account['access_token_secret']
        )
        api = twitter.API(auth)

        for x in range(10):
            random_index_trending = random.randrange(len(final))
            trending += " " + final[random_index_trending][0]

        statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'],account['id_shopee'], account['id'] , "Twitter" ))
        
        try:
            api.update_status(status=statusTweet, media_ids=[media.media_id])
            print(account['username'])
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