from distutils.log import info
from itertools import count
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

# Login Pinters
pinterest = Pinterest(email='fresmaazz@gmail.com',
                      password='Azzukhruf26',
                      username='id_myfashion',
                      cred_root='cred_root')


# Database
userID = "spongebobnfess"

idDataBaseItem = '15JVk3QaMzRIzvXGq8KNgUO4i6RFyG12h0BXUKlrFf2Q'

db = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{idDataBaseItem}/export?format=csv")


# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="shopeeaff"
)

# AUTO POSTING id_myfashion
def autoposting():
    print("\n\n🟧 AUTO POSTING : {}\n".format(datetime.now()))

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved")

    accountResult = mycursor.fetchall()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")

    database_post = mycursor.fetchall()

    for x in range(len(accountResult)):
        auth = twitter.OAuthHandler(accountResult[x][1], accountResult[x][2])
        auth.set_access_token(accountResult[x][4], accountResult[x][5])
        api = twitter.API(auth)

        profile = api.update_profile()

        print("\nAccount : {}".format(profile.name) + " ({})".format(profile.screen_name))

        random_index = random.randrange(len(database_post))

        # upload image
        urllib.request.urlretrieve('{}'.format(database_post[random_index][4]), "imagePost.png")
        
        statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3]))
        media = api.media_upload("imagePost.png")
        api.update_status(status=statusTweet, media_ids=[media.media_id])

        # Post Telegram
        message = 'https://api.telegram.org/bot5479078966:AAECnT7JEy4hNpjHGUzdZtSTsgOOjN22O_8/sendPhoto?chat_id=-1001658353827&photo={}&caption={}'.format(database_post[random_index][4], statusTweet)
        requests.post(message)

# AUTO RETWEET AKUN fresma_a
def retweetSecAccount():

    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    usernameAccount = "fresma_a"

    print("\n\n🟩 AUTO RETWEET BASE MUTUALAN : {}\n".format(datetime.now()))

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    api = twitter.API(auth)

    profile = api.update_profile()

    tweets = api.user_timeline(screen_name=usernameAccount,
                                # 200 is the maximum allowed count
                                count=1,
                                include_rts=True,
                                # Necessary to keep full_text
                                # otherwise only the first 140 words are extracted
                                tweet_mode='extended'
                                )

    for info in tweets[:1]:
        print(info.full_text)
        try :
            api.unretweet(info.id)
            print("Berhasil di Unretweet")
        except twitter.TweepyException as e:
            pass
            print(e)
        print("\n")

    tweets = api.user_timeline(screen_name=userID,
                                # 200 is the maximum allowed count
                                count=1,
                                include_rts=False,
                                # Necessary to keep full_text
                                # otherwise only the first 140 words are extracted
                                tweet_mode='extended'
                                )

    for info in tweets[:1]:                                                                                                                                     
        print("Account : {}".format(profile.name) +" ({})".format(profile.screen_name))
        print(info.full_text)
        if info.retweeted == True:
            print("❌ - Sudah diretweet")
        else:
            api.retweet(info.id)                                                                                                                                                                                                                    
            print("✅ - Berhasil di retweet")
        print("\n")

# Retweet Akun bayangan ke Spongebob
def autoRetweetNonEleved():
    # Minta bantuan akun eleved
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
   
    tweets = API.user_timeline(screen_name=userID,
                                   # 200 is the maximum allowed count
                                   count=1,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )

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

