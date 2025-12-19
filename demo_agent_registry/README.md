```bash
#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
#export REGION= [get from .env]
#export REPOSITORY_NAME= [get from .env]

# Generate resolved registry file with actual Cloud Run URLs
## How it works
# 1. **Template file**: `agent_registry_cloud_run_unresolved.json` contains placeholders like `GCP_PROJECT_NUMBER_PLACEHOLDER`
# 2. **Generated file**: `agent_registry_cloud_run_resolved.json` is created by the script with actual URLs
# 3. **Deployment**: The Docker image includes the resolved file, which the service uses at runtime
# **Note**: The resolved file is gitignored to avoid committing real Cloud Run URLs.
./demo_agent_registry/generate_cloud_registry.sh

# Build and push Docker image
docker build -f demo_agent_registry/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest .

docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/agent-registry:latest

# Deploy to Cloud Run
cat demo_agent_registry/service.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_NUMBER}/g" | \
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
# note this should diplay the correct resolved urls
curl "https://horizon-integration-test--agent-registry-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/agents"
```