FROM docker.io/library/node:22-bookworm

RUN mkdir -p /app
COPY package.json /app
COPY package-lock.json /app
COPY build /app/build

WORKDIR /app

# Install dependencies in the built app
RUN npm ci --omit dev

CMD [ "node", "build" ]
