```bash
#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
export REGION=us-central1
export REPOSITORY_NAME=horizon-integration-test

docker build -f demo_agent_registry/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest .

docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest

cat demo_agent_registry/service.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -

# (Optional) Allow unauthenticated access
gcloud run services add-iam-policy-binding horizon-integration-test--agent-registry-service \
  --region=${REGION} \
  --member="allUsers" \
  --role="roles/run.invoker"


### Testing deployments

# local
curl "http://localhost:5001/agents"

# unauthenticated (for testing only)
curl "https://horizon-integration-test--agent-registry-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/agents"
```