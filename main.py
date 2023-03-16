import time
import schedule
from bot.botFacebook import *
from bot.botTwitter import *
from bot.botPinterest import *
from bot.botTelegram import *
from bot.botReplyTwitter import *
from bot.postVideoTwiiter import * 

# # Twitter
# # schedule.every(25).minutes.do(autoposting)
# schedule.every(30).minutes.do(autoRetweetNonEleved)
# # schedule.every(18).minutes.do(autoRepostNonEleved)
# schedule.every(25).minutes.do(autopostingAkunBackUp)
# # schedule.every(20).minutes.do(autoRepostAkunAyah)
# schedule.every(45).minutes.do(autopostingTrendingTopik)

# # Twitter - post video
# # schedule.every(200).minutes.do(postingVideo)

# # Reply Twitter
# # schedule.every(30).minutes.do(posting)

# # Telegram
# schedule.every(30).minutes.do(autoPostingTelegram)

# # Pinterest
# schedule.every(30).minutes.do(autoPostingPinterest)

# # Facebook
# schedule.every(30).minutes.do(autoPostingFacebook)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

autoRetweetNonEleved()