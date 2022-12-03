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

userID = "spongebobnfess"

idDataBaseItem = '15JVk3QaMzRIzvXGq8KNgUO4i6RFyG12h0BXUKlrFf2Q'

db = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{idDataBaseItem}/export?format=csv")



# AUTO POSTING id_myfashion
def autoposting():
    print("\n\n🟧 AUTO POSTING : {}\n".format(datetime.now()))

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved")

    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")

    database_post = mycursor.fetchall()

    shopeid =1

    for x in range(len(accountResult)):
        auth = twitter.OAuthHandler(accountResult[x][1], accountResult[x][2])
        auth.set_access_token(accountResult[x][4], accountResult[x][5])
        api = twitter.API(auth)

        profile = api.update_profile()

        print("\nAccount : {}".format(profile.name) + " ({})".format(profile.screen_name))

        random_index = random.randrange(len(database_post))

        # upload image
        urllib.request.urlretrieve('{}'.format(database_post[random_index][4]), "imagePost.png")

        try:
            statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3], shopeid, "idmyfashion", "Twitter" ))
            media = api.media_upload("imagePost.png")
            api.update_status(status=statusTweet, media_ids=[media.media_id])
        except:
            pass
        

# Retweet Spongebob to Akun BackUp
def autoRetweetNonEleved():
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
   
    tweets = API.user_timeline(screen_name=userID, count=1, tweet_mode='extended')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved")

    accountResult = mycursor.fetchall()

    for x in range(len(accountResult)):

        api = twitter.Client(bearer_token=accountResult[x][3], consumer_key=accountResult[x][1], consumer_secret=accountResult[x][2], access_token=accountResult[x][4], access_token_secret=accountResult[x][5])
        print("Account : {}".format(accountResult[x][0]))

        for info in tweets[:1]:
            print("ID : {}".format(info.id))

        try:
            api.retweet(tweet_id=info.id)
            print("✅ - Retweet Berhasil\n")
        except twitter.TweepyException as e:
            pass
            print(e)
    
    # Sementara
    mycursor.execute("SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=1 AND username='sarhagthang' OR username='Donni_darwin' OR username='alviliaa_' OR username='aqillaaurelliaa' OR username='cantika_vela' OR username='HappyRacun'")

    accountResult = mycursor.fetchall()

    for i in range(len(accountResult)):
        auth = twitter.OAuth1UserHandler(
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
            accountResult[i][3], accountResult[i][4]
        )
        api = twitter.API(auth)

        print("Account : {}".format(accountResult[i][2]))

        for info in tweets[:1]:
            print("ID : {}".format(info.id))

        try:
            api.retweet(id=info.id)
            print("✅ - Retweet Berhasil\n")
        except twitter.TweepyException as e:
            print(e)
            pass
    # Sementara
    
    
# Repost Barang dari akun id_myfashion ke akun backUp
def autoRepostNonEleved() :
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    api = twitter.API(auth)
    userIDaccount = "id_myfashion"

    tweets = api.user_timeline(screen_name=userIDaccount, count=200, include_rts=False, tweet_mode='extended')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved WHERE username <> 'yusiedaynti' AND username <> '_firzaamanda' AND username <> 'vidyaisvara' AND username <> 'zannakirana_'")

    accountResult = mycursor.fetchall()

    for x in range(len(accountResult)):
        API = twitter.Client(bearer_token=accountResult[x][3], consumer_key=accountResult[x][1], consumer_secret=accountResult[x][2], access_token=accountResult[x][4], access_token_secret=accountResult[x][5])
        print("Account : {}".format(accountResult[x][0]))

        totalA = 3
        for index in range(len(tweets)-1, 0, -1):
            if totalA != 0:
                try :
                    random_index = random.randrange(len(tweets))
                    API.unretweet(source_tweet_id =tweets[random_index].id)
                    API.retweet(tweet_id=tweets[random_index].id)
                    print("✅ - Repost Berhasil")
                    API.like(tweet_id=tweets[random_index].id)
                    totalA = totalA - 1
                except twitter.TweepyException as e:
                    pass
                    print(e)
            else:
                break
       

def autopostingAkunBackUp():
   API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
   API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
   BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
   ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
   SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

   auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
   auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
   API = twitter.API(auth)

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

    statusTweet = "‼ PROMO DISKON ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3],accountResult[i][0], accountResult[i][1] , "Twitter" ))

    try:
        api.update_status(status=statusTweet, media_ids=[media.media_id])
        print(accountResult[i][2])
        print("✅ - Posting Berhasil\n")
    except:
        pass   
           

def autoRepostAkunAyah() :
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
    userIDaccount = "masitowae"

    tweets = API.user_timeline(screen_name=userIDaccount, count=100, include_rts=False, tweet_mode='extended')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_shopee, no, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=2 AND username <> 'imamto2003'")

    accountResult = mycursor.fetchall()

    for x in range(len(accountResult)):
        auth = twitter.OAuth1UserHandler(
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
            accountResult[x][4], accountResult[x][5]
        )
        api = twitter.API(auth)

        print("Account : {}".format(accountResult[x][3]))

        totalA = 2
        for index in range(len(tweets)-1, 0, -1):
                if totalA != 0:
                    try :
                        random_index = random.randrange(len(tweets))
                        api.unretweet(id =tweets[random_index].id)
                        api.retweet(id=tweets[random_index].id)
                        print("✅ - Repost Berhasil")
                        totalA = totalA - 1
                    except twitter.TweepyException as e:
                        pass
                        print(e)
                else:
                    break
 
def shortLinkShopee(link, idshopee, akun, sosialmedia):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, appid, rahasia FROM account_shopeeaff WHERE id={}".format(idshopee))
    account_shopee = mycursor.fetchall()

    from shopee_affiliate import ShopeeAffiliate    
    sa = ShopeeAffiliate(account_shopee[0][1], account_shopee[0][2])
    res = sa.generateShortLink(link, akun, sosialmedia)
    res = res.replace("shope", "shpe")
    return(res)