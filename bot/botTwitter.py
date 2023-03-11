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

idDataBaseItem = '15JVk3QaMzRIzvXGq8KNgUO4i6RFyG12h0BXUKlrFf2Q'
db = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{idDataBaseItem}/export?format=csv")

# API BotTwitter
def botTwitter():
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"
    
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
                "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
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
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
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

    mycursor = mydb.cursor()
    mycursor.execute("SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup")
    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()

    for i in range(len(accountResult)):
        random_index = random.randrange(len(database_post))
        urllib.request.urlretrieve('{}'.format(database_post[random_index][4]), "imagePost.png")
        media = API.media_upload("imagePost.png", additional_owners=[accountResult[i][1]])

        auth = twitter.OAuth1UserHandler(
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
            accountResult[i][3], accountResult[i][4]
        )
        api = twitter.API(auth)

        for x in range(10):
            random_index_trending = random.randrange(len(final))
            trending += " " + final[random_index_trending][0]

        statusTweet = "‼ PROMO DISKON ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}\n\ntag:{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3],accountResult[i][0], accountResult[i][1] , "Twitter" ), trending)
        
        try:
            api.update_status(status=statusTweet, media_ids=[media.media_id])
            print(accountResult[i][2])
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