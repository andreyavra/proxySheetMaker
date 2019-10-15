# proxySheetMaker
Welcome to the Yu-Gi-Oh! Proxy Sheet Maker! This service allows for easy creation of Yu-Gi-Oh! proxy sheets. 

# Running the App
To run the app, make sure you have the following libraries installed: requests; json; io; reportlab

Run the app through the terminal - in ./, python3 proxySheetMaker.py, then type either t or y depending on the type of decklist you want to turn into a PDF.

You can change cardList.txt, changing the card quantities, or adding them. Cards in cardList.txt should be in the format:
3 Decode Talker

The cards in deck.ydk are based on card IDs. To add multiple of a card, rewrite the ID on the next line.