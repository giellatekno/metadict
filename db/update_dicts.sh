#!/usr/bin/env bash
# Routine update of the metadict database with the newest NDS dicts.

set -euo pipefail

METADICT="$HOME/gut/giellatekno/metadict"

gut pull -o giellalt
cd "$METADICT/preprocessing"
python3 gather_dicts.py --gt-only
python3 create_db_data.py --only 'gt*'
python3 "$METADICT/db/update_dictionaries.py" -c --only 'gt*' sql_files/
