# Installing and running the Metadictionary

## Prerequisites

* Python version 3.10 or newer. We recommend 3.12.
* PostgreSQL
* pnpm (see https://pnpm.io/installation for help)
* node version 16 or newer
* Rust including the following packages:
  * systemfd
  * cargo watch
* [gut](https://github.com/divvun/gut)

## Fetch dictionary repositories

The Metadictionary uses dictionaries from two different sources:
* Publicly available dictionaries from GiellaLT found at https://github.com/giellalt/?q=dict
  * **important**: Fetch these using gut, so that your gut root directory is set correctly. This is referenced by scripts used later on.
  * You will (for now) want the North Saami (sme), Finnish (fin) and Norwegian bokmål (nob) dictionaries. Gut can filter repos using regex, making it easy to clone the ones you want.
* Our own, closed-source dictionary files found at https://github.com/giellatekno/dictionaries-closed (requires access)

## Set up secrets and keys

Three configuration files need to be created in the `api/` directory for authentication:
* `gh_app.toml`
* `giellatekno-metadictionary.<yyyy-mm-dd>.private-key.pem`
* `jwt_secret.txt`

### gh_app.toml

Open [the Metadictionary GitHub App settings](https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary) and create a client secret.

Create the file `gh_app.toml` with the following content, using the secret created above:
```text
client_id = "Iv1.f208b6793cca35ec"
client_secret = "GH APP CLIENT SECRET HERE"
```

### giellatekno-metadictionary.<yyyy-mm-dd>.private-key.pem
Open [the Metadictionary GitHub App settings](https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary) and create and download a private key. 
Move the key to the `api/` directory. Then edit the constant IAT_PK_PATH in `api/src/iat.rs` to match your key's name.

### jwt_secret.txt

Create this file by running the following command:
```bash
openssl rand --hex 32 > jwt_secret.txt
```

## Prepare the dictionaries

First create a virtual environment and install the `pandas` module
```bash
cd preprocessing/
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pandas
```
Then generate merged dictionary files from the GiellaLT dictionaries:
```bash
python3 generate_merged_gt_dicts.py -l sme nob fin
```
And lastly create the sql files needed for adding all the dictionaries to the dictionary database later:
```bash
python3 create_db_data.py 
```
## Initialize the database
If everything works as intended, this might be as easy as running the following commands:
```bash
cd db/
make image
make run
```
However, you might run into problems. If `make image` does not work as intended, you might need to add sub-userIDs and sub-groupIDs to your user for podman to use:
```bash
sudo usermod --add-subuids 65536-75535 $(whoami)
sudo usermod --add-subgids 65536-75535 $(whoami)
podman system migrate
```
If `make run` complains that port 5432 is in use, postgres is probably running directly in your OS. As we want to run it in a container, you will need to stop the running instance.
Find the process id (PID) of postgres using
```bash
sudo lsof -i tcp:5432
```
which should return something like
```text
COMMAND     PID     USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
postgres 340940 postgres    5u  IPv6 1053773      0t0  TCP localhost:postgresql (LISTEN)
postgres 340940 postgres    6u  IPv4 1053774      0t0  TCP localhost:postgresql (LISTEN)
```
You can then stop it using the PID you just found and then try running the containerized postgres again:
```bash
sudo kill 340940
make run
```
When you have the database up and running, keep it running and open a new terminal tab/window. Staying in the same `db/` directory, run the following command to import the dictionaries into the running database:
```bash
python3 insert_dictionaries.py ../preprocessing/sql_files --container
```

## Running the api
Move to the `api` directory and run the following commands:
```bash
make build
make dev
```
Keep it running and open a new terminal tab/window

## Running the frontend
Move to the `frontend/` directory and run the following command:
```bash
make dev
```

Now the metadictionary should be up and running on localhost, and you should be able to log in! Note that your GitHub user will need to be added to the list of people with access to closed dictionaries to see those in the search results.

# Recompiling and re-adding the dictionaries

To update the dictionaries in the database

Re-add dicts:

podman volume rm metadict-data
cd db/
make image
make run
keep running

python3 insert_dictionaries.py ../preprocessing/sql_files --container