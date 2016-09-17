#!/bin/bash

DIR=$( dirname "$0" )
cd "${DIR}"
virtualenv -p python3 .
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