# Repost Barang dari akun id_myfashion ke akun bayangan
def autorepostNonEleved() :
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    api = twitter.API(auth)
    # random_index_id = random.randrange(len(acEleved))
    userIDaccount = "id_myfashion"

    tweets = api.user_timeline(screen_name=userIDaccount,
                                   # 200 is the maximum allowed count
                                   count=200,
                                   include_rts=False,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved")

    accountResult = mycursor.fetchall()

    for x in range(8):
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

# Account Thread
def autopostThred():

    iddatabaseThread = '1cyNu0v-4x045vcJs_qIvJGnsSX28SVL--4zu8qIcnYo'

    acdbThread = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{iddatabaseThread}/export?format=csv")

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved")

    accountResult = mycursor.fetchall()

    for x in range(len(accountResult)):
        API = twitter.Client(bearer_token=accountResult[x][3], consumer_key=accountResult[x][1], consumer_secret=accountResult[x][2], access_token=accountResult[x][4], access_token_secret=accountResult[x][5])
        print("Account : {}".format(accountResult[x][0]))

        for index in range(0, len(acdbThread), 1):
                    try :
                        API.unretweet(source_tweet_id =acdbThread.iloc[index,1])
                        API.retweet(tweet_id=acdbThread.iloc[index,1])
                        print("✅ - Repost Berhasil - {}".format(acdbThread.iloc[index,1]))
                    except twitter.TweepyException as e:
                        pass
                        print(e)

# Auto Posting Pinterest
def postingPinterest():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")

    database_post = mycursor.fetchall()

    random_index = random.randrange(len(database_post))

    board_id='1089800878518777159'
    section_id=None
    image_url= database_post[random_index][4]
    description='#racunshopee #racuntiktok #racunshopeecheck #racunshopeehaul #racunshopeecheckout #racunshopeemurah #racuntiktokcheck #racunbelanja #racunootd #ootdindonesia #ootdindo #ootdindomen #ootdindokece #ootdcowok #outfitkekinian #outfitmurah #fashionpria #lokalbrand #lokalpride #lokalbrandindonesia #lokalprideindonesia #lokalproduk #brandlokal #produklokal #brandlokalindonesia #brandlocal #brandlocalindonesia'
    title= database_post[random_index][0]
    alt_text='alt text'
    link= shortLinkShopee(database_post[random_index][3])

    try:
        pinterest.pin(board_id=board_id, image_url=image_url, description=description, title=title, link=link)
        print("✅ - Posting Berhasil\n")
    except:
        pass


def shortLinkShopee(link):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT appid, rahasia FROM account_shopeeaff")
    account_shopee = mycursor.fetchall()

    from shopee_affiliate import ShopeeAffiliate    
    sa = ShopeeAffiliate(account_shopee[0][0], account_shopee[0][1])
    res = sa.generateShortLink(link)
    res = res.replace("shope", "shpe")

    return(res)

def autopostingBackup():
    print("\n\n🟧 AUTO POSTING : {}\n".format(datetime.now()))

    mycursor = mydb.cursor()

    mycursor.execute("SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved")

    accountResult = mycursor.fetchall()

    for x in range(0, 1, 1):
        auth = twitter.OAuthHandler(accountResult[x][1], accountResult[x][2])
        auth.set_access_token(accountResult[x][4], accountResult[x][5])
        api = twitter.API(auth)

        profile = api.update_profile()

        print("\nAccount : {}".format(profile.name) + " ({})".format(profile.screen_name))

        random_index = random.randrange(len(db))

        # upload image
        urllib.request.urlretrieve('{}'.format(db.iloc[random_index, 4]), "imagePost.png")
        
        statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(db.iloc[random_index, 0], db.iloc[random_index, 2], db.iloc[random_index, 3])
        media = api.media_upload("imagePost.png")
        api.update_status(status=statusTweet, media_ids=[media.media_id])

        # Post Telegram
        message = 'https://api.telegram.org/bot5479078966:AAECnT7JEy4hNpjHGUzdZtSTsgOOjN22O_8/sendPhoto?chat_id=-1001658353827&photo={}&caption={}'.format(db.iloc[random_index, 4], statusTweet)
        requests.post(message)
        print("✅ - Posting Berhasil\n")

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

   mycursor.execute("SELECT id,username, access_token, access_token_secret FROM account_backup")

   accountResult = mycursor.fetchall()

   mycursor.execute("SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post")

   database_post = mycursor.fetchall()

   print(accountResult)

   for i in range(len(accountResult)):
          
    random_index = random.randrange(len(database_post))

    urllib.request.urlretrieve('{}'.format(database_post[random_index][4]), "imagePost.png")
          
    media = API.media_upload("imagePost.png", additional_owners=[accountResult[i][0]])

    auth = twitter.OAuth1UserHandler(
        "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
        accountResult[i][2], accountResult[i][3]
    )
    api = twitter.API(auth)

    statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index][0], database_post[random_index][2], shortLinkShopee(database_post[random_index][3]))

    try:
        api.update_status(status=statusTweet, media_ids=[media.media_id])
        print("✅ - Posting Berhasil\n")
    except:
        pass


def statusBot():
    statusbot = "1nzzMebmvMyODar_9LivVMh7U8UuGwAwUL6kQzSZaAtI"

    status = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{statusbot}/export?format=csv")

    if(status.iloc[0][0] == "Aktif"):
        print("Bot Berjalan")
    else :
        print("Bot Mati")
        exit()

schedule.every(15).minutes.do(autoposting)
schedule.every(35).minutes.do(autopostingBackup)
schedule.every(10).minutes.do(retweetSecAccount) 
schedule.every(10).minutes.do(autoRetweetNonEleved)
schedule.every(15).minutes.do(autorepostNonEleved)
schedule.every(1444).minutes.do(autopostThred)
schedule.every(30).minutes.do(postingPinterest)
schedule.every(60).minutes.do(statusBot)
schedule.every(45).minutes.do(autopostingAkunBackUp)


while True:
    schedule.run_pending()
    time.sleep(1)


def autoRetweetNonEleved():
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
   
    tweets = API.user_timeline(screen_name=userID,
                                   # 200 is the maximum allowed count
                                   count=1,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=1")

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

def autorepostNonEleved() :
    API_KEY = "l8QEIHkBbb7Zpviv7ggt4XNpi"
    API_SECRET_KEY = "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAFrcgEAAAAADBt2zOc80n%2B6VnrIFjKzMwfhP%2B4%3DexqN2RgSuElNEqmOgdH6vecjFDoX1XTYHOGvGqfHrvjE5vke37"
    ACCESS_TOKEN = "975213506696855553-UcOW4U41SPc5XgwylP1FnHeYLKbTR9N"
    SECRET_ACCESS_TOKEN = "kQM4qyISdaPrRBFOjb0zfRpUKMdmG7UBXpgrDNDrxQs5E"

    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
    userIDaccount = "id_myfashion"

    tweets = API.user_timeline(screen_name=userIDaccount,
                                   # 200 is the maximum allowed count
                                   count=200,
                                   include_rts=False,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_shopee, no, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=1 ORDER BY no DESC")

    accountResult = mycursor.fetchall()

    for x in range(8):
        auth = twitter.OAuth1UserHandler(
            "l8QEIHkBbb7Zpviv7ggt4XNpi", "eM4Id0y0DiTLT3TJNZ9MDxZOUlx1rt5njK012vdt7RTligP77N",
            accountResult[x][4], accountResult[x][5]
        )
        api = twitter.API(auth)

        print("Account : {}".format(accountResult[x][3]))

        totalA = 3
        for index in range(len(tweets)-1, 0, -1):
                if totalA != 0:
                    try :
                        random_index = random.randrange(len(tweets))
                        api.unretweet(id =tweets[random_index].id)
                        api.retweet(id=tweets[random_index].id)
                        print("✅ - Repost Berhasil")
                        totalA = totalA - 1
                        api.create_favorite(id=tweets[random_index].id)
                    except twitter.TweepyException as e:
                        pass
                        print(e)
                else:
                    break