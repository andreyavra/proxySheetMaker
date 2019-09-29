import requests
import json
import numpy as np
import urllib
import cv2
import webreq

# https://storage.googleapis.com/ygoprodeck.com/pics/27551.jpg
# https://db.ygoprodeck.com/api/v5/cardinfo.php?name=Decode%20Talker
# https://db.ygoprodeck.com/api-guide/


CARD_NAME = 0
NUM_OF_CARDS = 1


def main():
    # print("<test>")

    # print("</test>")
    cards = get_user_cards()
    pdf = create_pdf(cards)
    send_pdf(pdf)


def get_user_cards():
    cards = []
    with open("cardList.txt") as f:
        for item in f:
            item = item.strip()
            i = 0
            while item[i] != ' ':
                i+=1
            numCards = int(item[:i])
            cardName = item[(i+1):]
            cards.append((cardName, numCards))
    return cards




def create_pdf(cards):
    mainAPI = "https://db.ygoprodeck.com/api/v5/cardinfo.php"
    imageAPI = "https://storage.googleapis.com/ygoprodeck.com/pics/"

    i = 0
    numTotalCards = len(cards)
    while i < numTotalCards:
        cardInfo = webreq.get_api_dict(mainAPI, {"name": cards[i][CARD_NAME]})

        imgURL = imageAPI + cardInfo['id'] + ".jpg"
        print("Printing imgURL:", imgURL)

        img = webreq.url_to_image(imgURL)

        print("ABC")

        webreq.display(img)

        print("DEF")

        

        
        i+=1

    return "ABC"




def send_pdf(pdf):
    print("Sent!")








main()


# SOLUTIONS TO GET IMAGE:

'''
from PIL import Image
import requests
from io import BytesIO

response = requests.get(url)
img = Image.open(BytesIO(response.content))
'''