import tweepy as twitter
import pandas as pd
import random
import urllib.request
import requests
import schedule
import mysql.connector
from decouple import config
from bot.database import *
from function_list import *

idDataBaseItem = '15JVk3QaMzRIzvXGq8KNgUO4i6RFyG12h0BXUKlrFf2Q'
db = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{idDataBaseItem}/export?format=csv")

# API BotTwitter
def botTwitter():
    API_KEY = config('API_KEY')
    API_SECRET_KEY = config('API_SECRET_KEY')
    BEARER_TOKEN = config('BEARER_TOKEN')
    ACCESS_TOKEN = config('ACCESS_TOKEN')
    SECRET_ACCESS_TOKEN = config('SECRET_ACCESS_TOKEN')
    
    auth = twitter.OAuthHandler(API_KEY,  API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    API = twitter.API(auth)
    
    return API


# AUTO POSTING id_myfashion
def autoposting():
    if(funtion('autoposting')[0]['is_active'] == 1) :
        print("\n\n🟧 AUTO POSTING\n")

        query = "SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_eleved"
        accountResult = db_connection(query)

        query = "SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post"
        database_post = db_connection(query)

        shopeid =1

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
                    api.update_status(status=statusTweet, media_ids=[media.media_id])
                    print("✅ - Posting Berhasil")
                except:
                    pass
            except:
                pass
        

# Retweet Spongebob to Akun BackUp
def autoRetweetNonEleved():
    if(funtion('autoRetweetNonEleved')[0]['is_active'] == 1) :
        userID = "spongebobnfess"
        tweets = botTwitter().user_timeline(screen_name=userID, count=1, tweet_mode='extended')

        query = "SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved WHERE is_retweet = 1"
        accountResult = db_connection(query)

        for account in accountResult:
            api = twitter.Client(bearer_token=account['BEARER_TOKEN'], consumer_key=account['API_KEY'], consumer_secret=account['API_SECRET_KEY'], access_token=account['ACCESS_TOKEN'], access_token_secret=account['SECRET_ACCESS_TOKEN'])
            # print("Account : {}".format(account['username']))

            for info in tweets[:1]:
                print("ID : {}".format(info.id))

            try:
                api.retweet(tweet_id=info.id)
                print("✅ - Retweet Berhasil\n")
            except twitter.TweepyException as e:
                pass
                print(e)
        
        # Sementara
        query = "SELECT id_shopee, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=1 AND is_retweet = 1"
        accountResult = db_connection(query)

        for account in accountResult:
            auth = twitter.OAuth1UserHandler(
                config('API_KEY'), config('API_SECRET_KEY'),
                account['access_token'], account['access_token_secret']
            )
            api = twitter.API(auth)

            # print("Account : {}".format(account['username']))

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
    if(funtion('autoRepostNonEleved')[0]['is_active'] == 1) :
        userIDaccount = "id_myfashion"

        tweets = botTwitter().user_timeline(screen_name=userIDaccount, count=200, include_rts=False, tweet_mode='extended')

        query = "SELECT username, API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, SECRET_ACCESS_TOKEN FROM account_non_eleved WHERE is_retweet = 1"
        accountResult = db_connection(query)

        for account in accountResult:
            API = twitter.Client(bearer_token=account['BEARER_TOKEN'], consumer_key=account['API_KEY'], consumer_secret=account['API_SECRET_KEY'], access_token=account['ACCESS_TOKEN'], access_token_secret=account['SECRET_ACCESS_TOKEN'])
            # print("Account : {}".format(account['username']))

            totalRetweet = 2
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
    if(funtion('autopostingAkunBackUp')[0]['is_active'] == 1) :
        query = "SELECT * FROM account_backup where id_shopee = '1' AND is_active = 1"
        accountResult = db_connection(query)

        query = "SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post"
        database_post = db_connection(query)

        for account in accountResult:
            random_index = random.randrange(len(database_post))
            
            try:
                urllib.request.urlretrieve('{}'.format(database_post[random_index]['product_img']), "imagePost.png")
                    
                media = botTwitter().media_upload("imagePost.png", additional_owners=[account['id_twitter']])

                auth = twitter.OAuth1UserHandler(
                    config('API_KEY'), config('API_SECRET_KEY'),
                    account['access_token'], account['access_token_secret']
                )
                api = twitter.API(auth)

                statusTweet = "‼ FLASH SALE ‼\n\n{}\n\n⛔️ DISKON : {}\n\nCheckout Sekarang 👇\n{}".format(database_post[random_index]['product_name'], database_post[random_index]['product_rating'], shortLinkShopee(database_post[random_index]['product_link'],account['id_shopee'], account['id_twitter'] , "Twitter" ))

                try:
                    api.update_status(status=statusTweet, media_ids=[media.media_id])
                    # print(account['username'])
                    print("✅ - Posting Berhasil\n")
                except:
                    pass   
            except:
                pass
           
# Repost akun backUp Ayah ke masitowae
def autoRepostAkunAyah() :
    if(funtion('autoRepostAkunAyah')[0]['is_active'] == 1) :
        userIDaccount = "masitowae"
        tweets = botTwitter().user_timeline(screen_name=userIDaccount, count=100, include_rts=False, tweet_mode='extended')

        query = "SELECT id_shopee, no, id, username, access_token, access_token_secret FROM account_backup WHERE id_shopee=2 AND username <> 'imamto2003'"
        accountResult = db_connection(query)

        for account in accountResult:
            auth = twitter.OAuth1UserHandler(
                config('API_KEY'), config('API_SECRET_KEY'),
                account['access_token'], account['access_token_secret']
            )
            api = twitter.API(auth)

            # print("Account : {}".format(account['username']))

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
    if(funtion('autopostingTrendingTopik')[0]['is_active'] == 1) :
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

        query = "SELECT * FROM account_backup WHERE username='HappyRacun'"
        accountResult = db_connection(query)

        query = "SELECT product_name, product_price, product_rating, product_link, product_img FROM database_post"
        database_post = db_connection(query)

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
                # print(account['username'])
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