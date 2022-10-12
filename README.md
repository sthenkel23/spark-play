# Boilerplate
Run pyspark locally and on GCP

[![Test, CI & Create Artifact](https://github.com/sthenkel23/spark-play/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sthenkel23/spark-play/actions/workflows/ci.yml)

## Get started 
`source scripts/poetry-setup-skeleton.sh`

## GCP
`source scripts/setup-gcp.sh`

Make changes in `flows/pipeline-1.py`

`make dist`

`source scripts/submit-dataproc-spark.sh`

When done

`source kill-gcp.sh`

## Contribute
Create issues and PRs to the dev branch.
