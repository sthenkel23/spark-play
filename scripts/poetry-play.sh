#!/bin/bash

poetry install
export PYTHONPATH=$PYTHONPATH:$PWD/src
poetry shell
poetry run spark-play      
