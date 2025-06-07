from time import sleep
import pyautogui as gui
import pytesseract
import requests
import library

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def main() -> None:
    current_slot: tuple[float, float] = library.cursor_auf_anfang()
    for i in range(2):
        gui.moveTo(*current_slot)
        for j in range(10):
            sleep(2)
            gui.moveTo(*current_slot)
            sleep(0.5)
            gui.click()
            sleep(0.1)
            gui.click()
            try:
                top_left_name: tuple[int, int] | None = library.find_icon("./Pictures/mag_glass.png")[2]
                bottom_right_name: tuple[int, int] | None = library.find_icon("./Pictures/exit.png")[1]
            except:
                print("------EXCEPT-------")
                if i < 9:
                    print(current_slot)
                    current_slot = (current_slot[0] + 63, current_slot[1])

                    print(current_slot)
                    continue

                print("-----BREAK---------")
                break
            gui.moveTo(top_left_name)
            sleep(1)
            gui.moveTo(bottom_right_name, duration=0.2)
            print(top_left_name[0])
            dimensions: tuple[int, int] | None = library.calculate_width_height(top_left_name, bottom_right_name)
            print(dimensions)
            print(library.read_item_name(top_left_name[0], top_left_name[1], dimensions[0], dimensions[1]))

            item_name: str = library.read_item_name(top_left_name[0], top_left_name[1], dimensions[0], dimensions[1]).strip()
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


            result = library.run_query(new_query)
            print(result)


            print(library.highest_vendor(result))
            library.sell_to_vendor(library.highest_vendor(result))
            # enter amount coordinates
            print("Esc druecken")
            sleep(5)
            print(gui.position())

            if i < 9:
                current_slot = (current_slot[0] + 63, current_slot[1])
                continue

            print("-----BREAK---------")
            break

        current_slot = (library.cursor_auf_anfang()[0], current_slot[1] + 63)




if  __name__ == "__main__":
    main()