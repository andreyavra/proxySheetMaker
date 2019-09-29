import requests
import json
import numpy as np
import urllib
import cv2


class Card:
    def __init__(self, name):
        self.name = name

    pass


def get_api_dict(API, paramsForAPI):
    ''' Given a url to a .json object, returns that information as a 
    dictionary. '''
    r = requests.get(API, paramsForAPI)
    # print("Printing first request: ")
    # print("URL: ", r.url)
    # print("ENCODING: ", r.encoding)
    # print("STATUS_CODE: ", r.status_code)
    # print("HEADERS: ", r.headers)
    # print("TEXT: ", r.text)
    # print("CONTENT: ", r.content)
    # print("JSON: ", r.json)
    # print("\n\n\n")

    d = json.loads(r.text[1:-1]) 

    return d


def url_to_image(url):
    ''' Given a url to an image and internet access, returns the image
    from the url as a OpenCV-formatted NumPy array. '''
    # Requesting the url
    resp = urllib.urlopen(url)
    # Decoding the reponse into a NumPy array
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # Decoding the NumPy array as an OpenCV image
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image





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
