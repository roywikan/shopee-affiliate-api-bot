from bs4 import BeautifulSoup
import requests
from requests import HTTPError
import csv
import os

def check_url(url):
    try:
        res = requests.get(url)
        res.raise_for_status

    except HTTPError as h:
        raise h

    except Exception as e:
        raise e 

    else:
        return res

def get_content(res):
    soup = BeautifulSoup(res.text, "html.parser")
    c = soup.find_all("div", class_ = "listicle-slide listicle-slide-portrait listicle-slide-image listicle-slide-multi-retailer")
    for a in c:
        #gets author names
        author = a.find("span", class_ = "listicle-slide-hed-text").text
        #gets quotes
        quote = a.find("div", class_ = "listicle-slide-dek").p.text
        
        with open("quotes.txt", "a",  encoding="utf-8") as file:
            writer = csv.DictWriter(file,fieldnames=["quote", "author"])
            writer.writerow({"quote":quote ,"author":"-"+author})
    
        

def quotes():

    if os.path.getsize("quotes.txt") == 0:
        res = check_url("https://www.goodhousekeeping.com/health/wellness/g2401/inspirational-quotes/")
        if str(res) == "<Response [200]>":
            get_content(res)

        else:
            pass
    else:
        with open("quotes.txt") as file:
            for line in file:
                print(line)

if __name__ == "__main__":
    quotes()

    
