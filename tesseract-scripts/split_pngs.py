
import cv2
import os.path
import shutil
from pathlib import Path
import argparse

LINE_DIR = Path("lines")

def add_margins(padding, cnt, img):
    x, y, w, h = cv2.boundingRect(cnt)
    img_w, img_h = img.shape[:2]

    x, y, w, h = (x-padding, y-padding, w+(padding*2), h+(padding*2)) 

    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if w > img_w:
        w = img_w
    if h > img_h:
        h = img_h

    return x, y, w, h


def split_lines(image_path, image_name, name):

    # Step 1: Load the image
    image = cv2.imread(image_path)

    # Check if the image is None
    if image is None:
        raise ValueError("Invalid image file or path.")

    # Step 2: Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # selected a kernel with more width so that we want to connect lines
    kernel_size = (200, 10) # Change this until you get desired results
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # Step 3: Perform the closing operation: Dilate and then close
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # Desired result is when lines become a complete white block
    # bw_closedS = cv2.resize(bw_closed, (480, 720))
    # cv2.imshow('bw_closed', bw_closedS)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Find contours for each text line
    contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to select those whose width is at least 3 times its height
    # filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3])>=1.5]

    filtered_contours = [cnt for cnt in contours if 4000 > cv2.boundingRect(cnt)[2] > 100 
                                                and 150 > cv2.boundingRect(cnt)[3] > 20]

    # Sort contours based on y-coordinate
    sorted_contours = sorted(filtered_contours, key=lambda contour: (cv2.boundingRect(contour)[0] >= 1200, cv2.boundingRect(contour)[1]))


    for i, contour in enumerate(sorted_contours, 1):
        
        x, y, w ,h = add_margins(5, contour, image)

        # Recognize each line. Crop the image for each line. Save in "lines" folder.
        line_image = image[y:y + h, x:x+w]

        # cv2.imshow('line_image', line_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        cv2.imwrite(f'{LINE_DIR}/{name}/{image_name}-{"%02d" % i}.png', line_image)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Split PNGs",
        description="Splits page PNGs into line PNGs."
    )
    parser.add_argument("folder", type=str, nargs=1, help="Folder with png files to be read.")

    return parser.parse_args()

def check_dirs(name):
    
    if LINE_DIR.exists():
        if Path.exists(LINE_DIR / name):
            shutil.rmtree(LINE_DIR / name)
    else:
        LINE_DIR.mkdir()
    os.mkdir(LINE_DIR / name)

def main():

    args = parse_args()
    
    input_folder = Path(args.folder[0])

    name = input_folder.name

    if not input_folder.is_dir():
        print(f"Directory doesn't exist: {input_folder}")
        exit(1)

    check_dirs(name)

    n = len(list(input_folder.glob(f"{name}*.png")))

    print("Splitting lines in .png files")
    for i, image_file in enumerate(sorted(input_folder.glob(f"{name}*.png")), 1):
        print(f"Splitting page {i} of {n}\t", end="\r")
        split_lines(str(image_file), image_file.stem, name)
    print()

if __name__ == "__main__":
    raise SystemExit(main())