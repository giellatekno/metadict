# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "python-docx>=1.2.0",
# ]
# ///
import argparse
from pathlib import Path

from docx import Document


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=str, help="Docx file to be converted.")
    return parser.parse_args()


def convert_to_txt(input_path, output_path):
    doc = Document(input_path)
    full_text = []

    for para in doc.paragraphs:
        para_parts = []
        for run in para.runs:
            text = run.text

            # Apply italic (cursive) markers
            if run.italic:
                text = f"%>{text}<%"

            # Apply bold markers
            if run.bold:
                text = f"$>{text}<$"

            para_parts.append(text)

        # Join runs together and add to the list of paragraphs
        full_text.append("".join(para_parts))

    with open(output_path, "w") as f:
        f.write("\n".join(full_text))


def main():
    args = parse_args()

    input_file = Path(args.file)
    output_file = Path(input_file.stem + ".txt")

    convert_to_txt(input_file, output_file)


if __name__ == "__main__":
    raise SystemExit(main())
