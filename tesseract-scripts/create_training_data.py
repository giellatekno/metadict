
import os.path
from pathlib import Path
import subprocess
import shutil
import argparse
import random
import cv2

GT_DIR = Path("gt")

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Create training data"
    )
    parser.add_argument("folder", type=str, nargs=1, help="Folder with line images.")
    return parser.parse_args()

def check_dirs(name):

    if not GT_DIR.exists():
        GT_DIR.mkdir()
    
    if not Path.exists(GT_DIR / name):
        Path.mkdir(GT_DIR / name)
    
def main():

    args = parse_args()
    
    input_folder = Path(args.folder[0])
    name = input_folder.name

    if not input_folder.is_dir():
        print(f"Directory doesn't exist: {input_folder}")
        exit(1)
    
    check_dirs(name)

    while True:
        try:
            print("Type what is in the image:")
            
            imgs = list(input_folder.glob(f"{name}*.png"))
            random.shuffle(imgs)

            for line_img in imgs:
                if Path(GT_DIR / name / line_img.name).exists():
                    continue

                p = subprocess.Popen(["display", str(line_img)])

                input_text = input("#: ")

                p.kill()

                gt_file = Path(GT_DIR / name / f"{line_img.name[:-4]}.gt.txt")


                gt_file.write_text(input_text)
                shutil.copy(line_img, GT_DIR / name)

                print(f"Written to {str(gt_file)}")
                print()

                

        
        except KeyboardInterrupt:
            break




if __name__ == "__main__":
    raise SystemExit(main())