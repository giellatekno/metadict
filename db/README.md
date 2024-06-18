# Database-related things

The database schema is stored in `init/00_tables.sql`.

Initial data for the Giellatekno dictionaries is copied in to those
tables, from files `data_dictionaries.txt`, and `data_articles.txt`.

Per right now, they are baked into the image, and run during first startup,
but that may change in the future, as we use a podman volume to store the
data.

## Data change

I changed from `COPY ... FROM file` to `COPY ... FROM PROGRAM 'gzip -cd file'`
in the `init/` folder, so make sure to gzip the `init/data_*` files!
