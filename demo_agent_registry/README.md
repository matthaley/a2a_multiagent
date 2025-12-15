#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
export REGION=us-central1
export REPOSITORY_NAME=horizon-integration-test

docker build -f demo_agent_registry/Dockerfile -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest .

docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest

gcloud run services replace demo_agent_registry/service.yaml \
  --region=${REGION} \
  --project=${PROJECT_ID}
  --update-env-vars=GCP_PROJECT_NUMBER=${GOOGLE_CLOUD_PROJECT_NUMBER},GCP_SERVICE_ACCOUNT=${GOOGLE_CLOUD_SERVICE_ACCOUNT}