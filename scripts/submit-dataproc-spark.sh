#! /bin/bash

gcloud dataproc jobs submit pyspark flows/pipeline-1.py \
    --cluster=${CLUSTER} \
    --region=${REGION} \
    --files dist/spark_play.pex \
    --properties-file=configs/job-profile \
    --py-files dist/spark_play-0.1.0-py3-none-any.whl \
    -- ${BUCKET_NAME}
    #     --properties-file=
    # -- gs://${BUCKET_NAME}/input/ gs://${BUCKET_NAME}/output/
