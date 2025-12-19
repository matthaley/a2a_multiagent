# Horizon Agent

This agent is a sample tenant-specific service that provides information about orders.

## Function

The Horizon Agent is designed to simulate a service that would be used by a specific tenant (e.g., a specific company or user). It has a single tool, `get_order_status`, which returns mock data for an order.

In the multi-tenant architecture, an instance of the Horizon Agent is run for a specific tenant. The `host_agent` is responsible for routing requests to the correct instance based on the `tenant_id`.

## Running the Agent

For instructions on how to run this agent as part of the complete demo, please see the main [README.md](../../README.md) file.

## Docker Deployment

The Horizon Agent can be deployed as a standalone Docker container.

### Building the Docker Image

From the project root directory:

```bash
docker build -f horizon_agent/Dockerfile -t horizon-agent:latest .
```

### Running the Container

The `--tenant-id` argument is required. You can override other settings via command-line arguments or environment variables:

```bash
# Basic usage with required tenant-id
docker run -p 8000:8000 \
  -e APP_URL="http://localhost:8000" \
  -e IDP_URL="http://localhost:5000" \
  horizon-agent:latest \
  --tenant-id tenant-abc

# Custom port and host
docker run -p 10008:10008 \
  -e APP_URL="http://localhost:10008" \
  -e IDP_URL="http://idp:5000" \
  horizon-agent:latest \
  --host 0.0.0.0 \
  --port 10008 \
  --tenant-id tenant-xyz

# With custom log level
docker run -p 8000:8000 \
  -e APP_URL="http://localhost:8000" \
  -e IDP_URL="http://localhost:5000" \
  horizon-agent:latest \
  --tenant-id tenant-abc \
  --log-level debug
```

### Environment Variables

- `APP_URL`: The public URL where the agent is accessible (default: auto-detected)
- `IDP_URL`: The URL of the Identity Provider for OAuth 2.0 (default: `http://localhost:5000`)
- `GOOGLE_API_KEY`: Required if not using Vertex AI (set via `GOOGLE_GENAI_USE_VERTEXAI=TRUE`)

### Command-Line Arguments

- `--tenant-id` (required): The tenant ID for this agent instance
- `--host`: Hostname to bind the server to (default: `0.0.0.0`)
- `--port`: Port to bind the server to (default: `8000`)
- `--log-level`: Uvicorn log level (default: `info`)

## Google Cloud Run Deployment

The Horizon Agent can be deployed to Google Cloud Run using the provided `service.yaml` configuration file.

### Prerequisites

1. Google Cloud SDK (`gcloud`) installed and configured
2. Docker installed (for building the image)
3. A GCP project with Cloud Run API enabled
4. Artifact Registry access (repository must be created first)

### Building and Pushing the Docker Image

First, create an Artifact Registry repository if you haven't already:

```bash
# Set your GCP project ID and region
#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
#export REGION= [get from .env]
#export REPOSITORY_NAME= [get from .env]

# Create Artifact Registry repository (Docker format)
gcloud artifacts repositories create ${REPOSITORY_NAME} \
  --repository-format=docker \
  --location=${REGION} \
  --description="Docker repository for horizon integration test"
```

Then build and push the Docker image:

```bash
# Build the Docker image
docker build -f horizon_agent/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/horizon-agent:latest .

# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/horizon-agent:latest
```

### Deploying to Cloud Run

1. **Update the service.yaml file:**
   - Replace `REPOSITORY_NAME` with your Artifact Registry repository name
   - Update `APP_URL` with your Cloud Run service URL (you can update this after first deployment)
   - Update `IDP_URL` with your Identity Provider service URL
   - Set `TENANT_ID` to the appropriate tenant ID for this deployment

2. **Deploy the service:**
```bash
# Deploy Tenant ABC service
cat horizon_agent/service-tenant-abc.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_NUMBER}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -

# (Optional) Allow unauthenticated access
gcloud run services add-iam-policy-binding horizon-integration-test--horizon-agent-tenant-abc \
  --region=${REGION} \
  --member="allUsers" \
  --role="roles/run.invoker"

# Deploy Tenant XYZ service
cat horizon_agent/service-tenant-xyz.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_NUMBER}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -

gcloud run services add-iam-policy-binding horizon-integration-test--horizon-agent-tenant-xyz \
  --region=${REGION} \
  --member="allUsers" \
  --role="roles/run.invoker"
```

### Testing deployments

You can test local and deployed app with,

```bash
# local testing
curl http://0.0.0.0:10008/.well-known/agent-card.json

curl -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://horizon-integration-test--horizon-agent-tenant-abc-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/.well-known/agent-card.json"

# impersonate service account method
TOKEN=$(gcloud auth print-access-token --impersonate-service-account=${GOOGLE_CLOUD_SERVICE_ACCOUNT})
curl -H "Authorization: Bearer $TOKEN" "https://horizon-integration-test--horizon-agent-tenant-abc-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/.well-known/agent-card.json"

# unauthenticated (for testing only)
curl "https://horizon-integration-test--horizon-agent-tenant-abc-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/.well-known/agent-card.json"
```
