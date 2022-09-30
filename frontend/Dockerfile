FROM node:16.16-alpine3.15 as builder
WORKDIR /frontend
COPY package.json /frontend/package.json
RUN npm install --only=production
EXPOSE 3000
COPY . /frontend