import textwrap
from PIL import Image, ImageDraw, ImageFont
import random
from string import ascii_letters
import csv

quotes = []
colors = ["darkgray", "darkgrey", "silver", "lightgray", "lightgrey", "gainsboro", "whitesmoke", "white", "snow", "aliceblue"]

def image():
    color = random.choice(colors)
    img = Image.new(mode="RGB", size=(1200,630), color=color)
    # img = Image.open("pics/1.jpg")
    I1 = ImageDraw.Draw(img)

    with open("quotes.txt",encoding="utf-8") as file:
        reader = csv.DictReader(file,fieldnames=["quote","author"])
        for line in reader:
            quotes.append(line)

    quote = random.choice(quotes)

    #choosed the font type and font size
    title_font = ImageFont.truetype('ariali.ttf', 90)
    
    avg_char_width = sum(title_font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    max_char_count = int( (img.size[0] * .95) / avg_char_width )
    scaled_wrapped_text = textwrap.fill(text=quote["quote"], width=max_char_count)
    title_text = scaled_wrapped_text

    #text is written in the image
    I1.text((img.size[0]/2 ,img.size[1]/2), title_text, fill =("black"), font=title_font, anchor="mm")
    img.save("pic.jpg")

if __name__ == "__main__":
    image()