.PHONY: help
help:
	@echo "Available commands:"
	@echo "dev - run development build locally"
	@echo "build - just cargo build --release"
	@echo "image - use podman to build the image"
	@echo "runlocal - run the built image, using local settings"
	@echo "stop - stop the locally running container"
	@echo "export - save podman image as metadict-api.tar.gz"
	@echo "push-labacr - push image to gtlabcontainerregistry.azurecr.io"
	@echo "push-gtweb - upload metadict-api.tar.gz to gtweb"
	@echo "bap - 'build and push', does build; image; push-gtweb;"

.PHONY: dev
dev:
	FRONTEND=http://localhost:5173 RUST_BACKTRACE=1 PG__HOST=localhost PG__PORT=1400 PG__PASSWORD=mysecretpassword systemfd --no-pid -s http::3000 -- cargo watch -x run
#	FRONTEND=http://localhost:5173 RUST_BACKTRACE=1 PG__HOST=localhost PG__PORT=5432 PG__PASSWORD=mysecretpassword systemfd --no-pid -s http::3000 -- cargo watch -x run

.PHONY: run-release
run-release:
	RUST_BACKTRACE=1 PG__PASSWORD=mysecretpassword systemfd --no-pid -s http::3000 -- cargo run --release

.PHONY: build
build:
	cargo build --target-dir target/ --release

.PHONY: build-dev
build-dev:
	cargo build --target-dir target/

.PHONY: image
image: target/release/metadict-api
	podman build -t metadict-api -f Dockerfile .

.PHONY: image-dev
image-dev:
	podman build -t metadict-api -f Dockerfile.dev .

.PHONY: runlocal
runlocal:
	podman run \
		--name metadict-api \
		--detach \
		--stop-signal=SIGINT \
		--rm \
		-p 8081:3000 \
		metadict-api

.PHONY: stop
stop:
	podman stop metadict-api

.PHONY: push-labacr
push-labacr:
	podman tag metadict-api gtlabcontainerregistry.azurecr.io/metadict-api
	podman push gtlabcontainerregistry.azurecr.io/metadict-api

# bap = "build and push"
# this is make build, make image, and make push-labacr
# ... I just do it so often
.PHONY: bap
bap:
	cargo build --target-dir target/ --release
	podman build -t metadict-api -f Dockerfile .
	podman tag metadict-api gtlabcontainerregistry.azurecr.io/metadict-api
	podman push gtlabcontainerregistry.azurecr.io/metadict-api

