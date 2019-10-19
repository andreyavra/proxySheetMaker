# Proxy Sheet Maker
# by Andrey Avramenko

# Given an input of y or t, and the corresponding deck.ydk or 
# cardList.txt in the same directory, outputs a PDF in the same 
# directory of the corresponding cards.

# Libraries required:
# requests, json, io, reportlab, PIL, time


# Guide to the API that this program uses:
# https://db.ygoprodeck.com/api-guide/

import requests
import json

from io import BytesIO
from PIL import Image


from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import reportlab.platypus as platypus 

from time import time


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
    startTimer = time()
    # Getting a list of the user's cards
    cards = get_user_cards(choice)
    # Creating a PDF
    create_pdf(cards, choice)
    endTimer = time()
    print("Time taken:", endTimer-startTimer)



def get_user_cards(choice):
    '''Given a choice for the correponding file format, ('y' for .ydk
    and 't' for .txt), returns the cards in the corresponding file 
    ('deck.ydk' or 'cardList.txt') that is in the current directory.'''
    cards = []
    if choice == 't':
        # Opening the corresponding file
        with open("cardList.txt") as f:
            for item in f:
                item = item.strip()
                # Finding the index between the number of cards and 
                # the card name
                i = 0
                while item[i] != ' ':
                    i+=1
                # Slicing the string at the index found above
                numCards = int(item[:i])
                cardName = item[(i+1):]
                # Appending this information into the total cards
                cards.append((cardName, numCards))
    else:
        # Opening the corresponding file
        with open("deck.ydk") as f:
            # Doing frequency analysis for all of the cards to account
            # for lack of frequency in a .ydk file.
            d = {}
            for item in f:
                item = item.strip()
                if item[0] != '#' and item[0] != '!' and item[0] != '':
                    d[item] = d.get(item, 0) + 1
            # Adding this information to the cards list
            for cardName in d:
                cards.append((cardName, d[cardName]))
    return cards




def create_pdf(cards, choice):
    '''Given cards in the tuple form (cardName, numCard), and the 
    format the cards are in, indestructively returns a pdf of all
    of the cards specified.'''
    # Defining APIs
    mainAPI = "https://db.ygoprodeck.com/api/v5/cardinfo.php"
    imageAPI = "https://storage.googleapis.com/ygoprodeck.com/pics/"

    # Initialising the PDF (default A4)
    doc = canvas.Canvas("proxySheet.pdf")
    # Adding a header to the PDF
    doc.drawString(9,831,"Andrey Avramenko is the best!")

    numTotalCards = len(cards)
    # Establishing counter for the number of cards on a PDF - max. is 9
    counter = 0
    i = 0
    # Looping through the cards to put them onto the PDF
    while i < numTotalCards:
        if choice == 't':
            # Getting the json file at the API as a dictionary 
            cardInfo = get_api_dict(mainAPI, 
                {"name": cards[i][CARD_NAME]})
            print("Adding card with ID:", cardInfo['id'])
            # Creating the imgURL to get the image from
            imgURL = imageAPI + cardInfo['id'] + ".jpg"
        else:
            # Creating the imgURL to get the image from
            imgURL = imageAPI + cards[i][0] + ".jpg"
        
        # Getting the image from the URL
        cardImg = get_img_from_url(imgURL)

        print(imgURL)
        

        # Making sure to put on the PDF the amount of cards specified
        j = 0
        while j < cards[i][NUM_OF_CARDS]:
            # Getting the future card position in the PDF as 
            # coordinates
            coords = get_coords(counter)
            # Putting the image onto the PDF
            doc.drawImage(cardImg, coords[0], coords[1], width=59*mm, 
                height=86*mm, mask='auto')
            if counter == 8: # Meaning the page is full
                # Creating new page
                doc.showPage()
                # Adding header onto new page on the PDF
                doc.drawString(9,831,"Andrey Avramenko is the best!")
                # Resetting the counter
                counter = 0
            else:
                # Adding that a card was drawn to the tally
                counter+=1
            j+=1
        print("Card added", cards[i][NUM_OF_CARDS], "times!")
        i+=1
    # Saving the PDF in the current directory.
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
        

def get_img_from_url(url):
    '''Given a url to an image as a string, returns the image as a 
    reportlab image object.'''
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return ImageReader(img)

    



def get_api_dict(API, paramsForAPI):
    ''' Given a url to a .json API as a string, like so: and the 
    parameters to the API in a dictionary, returns that information as 
    a dictionary in the form: {"name": "foo"}, returns the .json file 
    at the API as a dictionary.'''
    try:
        response = requests.get(API, paramsForAPI)
    except:
        ("URL is invalid, or parameters are invalid for the URL")
    
    try:
        dictionary = json.loads(response.text[1:-1]) 
        return dictionary
    except:
        raise NameError("URL is not an API that goes to a .json")
    


if __name__ == '__main__':
    main()