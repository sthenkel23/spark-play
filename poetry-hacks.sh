#!/bin/bash

PACKAGE_NAME="spark-play"

poetry new --src $PACKAGE_NAME
poetry add --group dev darglint flake8 black isort mypi pytest pytest-cov pylint pydocstyle safety

poetry install

export PYTHONPATH=$PYTHONPATH:$PWD/src

poetry run spark-play      
