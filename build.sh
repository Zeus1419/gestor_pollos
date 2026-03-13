#!/usr/bin/env bash
set -o errexit

cd bd_Smartgalpon_api

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate
