import os.path
import sys
import shutil
from pathlib import Path


def get_gut_root():
    app_toml_path = os.path.expanduser("~/.config/gut/app.toml")
    with open(app_toml_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            try:
                k, v = line.split("=", maxsplit=1)
            except IndexError:
                continue
            k = k.strip()
            v = v.strip()
            if k != "root":
                continue

            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]

            return v


try:
    # if GUTHOME (the gut directory) environment variable is set...
    GUTROOT = get_gut_root()
    script_directory = os.path.join(GUTROOT, "giellalt", "giella-core", "dicts", "scripts")
    # ...and the scripts directory have been moved to git ...
    if not os.path.isdir(script_directory):
        raise KeyError
finally:
    sys.path.append(script_directory)
    from merge_giella_dicts import merge_giella_dicts


def main():
    gut_root = get_gut_root()
    p = Path(gut_root) / "giellalt"

    shutil.rmtree("merged/", ignore_errors=True)
    Path("merged/").mkdir(parents=True, exist_ok=True)

    for i, directory in enumerate(p.glob("dict-*"), start=1):
        # strip away the "dict-" prefix
        name = directory.name[5:]
        if len(name) != 7:
            # skip ...-x-private  and other such dicts
            continue
        l1, l2 = name.split("-")

        output_filename = f"merged/gt-{l1}-{l2}.xml"
        try:
            n_entries = merge_giella_dicts(directory / "src", output_filename)
        except FileNotFoundError:
            print(f"no src files in dict {l1}-{l2}, skipping")
        except NotADirectoryError:
            print(f"no src directory in dict {l1}-{l2}, skipping")


if __name__ == "__main__":
    raise SystemExit(main())
