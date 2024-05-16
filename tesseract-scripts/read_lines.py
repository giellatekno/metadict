import cv2
import os.path
from pathlib import Path
import pytesseract
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Read lines",
        description="Reads lines with tesseract and outputs to a single textfile"
    )
    parser.add_argument("folder", type=str, nargs=1, help="Folder with png files to be read.")

    return parser.parse_args()


def main():

    args = parse_args()
    
    input_folder = Path(args.folder[0])

    name = input_folder.name

    if os.path.exists(f"{name}.txt"):
        os.remove(f"{name}.txt")


    if not input_folder.is_dir():
        print(f"Directory doesn't exist: {input_folder}")
        exit(1)

    textfile = open(f"{name}.txt", "a")

    n = len(list(input_folder.glob(f"{name}*.png")))

    for i, image_file in enumerate(sorted(input_folder.glob(f"{name}*.png")), 1):    
        print(f"Reading line {i} of {n}\t", end="\r")
        image = cv2.imread(str(image_file))
        line_text = pytesseract.image_to_string(image, lang="sme_test")
        textfile.writelines([line_text])
    print()
    textfile.close()

if __name__ == "__main__":
    raise SystemExit(main())