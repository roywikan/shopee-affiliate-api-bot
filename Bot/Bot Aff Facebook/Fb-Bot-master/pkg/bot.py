import time
import facebook as fb
from pic import image

acess_token = "EAAS1MRIVS4gBACfhbHeK3KdLUQi7UrbXAOKaYwjZCZBPN5GdYPuTbkjQLqGoGeAVUNAKQ62AWWSfyTcPHzL75DqHZBziSlwfRH5O7qAnR4znh36Rvx5kqgrwqhDZABkTg5APrWa3I0PPRkJXlkYDeR3x1oh4V7xFm7IlFJxPupyak5ClUy1U"

y = fb.GraphAPI(acess_token)
while True:
    image()
    y.put_photo(open("pic.jpg","rb") ,message="Quotes__")
    #uploads a image after an hour
    time.sleep(3600)

