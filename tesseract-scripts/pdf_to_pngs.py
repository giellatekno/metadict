
import os.path
from pathlib import Path
import subprocess
import argparse

IMG_DIR = Path("imgs")

def parse_args():
    parser = argparse.ArgumentParser(
        prog="PDF to PNG",
        description="Turns a PDF file into PNGs."
    )
    parser.add_argument("filename", type=str, nargs=1, help="PDF file to be parsed")
    return parser.parse_args()

def check_dirs(name):

    if not IMG_DIR.exists():
        IMG_DIR.mkdir()
    
    if not Path.exists(IMG_DIR / name):
        Path.mkdir(IMG_DIR / name)
    
def main():

    args = parse_args()
    
    input_file = Path(args.filename[0])

    name = input_file.name[:-4]

    if not input_file.suffix == ".pdf":
        print(f"Not a PDF file: {input_file}")
        exit(1)

    if not input_file.exists():
        print(f"File doesn't exist: {input_file}")
        exit(1)

    check_dirs(name)

    print("Creating .png files")
    subprocess.run(["pdftoppm", input_file, IMG_DIR / name / name, "-png", "-gray", "-r", "600", "-progress"])


if __name__ == "__main__":
    raise SystemExit(main())