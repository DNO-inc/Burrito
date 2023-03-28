#!/bin/bash

pip freeze > requirements.txt

cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add
