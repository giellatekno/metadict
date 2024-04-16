
# build the podman image
.PHONY: image
image:
	podman build -f Dockerfile -t metadict-db


# recreate the database (in host /var/lib/postgresql/data)
.PHONY: recreate
recreate:
	rm -rf /var/lib/postgresql/data/
	mkdir -p /var/lib/postgresql/data
	chmod a+w /var/lib/postgresql/data
	#chmod a+w /var/lib/postgresql/data/pgdata

# Run the podman image to spawn the database
.PHONY: run
run:
	podman run --rm --name metadict-db -it \
		-e POSTGRES_PASSWORD=mysecretpassword \
		-e PGDATA=/var/lib/postgresql/data/pgdata \
		-v /var/lib/postgresql/data:/var/lib/postgresql/data \
		metadict-db

# Stop the running container
.PHONY: stop
stop:
	podman stop metadict-db

# Get a psql shell to the database
.PHONY: psql
psql:
	podman exec -it metadict-db psql -U postgres

