#!/bin/bash

set -e
set -x

rm -rf .venv
python3.7 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

deactivate