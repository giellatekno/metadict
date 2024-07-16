FROM debian:sid-slim

# the api needs certificates to be able to use ssl, which it needs to
# contact the facebook api
RUN set -eux && \
    apt update && \
    apt install -y ca-certificates

RUN mkdir -p /app

# have to have a specific image for each host, which is a bit sad, this should
# be dynamic, in a way
#COPY config.gtweb.toml /app/config.toml
COPY config.toml /app/config.toml

COPY gh_app.toml jwt_secret.txt giellatekno-metadictionary.2024-04-26.private-key.pem /app/
COPY target/release/metadict-api /usr/local/bin/metadict-api
ENV PG__PASSWORD=mysecretpassword
WORKDIR /app
CMD [ "metadict-api" ]
