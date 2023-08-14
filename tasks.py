from pathlib import Path
from invoke import task

from mockup_automator import main
from img_utils import resize, optimize_images_in_directory

ROOT = Path(__file__).parent

RATIOS = {
    "2x3": (7275, 10875),
    "3x4": (5475, 7275),
    "4x5": (4875, 6075),
    "11x14": (3375, 4275),
    "Asizes": (7091, 10008),
}

@task
def mockup(c, name="Fletch"):
    main()

@task
def render(c, src, percentage=100):
    blends = [f for f in Path(src).iterdir() if f.suffix.lower() == ".blend"]
    render_script = ROOT / "render.py"
    for blend in blends:
        c.run(f"blender -b {blend} -P {render_script} -- {percentage}")
        render_src = blend.parent / blend.stem / f"{blend.stem}_src.png"
        for ratio, dims in RATIOS.items():
            w = int(dims[0] * percentage / 100)
            h = int(dims[1] * percentage / 100)
            resize(render_src, render_src.with_stem(render_src.stem.replace("src", ratio)), new_width=w, new_height=h)

@task
def optimize(c, target, fit: int=800):
    optimize_images_in_directory(Path(target), base_width=fit)