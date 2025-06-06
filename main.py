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
def cursor_auf_anfang() -> None:
    #Koordinaten erster Slot (1266, 80)
    # Koordinaten zweiter Slot (1329, 80)
    # Dimensionen eines Slots: 63 * 63
    gui.moveTo(1266 + 63/2, 80 + 63/2)



def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def highest_vendor(data: dict) -> str:
    max_price: int = 0
    max_price_vendor: str
    counter: int = 0
    for item in data['data']['items'][0]['sellFor']:
        if item['price'] > max_price:
            max_price = item['price']
            max_price_vendor = item['vendor']['name']

        counter += 1

    return max_price_vendor

def sell_to_vendor(vendor: str) -> None:
    ...






def main() -> None:
    sleep(2)
    top_left_name: tuple[int, int] | None = find_icon("./Pictures/mag_glass.png")[2]
    bottom_right_name: tuple[int, int] | None = find_icon("./Pictures/exit.png")[1]
    gui.moveTo(top_left_name)
    sleep(1)
    gui.moveTo(bottom_right_name, duration=1)
    print(top_left_name[0])
    dimensions: tuple[int, int] | None = calculate_width_height(top_left_name, bottom_right_name)
    print(dimensions)
    print(read_item_name(top_left_name[0], top_left_name[1], dimensions[0], dimensions[1]))

    item_name: str = read_item_name(top_left_name[0], top_left_name[1], dimensions[0], dimensions[1]).strip()
    #item_name = "Balaclava"

    new_query = f"""
    {{
      items(name: "{item_name}", limit: 1) {{
        name
        sellFor {{
          vendor {{ name }}
          price
        }}
      }}
    }}
    """


    result = run_query(new_query)
    print(result)

    print(highest_vendor(result))




if  __name__ == "__main__":
    main()