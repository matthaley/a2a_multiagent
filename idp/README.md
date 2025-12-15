#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
export REGION=us-central1
export REPOSITORY_NAME=horizon-integration-test

docker build -f idp/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/idp:latest .

docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/idp:latest

gcloud run services replace idp/service.yaml \
  --region=${REGION} \
  --project=${GOOGLE_CLOUD_PROJECT_ID}
  --update-env-vars=GCP_PROJECT_NUMBER=${GOOGLE_CLOUD_PROJECT_NUMBER},GCP_SERVICE_ACCOUNT=${GOOGLE_CLOUD_SERVICE_ACCOUNT}