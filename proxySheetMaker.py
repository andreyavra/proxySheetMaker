import requests
import json
import numpy as np
import urllib
import cv2
import webreq

from PIL import Image
from io import BytesIO

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, landscape, A4

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
import reportlab.platypus as platypus # includes: SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader



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

    doc = canvas.Canvas("proxySheet.pdf")

    print("Printing Coordinates of an A4:", A4)
    doc.drawString(9,831,"My name's Hayato and I got 37 ATAR :(")
    # Coords start from bottom left, and each point is 1/72 inches
    

    i = 0
    numTotalCards = len(cards)
    price = 0
    # xcoords = (10,10+58*mm,10+2*58*mm)
    # ycoords = (831,831-86*mm,831-2*86*mm)
    counter = 0
    while i < numTotalCards:
        cardInfo = webreq.get_api_dict(mainAPI, {"name": cards[i][CARD_NAME]})

        price+=float(cardInfo['card_prices']['tcgplayer_price'])

        imgURL = imageAPI + cardInfo['id'] + ".jpg"
        print("Printing imgURL:", imgURL)

        # response = requests.get(imgURL)
        # img = Image.open(BytesIO(response.content))

        # >>> img = ImageReader(imgURL)
        # img = getImg(imgURL, 86, 58)

        # >>>doc.drawImage(img, 10, 10, mask='auto')

        j = 0
        while j<cards[i][NUM_OF_CARDS]:
            doc.drawImage(imgURL, 10, 10, width=59*mm, height=86*mm, mask='auto')
            doc.showPage()
            j+=1

        i+=1
    print('Hey povo. Fucking buy the deck for ${price} at TCG player.'.format(price=price))
    doc.save()

    return "ABC"




def send_pdf(pdf):
    print("Sent!")




def getImg(url, newWidth, newHeight):
    ''' uses mm you american scum '''
    # iw, ih = img.getSize()
    # aspect = ih / float(iw)
    print(url)
    return platypus.Image(url, width=newWidth, height=newHeight)



main()


# SOLUTIONS TO GET IMAGE:

'''
from PIL import Image
import requests
from io import BytesIO

response = requests.get(url)
img = Image.open(BytesIO(response.content))
'''