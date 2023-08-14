from pathlib import Path
from invoke import task
import subprocess

from mockup_automator import main
from img_utils import crop_resize, optimize_images_in_directory

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
def mockup(c, listings, mockups, fit=1900):
    listings = [x for x in Path(listings).iterdir() if x.is_dir()]
    mockups_path = Path(mockups)
    mockup_blends = _get_blends_in_folders(mockups_path)

    for listing in listings:
        art_file = _get_artfile(listing)
        for mockup in mockup_blends:
            subprocess.call(["blender", "-b", mockup, "-P", MOCKUP_SCRIPT, "--", art_file])


@task
def render(c, src, percentage=100):
    blends = [f for f in Path(src).iterdir() if f.suffix.lower() == ".blend"]
    render_script = ROOT / "render.py"
    for blend in blends:
        c.run(f"blender -b {blend} -P {render_script} -- {percentage}")
        src_path = blend.parent / blend.stem / f"{blend.stem}_src.png"
        for ratio, dims in RATIOS.items():
            w = int(dims[0] * percentage / 100)
            h = int(dims[1] * percentage / 100)
            out_path = src_path.with_stem(src_path.stem.replace("src", ratio)).with_suffix(".jpg")
            crop_resize(src_path, out_path, new_width=w, new_height=h)

@task
def optimize(c, target, fit: int=800):
    optimize_images_in_directory(Path(target), base_width=fit)