#! /bin/bash
export PROJECT_NAME=spark-play
export PROJECT_ID=${PROJECT_NAME}-${RANDOM}
export SERVICE_ACCOUNT_NAME=johndoe
export GOOGLE_APPLICATION_CREDENTIALS=.env/${PROJECT_ID}--2.json
export BUCKET_NAME=${PROJECT_ID}-garden
export STORAGE_CLASS=STANDARD
export CLUSTER=${PROJECT_ID}-compute
export REGION=europe-west6


# Set the gcp project
gcloud auth login

echo "\nCREATING PROJECT"
echo "================\n\n"
gcloud projects create ${PROJECT_ID} 
gcloud beta projects get-iam-policy ${PROJECT_ID} --format=json > .env/${PROJECT_ID}--1.json
gcloud beta projects set-iam-policy ${PROJECT_ID} .env/${PROJECT_ID}--1.json
export BILLING_ID=`gcloud beta billing accounts list | awk 'f;/ACCOUNT_ID/{f=1}' | awk {'print $1}'`
gcloud beta billing projects link ${PROJECT_ID} --billing-account=$BILLING_ID
gcloud beta billing projects describe ${PROJECT_ID}
gcloud config set project ${PROJECT_ID}

# Enable APIs
echo "\nENABLING APIs"
echo "=================\n\n"
for SERVICE in storage-component.googleapis.com dataproc.googleapis.com compute.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com
do
    echo "Enabling ... -> " $SERVICE
    gcloud services enable ${SERVICE} --project=${PROJECT_ID}
done

# Create service account
echo "\nCREATING A SERVICE ACCOUNT"
echo "==========================\n\n"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} --display-name="QuickStart"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/owner" 
gcloud iam service-accounts keys create $GOOGLE_APPLICATION_CREDENTIALS \
    --iam-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

gcloud auth activate-service-account --project=${PROJECT_ID} --key-file=${GOOGLE_APPLICATION_CREDENTIALS}


# Create a bucket
echo "\nCREATING A BUCKET"
echo "=================\n\n"
gcloud storage buckets create gs://${BUCKET_NAME} \
    --project=${PROJECT_ID} \
    --default-storage-class=${STORAGE_CLASS} \
    --location=${REGION} \
    --uniform-bucket-level-access

# Create a Dataproc cluster. Run the command, below, 
# to create a single-node Dataproc cluster in the specified Compute Engine zone.

echo "\nCREATING A CLUSTER"
echo "=================\n\n"
gcloud dataproc clusters create ${CLUSTER} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --single-node
    # --image-version=2.0-ubuntu18 \
    # --master-machine-type \
    # --bucket=${BUCKET}
    

echo "\n CREATING A ARTIFACTORY"
echo "=================\n\n"
gcloud config set artifacts/repository ${PROJECT_NAME}
gcloud config set artifacts/location ${REGION}
# gcloud artifacts packages list --project=${PROJECT_ID} 
# gcloud artifacts packages list --repository=${PROJECT_NAME}

echo $PROJECT_ID >> .env/project.ids
