#!/bin/bash
set -e
git pull
revision=$(git rev-parse HEAD)
/opt/star-burger-dvmn/.venv/bin/pip install -r requirements.txt
/opt/star-burger-dvmn/.venv/bin/python manage.py migrate
/opt/star-burger-dvmn/.venv/bin/python manage.py collectstatic --no-input
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
systemctl disable star-burger
systemctl reload star-burger
systemctl enable star-burger
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "revision": "'$revision'", "rollbar_name": "'$ROLLBAR_NAME'", "local_username": "'$USER'", "comment": "Tuesday deployment", "status": "succeeded"}'
