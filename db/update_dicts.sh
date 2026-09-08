#!/usr/bin/env bash
# Routine update of the metadict database with the newest NDS dicts.

USER_NAME=services
METADICT="$HOME/gut/giellatekno/metadict"

runuser -l "$USER_NAME" -c "
set -euo pipefail
gut pull -o giellalt -r 'dict-'
cd '$METADICT/preprocessing'
python3 gather_dicts.py --gt-only
python3 create_db_data.py --only 'gt*'
"

python3 "$METADICT/db/update_dictionaries.py" -c --only 'gt*' sql_files/

