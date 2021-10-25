#!/bin/bash

export FLASK_APP=/home/temp/beer-horoscope/src/rest_api/main.py
export TRAINED_MODELS_DIR=/mnt/storage/out/

mkdir -p /mnt/storage/out
virtualenv /home/temp/venv
source /home/temp/venv/bin/activate
pip install -r /home/temp/beer-horoscope/src/rest_api/requirements.txt
flask run --host=0.0.0.0