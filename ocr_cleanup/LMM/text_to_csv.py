import argparse
import csv
import re
import subprocess

HFST_LOOKUP_BIN = "hfst-lookup"
FST_PATH = "/home/brede/gut/giellalt/lang-sma/src/fst/analyser-gt-desc.hfstol"


def get_saami_analyses(word_list):
    """Feeds a list of words into one hfst-lookup process and returns results."""
    if not word_list:
        return {}

    # Join words with newlines to send as a single block
    input_text = "\n".join(word_list)

    try:
        process = subprocess.Popen(
            [HFST_LOOKUP_BIN, "-q", "--time-cutoff=10", FST_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, _ = process.communicate(input=input_text)

        # HFST output: "word\tanalysis"
        results = {}
        for block in stdout.split("\n\n"):
            if not block.strip():
                continue
            parts = block.split("\t")
            if len(parts) >= 2:
                word, analysis = parts[0], parts[1]
                # If it doesn't contain '+?', it's a recognized Saami word
                results[word] = word not in ["=", "1"] and "+?" not in analysis
        return results
    except Exception as e:
        print(f"Error running HFST: {e}")
        return {}


def split_saami_entry(line):
    line = line.strip()
    if not line.strip():
        return None, None

    words = line.split()
    roman_pattern = r"^(I|II|III|IV|V|VI|VII|VIII)$"

    start_index = 0
    if words:
        # Matches things like "1", "*", "1*", "2.", etc.
        if re.match(r"^(\*|\d+\*?|\d+\.)$", words[0]):
            start_index = 1

    lemma_word_count = start_index

    for i in range(start_index, len(words)):
        word = words[i]
        # 1. STOP CONDITIONS: Colon, "1.", or "="
        if word in [":", "1.", "=", "se"]:
            break

        # Rule: Square brackets always count as a lemma word
        is_bracketed = word.startswith("[") and word.endswith("]")
        is_hyphenated = word.startswith("-") and word.endswith("-")

        is_comma = word == ","
        is_semicolon = word == ";"
        is_roman = re.match(roman_pattern, word)
        is_flt_marker = word == "flt."
        is_pred_marker = word == "pred."
        is_attr_marker = word == "attr."

        # 3. Contextual Look-back
        prev_was_comma = i > start_index and words[i - 1] == ","
        prev_was_semicolon = i > start_index and words[i - 1] == ";"

        # Did the previous word trigger an inclusion of the current word?
        prev_was_valid_flt = (
            i > start_index
            and words[i - 1] == "flt."
            and i > start_index + 1
            and words[i - 2] == ","
        )
        prev_was_valid_pred = (
            i > start_index
            and words[i - 1] == "pred."
            and i > start_index + 1
            and words[i - 2] == ";"
        )

        # --- Decision Logic ---
        if (
            i == start_index
            or is_bracketed
            or is_hyphenated
            or is_comma
            or is_semicolon
            or is_roman
            or is_flt_marker
            or is_pred_marker
            or is_attr_marker
            or prev_was_comma
            or prev_was_semicolon
            or prev_was_valid_flt
            or prev_was_valid_pred
        ):
            lemma_word_count = i + 1
        else:
            break

    lemma_part = " ".join(words[:lemma_word_count])
    definition_part = " ".join(words[lemma_word_count:])

    return lemma_part, definition_part


def main():
    parser = argparse.ArgumentParser(description="Optimized Batch Saami Splitter.")
    parser.add_argument("input", help="Source .txt file")
    parser.add_argument("output", help="Target .csv file")
    args = parser.parse_args()

    results_data = []
    words_to_check = []

    # Step 1: Initial Split
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            lemma, definition = split_saami_entry(line)

            # Identify the first word of the definition to check later
            first_def_word = ""
            def_words = definition.strip().split()
            if def_words:
                first_def_word = def_words[0].strip("*(),.;:")

            results_data.append(
                {"lemma": lemma, "definition": definition, "check_word": first_def_word}
            )
            if first_def_word:
                words_to_check.append(first_def_word)

    # Step 2: Batch Analysis (The Fast Part)
    print(f"Analyzing {len(words_to_check)} words with HFST...")
    saami_status_map = get_saami_analyses(list(set(words_to_check)))

    # Step 3: Write to CSV
    with open(args.output, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Lemma Section", "Definition Section", "Review Reason"])

        for item in results_data:
            reason = ""
            # Re-check logic for reasons
            if item["definition"].strip().startswith("("):
                reason = "Starts with Parenthesis"
            elif item["check_word"] and saami_status_map.get(item["check_word"]):
                reason = "Saami Word in Definition"

            writer.writerow([item["lemma"], item["definition"], reason])

    print(f"Done! {len(results_data)} lines processed.")


if __name__ == "__main__":
    main()
