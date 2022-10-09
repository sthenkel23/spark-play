#!/bin/bash

poetry shell
poetry install
export PYTHONPATH=$PYTHONPATH:$PWD/src
poetry run spark_play      
