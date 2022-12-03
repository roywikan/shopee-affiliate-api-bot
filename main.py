import time
import schedule
from bot.botFacebook import *
from bot.botTwitter import *
from bot.botPinterest import *
from bot.botTelegram import *

# Twitter
schedule.every(15).minutes.do(autoposting)
schedule.every(35).minutes.do(autopostingBackup)
schedule.every(10).minutes.do(retweetSecAccount) 
schedule.every(10).minutes.do(autoRetweetNonEleved)
schedule.every(15).minutes.do(autorepostNonEleved)
schedule.every(30).minutes.do(postingPinterest)
schedule.every(60).minutes.do(statusBot)
schedule.every(30).minutes.do(autopostingAkunBackUp)
schedule.every(20).minutes.do(autorepostAkunAyah)

# Telegram
schedule.every(30).minutes.do(autoPostingTelegram)

# Pinterest
schedule.every(30).minutes.do(autoPostingPinterest)

# Facebook
schedule.every(30).minutes.do(autoPostingFacebook)

while True:
    schedule.run_pending()
    time.sleep(1)