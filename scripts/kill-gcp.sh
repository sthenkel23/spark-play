#! /bin/bash

export PROJECT_ID=$(head -1 .env/project.ids)

# Kill the project
gcloud projects delete $PROJECT_ID

rm .env/${PROJECT_ID}--1.json
rm .env/${PROJECT_ID}--2.json

rm .env/project.ids
