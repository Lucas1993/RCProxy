#!/bin/sh

clear
python3 proxy.py -i 'localhost' -p 8080 -w whitelist -d blocked
