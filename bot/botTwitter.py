import tweepy as twitter
import pandas as pd
import random
import urllib.request
from PIL import Image
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


# AUTO POSTING id_myfashion
def autoposting():
    print("\n\n🟧 AUTO POSTING\n")

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved")
    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()

    shopeid =1

    for account in accountResult:
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
            api.update_status(status=statusTweet, media_ids=[media.media_id])
            print("✅ - Posting Berhasil")
        except:
            pass
        

# Retweet Spongebob to Akun BackUp
def autoRetweetNonEleved():
    userID = "spongebobnfess"
    tweets = botTwitter().user_timeline(screen_name=userID, count=1, tweet_mode='extended')

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved")
    accountResult = mycursor.fetchall()

    for account in accountResult:
        api = twitter.Client(bearer_token=account['BEARER_TOKEN'], consumer_key=account['API_KEY'], consumer_secret=account['API_SECRET_KEY'], access_token=account['ACCESS_TOKEN'], access_token_secret=account['SECRET_ACCESS_TOKEN'])
        print("Account : {}".format(account['username']))

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

    for account in accountResult:
        auth = twitter.OAuth1UserHandler(
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
            account['access_token'], account['access_token_secret']
        )
        api = twitter.API(auth)

        print("Account : {}".format(account['username']))

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
    userIDaccount = "id_myfashion"

    tweets = botTwitter().user_timeline(screen_name=userIDaccount, count=200, include_rts=False, tweet_mode='extended')

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved WHERE username <> 'yusiedaynti' AND username <> '_firzaamanda' AND username <> 'vidyaisvara' AND username <> 'zannakirana_'")
    accountResult = mycursor.fetchall()

    for account in accountResult:
        API = twitter.Client(bearer_token=account['BEARER_TOKEN'], consumer_key=account['API_KEY'], consumer_secret=account['API_SECRET_KEY'], access_token=account['ACCESS_TOKEN'], access_token_secret=account['SECRET_ACCESS_TOKEN'])
        print("Account : {}".format(account['username']))

        totalRetweet = 3
        for index in tweets:
            if totalRetweet != 0:
                try :
                    random_index = random.randrange(len(tweets))
                    API.unretweet(source_tweet_id =tweets[random_index].id)
                    API.retweet(tweet_id=tweets[random_index].id)
                    print("✅ - Repost Berhasil")
                    API.like(tweet_id=tweets[random_index].id)
                    totalRetweet = totalRetweet - 1
                except twitter.TweepyException as e:
                    pass
                    print(e)
            else:
                break
                

def autopostingAkunBackUp():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup")
    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")
    database_post = mycursor.fetchall()

    for account in accountResult:
        random_index = random.randrange(len(database_post))

        urllib.request.urlretrieve('{}'.format(database_post[random_index]['product_img']), "imagePost.png")
            
        media = botTwitter().media_upload("imagePost.png", additional_owners=[account['id']])

        auth = twitter.OAuth1UserHandler(
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
            account['access_token'], account['access_token_secret']
        )
        api = twitter.API(auth)

        statusTweet = "‼ PROMO DISKON ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'],account['id_shopee'], account['id'] , "Twitter" ))

        try:
            api.update_status(status=statusTweet, media_ids=[media.media_id])
            print(account['username'])
            print("✅ - Posting Berhasil\n")
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
                

def shortLinkShopee(link, idshopee, akun, sosialmedia):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT id, appid, rahasia FROM account_shopeeaff WHERE id={}".format(idshopee))
    account_shopee = mycursor.fetchall()

    from shopee_affiliate import ShopeeAffiliate    
    sa = ShopeeAffiliate(account_shopee[0]['appid'], account_shopee[0]['rahasia'])
    res = sa.generateShortLink(link, akun, sosialmedia)
    res = res.replace("shope", "shpe")
    return(res)