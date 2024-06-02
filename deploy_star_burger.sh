#!/bin/bash
set -e
git pull
/opt/star-burger-dvmn/.venv/bin/pip install -r requirements.txt
/opt/star-burger-dvmn/.venv/bin/python manage.py migrate
/opt/star-burger-dvmn/.venv/bin/python manage.py collectstatic --no-input
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
systemctl disable star-burger
systemctl reload star-burger
systemctl enable star-burger
