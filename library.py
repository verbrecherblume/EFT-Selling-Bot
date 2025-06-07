from time import sleep
from typing import Any, Sequence
import cv2 as cv
import numpy as np
import pyautogui as gui
import pytesseract
import requests

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#find specified icon
def find_icon(icon: str) -> tuple[Sequence[int], tuple[int, int | Any]] | None:
    screenshot = gui.screenshot()
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    template = cv.imread(icon, cv.IMREAD_COLOR)
    w, h = template.shape[1], template.shape[0]

    result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        top_right = (top_left[0] + w, top_left[1])
        bottom_left = (top_left[0], top_left[1] + h)

        print(f"top_left: {top_left}, top_right: {top_right}, bottom_right: {bottom_right}")

        print(f"Icon gefunden bei: {top_left} – Übereinstimmung: {max_val:.2f}")
        return top_left, bottom_left, top_right, bottom_right
    else:
        print("Icon nicht gefunden.")
        return None


#size des Bildschirm rausfinden
def get_max_size() -> tuple[int, int, int, int]:
    x: int = 0
    y: int = 0
    z: bool = True
    while True:
        if gui.onScreen(x, y) == False:
            break

        x += 1
    max_x: int = x

    x = 0

    while True:
        if gui.onScreen(x, y) == False:
            break

        x -= 1
    min_x: int = x

    while True:
        if gui.onScreen(x-1, y) == False:
            break
        y += 1
    max_y: int = y

    y = 0

    while True:
        if gui.onScreen(x-1, y) == False:
            break
        y += 1
    min_y: int = y

    return min_x, min_y, max_x, max_y

def read_item_name(x: int, y: int, width: int, height: int) -> str:
    screenshot = gui.screenshot(region=(x, y, width, height))
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    return pytesseract.image_to_string(img, lang="eng")


def calculate_width_height(top_left: tuple[int, int], bottom_right: tuple[int, int]) -> tuple[int, int]:
    width: int = bottom_right[0] - top_left[0]
    height: int = bottom_right[1] - top_left[1]
    return width, height



#cursor auf den ersten slot setzen
def cursor_auf_anfang() -> tuple[float, float]:
    #Koordinaten erster Slot (1266, 80)
    # Koordinaten zweiter Slot (1329, 80)
    # Dimensionen eines Slots: 63 * 63
    return (1266 + 63/2, 80 + 63/2)



def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def highest_vendor(data: dict) -> tuple[str, int]:
    max_price: int = 0
    max_price_vendor: str
    counter: int = 0
    for item in data['data']['items'][0]['sellFor']:
        if item['price'] > max_price:
            max_price = item['price']
            max_price_vendor = item['vendor']['name']

        counter += 1

    return (max_price_vendor, max_price)

def sell_to_vendor(vendor_price: tuple[str, int]) -> None:
    if vendor_price[0] == "Flea Market":
        location = find_icon("./Pictures/add_offer.png")
        deviation: tuple[int, int] = (location[3][0] - location[0][0], location[3][1] - location[0][1])
        middle: tuple[int, int] = (location[0][0] + deviation[0]/2, location[0][1] + deviation[1]/2)

        gui.moveTo(middle[0], middle[1], duration=0.2)

        while True:
            if find_icon("./Pictures/maximum_offers.png") is not None:
                print("schlafe fuer 5 sekunden")
                sleep(5)
                continue
            break



        #gui.click(middle[0], middle[1], duration=0.2)


        gui.click(x=960, y=475, duration=0.2)
        gui.write(str(vendor_price[1]))

        location = find_icon("./Pictures/place_offer.png")
        deviation: tuple[int, int] = (location[3][0] - location[0][0], location[3][1] - location[0][1])
        middle: tuple[int, int] = (location[0][0] + deviation[0] / 2, location[0][1] + deviation[1] / 2)

        gui.moveTo(middle[0], middle[1], duration=0.2)
        #change to gui.click()



        #print(find_icon("./Pictures/requirements.png")[0])











