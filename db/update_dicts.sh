#!/usr/bin/env bash
# Routine update of the metadict database with the newest NDS dicts.

set -euo pipefail

METADICT="$HOME/gut/giellatekno/metadict"

log() { printf '%s %s\n' "$(date -Is)" "$*"; }

log "Pulling latest GT dict repos..."
gut pull -o giellalt -r "dict-"

cd "$METADICT/preprocessing"

log "Gathering GT dicts..."
python3 gather_dicts.py --gt-only

log "Generating SQL files..."
python3 create_db_data.py --only 'gt*'

log "Updating GT dictionaries in the database..."
python3 "$METADICT/db/update_dictionaries.py" -c --only 'gt*' sql_files/

log "Done."
