#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
export REGION=us-central1
export REPOSITORY_NAME=horizon-integration-test

docker build -f demo_agent_registry/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest .

docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest

cat demo_agent_registy/service.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -