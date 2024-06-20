.PHONY: help
help:
	@echo "Available commands:"
	@echo "help - show this help"
	@echo "dev - run development build locally"
	@echo "build-gtweb - build with base=/metadict, for gtweb"
	@echo "image - use podman to build the image"
	@echo "runlocal - run the built image, using local settings"
	@echo "export - save podman image as metadict-front.tar.gz"
	@echo "push-gtweb - upload metadict-front.tar.gz to gtweb"

.PHONY: dev
dev:
	#CMD := $(shell which pnpm || which npm)
	PUBLIC_API_ENDPOINT=http://localhost:3000 pnpm run dev

.PHONY: build-gtweb
build-gtweb:
	SK_BASE=/metadict pnpm run build

.PHONY: image
image:
	podman build -t metadict-front -f Dockerfile

.PHONY: run-image
run-image:
	podman run --rm -p 3000:3000 --name metadict-front metadict-front

.PHONY: export
export:
	podman save -o metadict-front.tar metadict-front
	gzip -f metadict-front.tar

.PHONY: push-gtweb
push-gtweb:
	scp metadict-front.tar.gz gtweb.uit.no:/home/anders/metadict-front.tar.gz
