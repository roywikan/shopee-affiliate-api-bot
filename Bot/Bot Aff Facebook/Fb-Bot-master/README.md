# Fb-Bot
Facebook bot

## Overview
This program automatically posts a picture in facebook page after a certain time.

## Features
- First the [scrape.py](https://github.com/RitikSibjr/Fb-Bot/blob/master/pkg/scrape.py) program scrapes the website and collects the all the quotes present in the site. The scrapped quotes are saved to a file.
- [pic.py](https://github.com/RitikSibjr/Fb-Bot/blob/master/pkg/pic.py) program selects one random quote from the file. The program creates an image then the quote is written in the image and saves the image.
- [bot.py](https://github.com/RitikSibjr/Fb-Bot/blob/master/pkg/bot.py) gets the image saved from the [pic.py](https://github.com/RitikSibjr/Fb-Bot/blob/master/pkg/pic.py) and posts into the facebook page. 
