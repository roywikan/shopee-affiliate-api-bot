import time
import schedule
from bot.botFacebook import *
from bot.botTwitter import *
from bot.botPinterest import *
from bot.botTelegram import *
from bot.botReplyTwitter import *
from bot.postVideoTwiiter import * 
from function_list import *

# Twitter
schedule.every(funtion('autoposting')[0]['set_time']).minutes.do(autoposting)
schedule.every(funtion('autoRetweetNonEleved')[0]['set_time']).minutes.do(autoRetweetNonEleved)
schedule.every(funtion('autoRepostNonEleved')[0]['set_time']).minutes.do(autoRepostNonEleved)
schedule.every(funtion('autopostingAkunBackUp')[0]['set_time']).minutes.do(autopostingAkunBackUp)
# schedule.every(funtion('autoRepostAkunAyah')[0]['set_time']).minutes.do(autoRepostAkunAyah)
schedule.every(funtion('autopostingTrendingTopik')[0]['set_time']).minutes.do(autopostingTrendingTopik)

# Twitter - post video
schedule.every(funtion('postingVideo')[0]['set_time']).minutes.do(postingVideo)

# Reply Twitter
# schedule.every(funtion('posting')[0]['set_time']).minutes.do(posting)

# Telegram
schedule.every(funtion('autoPostingTelegram')[0]['set_time']).minutes.do(autoPostingTelegram)

# Pinterest
schedule.every(funtion('autoPostingPinterest')[0]['set_time']).minutes.do(autoPostingPinterest)

# Facebook
schedule.every(funtion('autoPostingFacebook')[0]['set_time']).minutes.do(autoPostingFacebook)

bar = [
    ".     ",
    " .    ",
    "  .   ",
    "   .  ",
    "    . ",
    "     .",
    "    . ",
    "   .  ",
    "  .   ",
    " .    ",
]
i = 0

while True:
    print("The bot is running", bar[i % len(bar)], end="\r")
    schedule.run_pending()
    time.sleep(1)
    i += 1
