#!/bin/bash

pip freeze > requirements.txt

#cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add

venv_libs=$(cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1)
poetry_libs=$(poetry show | sed 's/|/ /' | awk '{print $1}')

function install_in_poetry {
    for venv_l in $venv_libs; do
        is_exists=0

        for poetry_l in $poetry_libs; do
            if [ $venv_l == $poetry_l ]; then
                is_exists=1
            fi
        done

        if [ $is_exists = 0 ]; then
            echo "Install $venv_l"
            poetry add $venv_l
        fi

    done
}

install_in_poetry
