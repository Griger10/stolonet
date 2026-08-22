FROM node:24-alpine

WORKDIR /app

RUN npm install -g serve

COPY frontend/package*.json frontend/package-lock.json /app/

RUN npm install

COPY frontend/ /app/

RUN npm run build && rm -f .env
