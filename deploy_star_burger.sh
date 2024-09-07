#!/bin/bash
set -e
git pull
revision=$(git rev-parse HEAD)
docker compose down
docker compose build
docker compose up
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "revision": "'$revision'", "rollbar_name": "'$ROLLBAR_NAME'", "local_username": "'$USER'", "comment": "Tuesday deployment", "status": "succeeded"}'
