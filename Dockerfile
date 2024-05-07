FROM node:16.16.0

WORKDIR /usr/src/app
RUN apt-get update || : && apt-get install python3 python3-pip -y

COPY package*.json ./

RUN npm ci --dev
EXPOSE 3000
COPY ./bundles-src ./bundles-src

