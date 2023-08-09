from pathlib import Path
from invoke import task

from mockup_automator import main

ROOT = Path(__file__).parent

@task
def mockup(c, name="Fletch"):
    main()

@task
def render(c, src, percentage=100):
    blends = [f for f in Path(src).iterdir() if f.suffix.lower() == ".blend"]
    render_script = ROOT / "render.py"
    for blend in blends:
        c.run(f"blender -b {blend} -P {render_script} -- {percentage}")
        # check that folder for blend exists
        # compress folder
