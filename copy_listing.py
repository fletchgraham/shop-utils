from pathlib import Path

import pyautogui
import webbrowser
import time

import pyscreeze
import PIL

ROOT = Path(__file__).parent
REGIONS = ROOT / "screen_regions"

ADD_FILE = REGIONS / "add_file.png"
ADD_PHOTOS = REGIONS / "add_photos.png"
COPY_LISTING = REGIONS / "copy_listing.png"
DELETE_FILE = REGIONS / "delete_file.png"
DELETE_PHOTO = REGIONS / "delete_photo.png"
LEAVE_PAGE = REGIONS / "leave_page.png"
PRIMARY_LISTING = REGIONS / "primary_listing.png"
PUBLISH_CONFIRM = REGIONS / "publish_confirm.png"
PUBLISH_COPY = REGIONS / "publish_copy.png"

# ask user for url to edit listing page
# open browser to edit listing
url = input("URL: ")
webbrowser.open(url)  # replace with your desired URL
time.sleep(3)  # wait for the web page to load

# click "copy"

def retina(point: pyautogui.Point) -> pyautogui.Point:
    return pyautogui.Point(point.x // 2, point.y // 2)

def click_region(region: Path, delay=2):
    reg = pyautogui.locateCenterOnScreen(region.as_posix(), confidence=0.8)
    reg = retina(reg)
    if reg:
        print(reg)
        pyautogui.click(reg)
        time.sleep(2)
    else:
        raise ValueError(f"Region not found: {region.stem}")
    
click_region(COPY_LISTING)

# scroll down till photos are visible
# mouse to "primary"
# mouse to trash can
# click ten times with small delay
# mouse to add photos and click
# cmd shift G
# enter the path to selects
# cmd a
# enter
# wait a bit
# scroll down to digital files
# mouse to x button and click
# click add file
# cmd shift g
# enter path to zip
# enter
# if "leave page" can be found, click it
# wait a bit

# Step 1: Open a web page

# Step 2: Locate and click the first button based on the screenshot
# first_button = pyautogui.locateOnScreen('first_button.png', confidence=0.8)
# if first_button:
#     pyautogui.click(pyautogui.center(first_button))
#     time.sleep(2)  # delay after clicking the first button
# else:
#     print("First button not found!")

# # Step 3: Locate and click the second button based on the screenshot
# second_button = pyautogui.locateOnScreen('second_button.png', confidence=0.8)
# if second_button:
#     pyautogui.click(pyautogui.center(second_button))
#     time.sleep(2)  # delay after clicking the second button
# else:
#     print("Second button not found!")

# # Step 4: File Upload - Usually a dialog will open when you click an 'Upload' button
# # To handle the file dialog, you need to type the file path and then press 'Enter'
# file_path = "/path/to/your/file.txt"
# pyautogui.write(file_path)
# time.sleep(1)  # small delay to ensure the path is fully typed
# pyautogui.press('enter')

# # Note: Make sure 'first_button.png' and 'second_button.png' are in the same directory as your script 
# # or provide the full path to the images.
# # The `confidence` argument allows for a little flexibility in the image match. 
# # This is especially useful if the screenshot isn't pixel-perfect.
