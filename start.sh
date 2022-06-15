#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "./start.sh"
    echo "first argument is forwarded to ./install.sh"
    exit 0
fi
./install.sh "$1"
python3 ./main.py
