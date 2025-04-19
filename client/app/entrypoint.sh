#!/bin/bash

# Lance snif
python retrieve_requests.py &

# Lance le main
python main.py
