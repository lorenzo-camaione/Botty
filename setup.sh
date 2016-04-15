#!/usr/bin/env bash

echo -e '\nInstalling Virtual Environment Tool'
sudo apt-get install python-virtualenv python3-dev libssl-dev swig libpq-dev

echo -e '\nCreating Virtual Environment'
virtualenv --python=python3.4 venv

echo -e '\nInstalling Requirements'
./venv/bin/pip3 install -r ./requirements.txt

PYTHON_VERSION=`venv/bin/python3 --version`
PIP_VERSION=`venv/bin/pip3 --version`

echo -e "\nEnvironment Info:"
echo -e "  " ${PYTHON_VERSION} "\n  " ${PIP_VERSION} "\n"
