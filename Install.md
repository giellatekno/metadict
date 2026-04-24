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
  * You will (for now) want the North Saami (sme), South Saami (sma), Inari Saami (smn), Finnish (fin) and Norwegian bokmål (nob) dictionaries. Gut can filter repos using regex, making it easy to clone the ones you want.
* Our own, closed-source dictionary files found at https://github.com/giellatekno/dictionaries-closed (requires access)

**important**: Fetch these using gut, so that your gut root directory is set correctly. This is referenced by scripts used later on.

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

```bash
cd preprocessing/
```
In the `preprocessing/` folder we turn the various dictionary files into SQL so that they can be added to the database later.
The script `gather_dicts.py` will try to fetch all the dictionary files and put them in the `dicts/` subfolder. 
The closed dictionaries in `gut_root/giellatekno/dictionaries-closed` will be symlinked and the GiellaLT dicts in 
`gut_root/giellalt/dict-*` will be merged into single files.

```bash
python3 gather_dicts.py
```
The script `create_db_data.py` reads the dicts in the `dicts/` folder and generates SQL files. These are placed in the folder `sql_files/`.
```bash
python3 create_db_data.py 
```

## Initialize and run the database
If everything works as intended, this might be as easy as running the following commands:
```bash
cd db/
just image
just run
```
However, you might run into problems. If `make image` does not work as intended, you might need to add sub-userIDs and sub-groupIDs to your user for podman to use:
```bash
sudo usermod --add-subuids 65536-75535 $(whoami)
sudo usermod --add-subgids 65536-75535 $(whoami)
podman system migrate
```
If `make run` complains that port 5432 is in use, postgres is probably running directly in your OS. As we want to run it in a container, you will need to stop the running instance.
Find the process id (PID) of postgres using:
```bash
suo lsof -i tcp:5432
```
which should return something like:
```text
COMMAND     PID     USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
postgres 340940 postgres    5u  IPv6 1053773      0t0  TCP localhost:postgresql (LISTEN)
postgres 340940 postgres    6u  IPv4 1053774      0t0  TCP localhost:postgresql (LISTEN)
```
You can then stop it using the PID you just found and then try running the containerized postgres again:
```bash
sudo kill 340940
just run
```
When you have the database up and running, keep it running and open a new terminal tab/window. Staying in the same `db/` directory, run the following command to import the dictionaries into the running database:

```bash
just fill-local
```

Database contents are not saved, so the command above must be run each time you start the database.

## Running the API
Move to the `api/` directory and run the following commands:
```bash
just build
just dev
```
Keep it running and open a new terminal tab/window.

## Running the frontend
Move to the `frontend/` directory and run the following commands:
```bash
pnpm install
just dev
```

Now the metadictionary should be up and running on `localhost:5173` and the api at `localhost:3000`, and you should be able to log in! Note that your GitHub user will need to be added to the list of people with access to closed dictionaries to see those in the search results.

# Recompiling and re-adding the dictionaries

To update the dictionaries in the database, create new sql files, then restart the database and re-fill it. 

To create new sql files simply retrace the steps of [Prepare the dictionaries](#prepare-the-dictionaries). 
Re-running `gather_dicts.py` is only necessary if the dictionary files have changed. (E.g. a new closed dictionary file had been added or you want to fetch the latest GiellaLT dicts)
```bash
cd preprocessing/
python3 gather_dicts.py # Otional
python3 create_db_data.py
```

Then start the database and fill it again.
```bash
cd db/
just run
just fill-local
```
