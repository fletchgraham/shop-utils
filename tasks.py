from pathlib import Path
from invoke import task
import subprocess
from zipfile import ZipFile
import random

from mockup_automator import main
from img_utils import crop_resize, optimize_images_in_directory
from copy_listing import copy_listing_for_folder

ROOT = Path(__file__).parent
MOCKUP_SCRIPT = ROOT / "run_mockup.py"

RATIOS = {
    "2x3": (7275, 10875),
    "3x4": (5475, 7275),
    "4x5": (4875, 6075),
    "11x14": (3375, 4275),
    "Asizes": (7091, 10008),
}

def _get_blends_in_folders(target: Path) -> list[Path]:
    blends = []
    folders = [f for f in target.iterdir() if f.is_dir()]
    for f in folders:
        blends.append([file for file in f.iterdir() if file.suffix == ".blend"][0])
    return blends

def _get_artfile(listing_dir: Path) -> Path:
    jpgs = [f for f in listing_dir.iterdir() if f.suffix == ".jpg"]
    for j in jpgs:
        if j.stem.split("_")[-1] == "3x4":
            return j


@task
def mockup(c, listings, mockups, fit=1800):
    listings = [x for x in Path(listings).iterdir() if x.is_dir()]
    mockups_path = Path(mockups)
    mockup_blends = _get_blends_in_folders(mockups_path)

    for listing in listings:
        art_file = _get_artfile(listing)
        for mockup in mockup_blends:
            subprocess.call(["blender", "-b", mockup, "-P", MOCKUP_SCRIPT, "--", art_file])
        optimize_images_in_directory(listing / "mockups", base_width=fit)


@task
def render(c, src, percentage=100):
    blends = [f for f in Path(src).iterdir() if f.suffix.lower() == ".blend"]
    render_script = ROOT / "render.py"
    for blend in blends:
        c.run(f"blender -b {blend} -P {render_script} -- {percentage}")
        src_path = blend.parent / blend.stem / f"{blend.stem}_src.png"
        to_zip = []
        for ratio, dims in RATIOS.items():
            w = int(dims[0] * percentage / 100)
            h = int(dims[1] * percentage / 100)
            out_path = src_path.with_stem(src_path.stem.replace("src", ratio)).with_suffix(".jpg")
            crop_resize(src_path, out_path, new_width=w, new_height=h)
            to_zip.append(out_path)
        
        zip_path = src_path.with_stem("_".join(src_path.stem.split("_")[:-1])).with_suffix(".zip")
        with ZipFile(zip_path, "w") as zipf:
            for f in to_zip:
                zipf.write(f, arcname=f.name)

@task
def optimize(c, target, fit: int=800):
    optimize_images_in_directory(Path(target), base_width=fit)


@task
def choose_ten_mockups(c, listings):
    listings = [x for x in Path(listings).iterdir() if x.is_dir()]
    for listing in listings:
        print(f"working on {listing}")
        mockup_dir = listing / "mockups"
        choice_dir = mockup_dir / "selects"
        choice_dir.mkdir(exist_ok=True)
        if len(list(choice_dir.iterdir())) == 10:
            continue
        lo_mockups = [f for f in mockup_dir.iterdir() if f.suffix == ".jpg" and f.stem.split("_")[0] == "lo"]
        choices = random.sample(lo_mockups, 10)
        for choice in choices:
            choice.rename(choice_dir / choice.name)


@task
def copy_listing(c, url: str, listings: str):
    listings = [x for x in Path(listings).iterdir() if x.is_dir()]
    for listing in listings:
        copy_listing_for_folder(url, Path(listing))
