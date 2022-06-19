#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "./install.sh [--no-transformers] [--no-chatterbot]"
    exit 0
fi
python3 -m pip install -r requirements.txt
if [[ $(echo "$@" | grep -e "--no-transformers") == "" ]]; then
    python3 -m pip install -r ./requirements_transformers.txt
fi
if [[ $(echo "$@" | grep -e "--no-chatterbot") == "" ]]; then
    python3 -m pip install -r ./requirements_chatterbot.txt
    python3 -m spacy download en_core_web_sm
fi
