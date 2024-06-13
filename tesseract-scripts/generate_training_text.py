"""
Short script for turning a wodfrequency list into training_text for tesseract. 
"""

import random

START_PUNC = list("([{«“")
END_PUNC = list(".,:;])}”»’'?!%´\"-_")


def main():

    with open("sme_wf.freq", "r") as f:
        lines = [l.strip() for l in f.readlines()]

    words = []

    for line in lines:
        freq = int(line.split()[0])
        try:
            word = line.split()[1].strip()
        except Exception:
            continue
        for _ in range(freq):
            words.append(word)

    random.shuffle(words)

    output_lines = []
    line = ""
    for word in words:
        word = word.strip()
        if len(word) > 81:
            continue

        if len(line) + len(word) > 81:
            output_lines.append(line + "\n")
            line = ""
        
        
        if word in END_PUNC:
            if line and line.rstrip()[-1:] not in END_PUNC:
                # print(line)
                line = line.rstrip() + word + " "
        elif word in START_PUNC:
            line = line + word
        else:
            if random.randint(0,50) == 0:
                word = word.upper()
            line = line + word + " "
    

    with open("sme.training_text", "w") as output_f:
        output_f.writelines(output_lines)

        


if __name__ == "__main__":
    main()