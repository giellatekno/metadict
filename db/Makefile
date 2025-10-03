.PHONY: help
help:
	@echo "Available commands:"
	@echo "image - make podman image"
	@echo "run - run image locally, data will be stored in volume called metadict-data"
	@echo "shell - run bash inside the running container"
	@echo "psql - run psql inside the running container"
	@echo "export - save podman image as metadict-db.tar.gz"
	@echo "push-gtweb - upload metadict-db.tar.gz to gtweb"
	@echo "push-labacr - push image to gtlabcontainerregistry.azurecr.io"

.PHONY: image
image:
	podman build --no-cache -f Dockerfile -t metadict-db

# recreate the database (in host /var/lib/postgresql/data)
.PHONY: recreate
recreate:
	@echo "Notice: this isn't needed anymore, as we use volumes instead of storing data directly on host"
	@echo "Run podman volume rm metadict-data to remove the data (after first stopping the db!)"
	rm -rf /var/lib/postgresql/data/
	mkdir -p /var/lib/postgresql/data
	chmod a+w /var/lib/postgresql/data
	#chmod a+w /var/lib/postgresql/data/pgdata

.PHONY: run
run:
	podman run --rm -it \
		--name metadict-db \
		-p 5432:5432 \
		--mount type=volume,source=metadict-data,target=/var/lib/postgresql/data \
		metadict-db

.PHONY: shell
shell:
	podman exec -it metadict-db /bin/bash

.PHONY: stop
stop:
	podman stop metadict-db

.PHONY: psql
psql:
	podman exec -it metadict-db psql -U postgres

.PHONY: push-labacr
push-labacr:
	podman tag metadict-db gtlabcontainerregistry.azurecr.io/metadict-db
	podman push gtlabcontainerregistry.azurecr.io/metadict-db
