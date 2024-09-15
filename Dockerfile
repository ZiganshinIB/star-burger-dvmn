FROM node:16.16.0
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN apt-get update || : && apt-get install python3 python3-pip -y && rm -rf /var/lib/apt/lists/*
COPY ./ ./
EXPOSE 8000
