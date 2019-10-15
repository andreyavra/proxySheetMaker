import requests
import json
import numpy as np
import urllib
import cv2


class Card:
    def __init__(self, id, name, type, race, desc, img, setID, atk=None, defense=None, attribute=None, linkVal=None, linkMarkers=None):
        self.name = name

    pass













def display(image):
    ''' Given an OpenCV-formatted NumPy list, displays the image'''
    # This opens a window displaying the image
    cv2.imshow("result", image)
    if cv2.waitKey(0) == ord('q'):
        return






if __name__ == "__main__":
    print("This program is not for running!")
    print("This is used for fast web requests.")
    print("To use this library, do the following in your program:")
    print("import webreq")
