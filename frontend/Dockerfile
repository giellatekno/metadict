FROM docker.io/library/node:22-bookworm

RUN mkdir -p /app
COPY package.json /app
COPY build /app/build

WORKDIR /app
CMD [ "node", "build" ]
