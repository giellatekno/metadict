import cv2
from pathlib import Path
import pytesseract
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Read images",
        description="Reads images with tesseract and outputs to a single textfile"
    )
    parser.add_argument("folder", type=str, help="Folder with png files to be read.")
    parser.add_argument("-l", "--lang", type=str, nargs="?", default="nor_sme", help="Language. Default: \"nor_sme\"")

    return parser.parse_args()


def preprocess_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # get grayscale image
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # thresholding
    #img = cv2.medianBlur(img ,5) # remove noise
    return img

def main():

    args = parse_args()
    
    input_folder = Path(args.folder)
    name = input_folder.name

    custom_config = f"-l {args.lang}"# --psm 6"
    print(custom_config)

    if not input_folder.is_dir():
        print(f"Directory doesn't exist: {input_folder}")
        exit(1)

    n = len(list(input_folder.glob(f"{name}*.png")))
    lines = []
    for i, image_file in enumerate(sorted(input_folder.glob(f"{name}*.png")), 1):    
        print(f"Reading image {i} of {n}\t", end="\r")
        image = cv2.imread(str(image_file))
        # image = preprocess_image(cv2.imread(str(image_file)))
        
        line_text = pytesseract.image_to_string(image, config=custom_config)
        lines.append(line_text)
    print()

    with open(f"{name}.txt", "w") as textfile:
        textfile.writelines(lines)


if __name__ == "__main__":
    raise SystemExit(main())