from pathlib import Path
import subprocess


ROOT = Path(__file__).parent
MOCKUP_DIR = ROOT / "mockups"
ART_DIR = ROOT / "art"
MOCKUP_SCRIPT = ROOT / "run_mockup.py"

IMG_EXTENSIONS = [".png", ".jpg"]


def main():
    if not ART_DIR.exists:
        return
    
    mockups = [p for p in MOCKUP_DIR.iterdir() if p.suffix.lower() == ".blend"]
    art_files = [a for a in ART_DIR.iterdir() if a.suffix.lower() in IMG_EXTENSIONS]

    print(mockups)
    print(art_files)
    
    for mockup in mockups:
        for art_file in art_files:
            print(f"working on {mockup} and {art_file}")
            subprocess.call(["blender", "-b", mockup, "-P", MOCKUP_SCRIPT, "--", art_file])

if __name__ == "__main__":
    main()