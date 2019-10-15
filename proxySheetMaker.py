# Proxy Sheet Maker
# by Andrey Avramenko

# Given an input of y or t, and the corresponding deck.ydk or 
# cardList.txt in the same directory, outputs a PDF in the same 
# directory of the corresponding cards.

# Libraries required:
# requests, json, io, reportlab


# Guide to the API that this program uses:
# https://db.ygoprodeck.com/api-guide/

import requests
import json
from io import BytesIO

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import reportlab.platypus as platypus 
# platypus includes: SimpleDocTemplate, Paragraph, Spacer, Image


CARD_NAME = 0
NUM_OF_CARDS = 1
LMARGIN = 30
TMARGIN = 30


xcoords_for_getcoords = (
    LMARGIN, 
    LMARGIN+58*mm, 
    LMARGIN+2*58*mm
)
ycoords_for_getcoords = (
    841.8897637795277-TMARGIN-86*mm, 
    841.8897637795277-TMARGIN-2*86*mm, 
    841.8897637795277-TMARGIN-3*86*mm
)


def main():
    choice = input("Please enter y for deck.ydk, or t for "
        "cardList.txt: ").lower()[0]
    cards = get_user_cards(choice)
    create_pdf(cards, choice)



def get_user_cards(choice):
    '''Given a choice for the correponding file format, ('y' for .ydk
    and 't' for .txt), returns the cards in the corresponding file 
    ('deck.ydk' or 'cardList.txt') that is in the current directory.'''
    cards = []
    if choice == 't':
        with open("cardList.txt") as f:
            for item in f:
                item = item.strip()
                i = 0
                while item[i] != ' ':
                    i+=1
                numCards = int(item[:i])
                cardName = item[(i+1):]
                cards.append((cardName, numCards))
    else:
        with open("deck.ydk") as f:
            d = {}
            for item in f:
                item = item.strip()
                if item[0] != '#' and item[0] != '!' and item[0] != '':
                    d[item] = d.get(item, 0) + 1

            for cardName in d:
                cards.append((cardName, d[cardName]))
                
    return cards




def create_pdf(cards, choice):
    '''Given cards in the tuple form (cardName, numCard), and the 
    format the cards are in, indestructively returns a pdf of all
    of the cards specified.'''
    mainAPI = "https://db.ygoprodeck.com/api/v5/cardinfo.php"
    imageAPI = "https://storage.googleapis.com/ygoprodeck.com/pics/"

    doc = canvas.Canvas("proxySheet.pdf")

    print("Printing Coordinates of an A4:", A4)
    doc.drawString(9,831,"My name's Hayato and I got 37 ATAR :(")
    # Coords start from bottom left, and each point is 1/72 inches

    i = 0
    numTotalCards = len(cards)

    counter = 0
    while i < numTotalCards:
        if choice == 't':
            cardInfo = get_api_dict(mainAPI, {"name": cards[i][CARD_NAME]})
            imgURL = imageAPI + cardInfo['id'] + ".jpg"
        else:
            print(cards[i])
            imgURL = imageAPI + cards[i][0] + ".jpg"
            
        j = 0
        while j<cards[i][NUM_OF_CARDS]:
            coords = get_coords(counter)
            print("coords:", coords)
            doc.drawImage(imgURL, coords[0], coords[1], width=59*mm, height=86*mm, mask='auto')
            if counter == 8:
                doc.showPage()
                counter = 0
            else:
                counter+=1
            j+=1

        i+=1
    doc.save()
    


def get_coords(counter):
    '''Function not to be used directly.'''
    xcoord = xcoords_for_getcoords[counter%3]
    if counter <= 2:
        ycoord = ycoords_for_getcoords[0]
    elif counter <= 5:
        ycoord = ycoords_for_getcoords[1]
    else:
        ycoord = ycoords_for_getcoords[2]
    return (xcoord,ycoord)
        
    

def get_api_dict(API, paramsForAPI):
    ''' Given a url to a .json object, returns that information as a 
    dictionary.'''
    response = requests.get(API, paramsForAPI)
    dictionary = json.loads(response.text[1:-1]) 

    return dictionary


if __name__ == '__main__':
    main()