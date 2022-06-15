#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "./install.sh [--not-full]"
    exit 0
fi
python3 -m pip install -r requirements.txt
if [[ "$1" != "--not-full" ]]; then
    python3 -m pip install -r requirements_full.txt
fi
python3 -m spacy download en_core_web_sm
