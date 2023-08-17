"""works with etsy on chrome on a retina m2 macbook air."""

from pathlib import Path

import pyautogui
import webbrowser
import time

ROOT = Path(__file__).parent
REGIONS = ROOT / "screen_regions"

ADD_FILE = REGIONS / "add_file.png"
ADD_PHOTOS = REGIONS / "add_photos.png"
ADD_VIDEO = REGIONS / "add_video.png"
BACK_TO_LISTINGS = REGIONS / "back_to_listings.png"
COPY_LISTING = REGIONS / "copy_listing.png"
DELETE_FILE = REGIONS / "delete_file.png"
DELETE_PHOTO = REGIONS / "delete_photo.png"
FILE_UPLOADED = REGIONS / "file_uploaded.png"
LEAVE_PAGE = REGIONS / "leave_page.png"
PRIMARY_LISTING = REGIONS / "primary_listing.png"
PUBLISH_CONFIRM = REGIONS / "publish_confirm.png"
PUBLISH_COPY = REGIONS / "publish_copy.png"


def copy_listing_for_folder(edit_url: str, listing_dir: Path):
    """copy the given listing for the given listing folder."""
    # TODO: make sure listing exists
    # TODO: make sure zip exists
    # TODO: make sure selects exist

    webbrowser.open(edit_url)  # replace with your desired URL
    wait_for_region(COPY_LISTING)

    click_region(COPY_LISTING, delay=2)
    wait_for_region(BACK_TO_LISTINGS)

    scroll_to_find(ADD_VIDEO, increment=-5)

    # mouse to the primary listing to reveal the delete button
    pyautogui.moveTo(retina(pyautogui.locateCenterOnScreen(PRIMARY_LISTING.as_posix())))

    # delete existing photos
    for _ in range(10):
        click_region(DELETE_PHOTO, delay=.3)

    # add new photos
    click_region(ADD_PHOTOS, delay=1)
    pyautogui.hotkey("command", "shift", "g")
    time.sleep(.3)

    # enter the path to selects
    selects_path = listing_dir / "mockups" / "selects"
    pyautogui.write(selects_path.as_posix())
    time.sleep(.2)
    pyautogui.press("enter")
    time.sleep(.2)
    pyautogui.hotkey("command", "a")
    time.sleep(.2)
    pyautogui.press("enter")
    time.sleep(.2)

    wait_for_region(PRIMARY_LISTING)

    # delete existing digital file
    scroll_to_find(ADD_FILE, increment=-5)
    click_region(DELETE_FILE, delay=.2)
    
    # add new digitial file
    scroll_to_find(ADD_FILE)
    click_region(ADD_FILE, delay=1.2)
    pyautogui.hotkey("command", "shift", "g")
    time.sleep(.3)
    zip_path = listing_dir / (listing_dir.name + ".zip")
    pyautogui.write(zip_path.as_posix())
    time.sleep(.2)
    pyautogui.press("enter")
    time.sleep(.2)
    pyautogui.press("enter")
    time.sleep(2)

    wait_for_region(FILE_UPLOADED)

    click_region(PUBLISH_COPY, delay=.5)
    click_region(PUBLISH_CONFIRM, delay=.5)

    # if "leave page" can be found, click it
    leave_page = pyautogui.locateOnScreen(LEAVE_PAGE.as_posix())
    if leave_page:
        click_region(LEAVE_PAGE)


def wait_for_region(region: Path, timeout=20):
    time.sleep(.1)
    for _ in range(timeout * 10 - 1):
        if pyautogui.locateOnScreen(region.as_posix(), confidence=.9):
            return
        else:
            time.sleep(.1)
    raise TimeoutError(f"Region never appeared: {region.stem}")

def retina(point: pyautogui.Point) -> pyautogui.Point:
    if not point:
        return None
    return pyautogui.Point(point.x // 2, point.y // 2)

def click_region(region: Path, delay=2):
    reg = pyautogui.locateCenterOnScreen(region.as_posix(), confidence=0.9)
    reg = retina(reg)
    if reg:
        pyautogui.click(reg)
        time.sleep(delay)
    else:
        raise ValueError(f"Region not found: {region.stem}")

def scroll_to_find(region: Path, increment=-2):
    for _ in range(20):
        reg = pyautogui.locateOnScreen(region.as_posix(), confidence=.8)
        if reg:
            return
        else:
            pyautogui.scroll(increment)
    raise ValueError(f"Couldn't scroll to find region {region.stem}")
