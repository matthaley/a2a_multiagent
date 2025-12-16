#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
export REGION=us-central1
export REPOSITORY_NAME=horizon-integration-test

docker build -f idp/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/idp:latest .

docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/idp:latest

cat idp/service.yaml | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GCP_PROJECT_NUMBER}/g" | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -