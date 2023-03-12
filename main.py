import time
import schedule
from bot.botTwitter import *

# Twitter
schedule.every(25).minutes.do(autopostingAkunBackUp)
schedule.every(20).minutes.do(autoRepostAkunAyah)
schedule.every(45).minutes.do(autopostingTrendingTopik)

while True:
    schedule.run_pending()
    time.sleep(1)
    print("Bots are running.......")