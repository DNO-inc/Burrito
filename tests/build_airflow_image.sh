#!/bin/bash

RED_COLOR="\e[31m"
RESET_COLOR="\e[0m"

docker build -t burrito-airflow-test -f burrito/airflow/Dockerfile .

if [[ $? != 0 ]]; then
    echo -e "\n\t${RED_COLOR}Failed to build image${RESET_COLOR}"
    exit
fi

docker tag burrito-airflow-test localhost:5000/burrito-airflow-test

docker push localhost:5000/burrito-airflow-test

if [[ $? != 0 ]]; then
    echo -e "\n\t${RED_COLOR}Failed to push image${RESET_COLOR}"
    exit
fi
