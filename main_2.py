import library
import pyautogui as gui
from time import sleep

'''
------Goal--------
- first item gets selected
- filter by item
- get price of second highest item
- put into enter amount
- place offer
- go to second item
- repeat
'''

def main() -> None:
    sleep(1)
    current_slot: tuple[int, int] | None = library.find_icon("./Pictures/flea_market_start_point.png")[3]
    for j in range(3):
        for i in range(10):
            gui.moveTo(current_slot[0] + 20, current_slot[1])

            try:
                library.sell_item()
            except:
                current_slot = (current_slot[0] + 63, current_slot[1])
                continue

            print("Sold the item")
            sleep(5)

            print(gui.position())
            while True:
                if library.check_add_offer():
                    break
                sleep(10)

            gui.click()

            print("Checkpoint")


            current_slot = (current_slot[0] + 63, current_slot[1])

        current_slot = (current_slot[0] - 10 * 63, current_slot[1] + 63)








if  __name__ == "__main__":

    main()