#!/bin/bash
set -e
python3 manage.py migrate
python3 manage.py collectstatic --no-input
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
python3 ./manage.py runserver 0.0.0.0:8000
