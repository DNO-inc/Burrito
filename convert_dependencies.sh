#!/bin/bash

cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add
