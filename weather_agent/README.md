# Weather Agent

This agent provides weather information for a given location. It is a remote agent that can be used by other agents.

## Function

The Weather Agent simulates a weather forecasting service. It has a single tool, `get_weather`, which returns mock weather data for a requested city.

## Running the Agent

For instructions on how to run this agent as part of the complete demo, please see the main [README.md](../README.md) file.

## Docker Deployment

The Weather Agent can be deployed as a standalone Docker container.

### Building the Docker Image

From the project root directory:

```bash
docker build -f weather_agent/Dockerfile -t weather-agent:latest .
```

### Running the Container

You can override settings via command-line arguments or environment variables:

```bash
# Basic usage with default settings
docker run -p 8080:8080 \
  -e APP_URL="http://localhost:8080" \
  -e IDP_URL="http://localhost:5000" \
  weather-agent:latest

# Custom port
docker run -p 10001:10001 \
  -e APP_URL="http://localhost:10001" \
  -e IDP_URL="http://idp:5000" \
  weather-agent:latest \
  --port 10001

# With custom log level
docker run -p 8080:8080 \
  -e APP_URL="http://localhost:8080" \
  -e IDP_URL="http://localhost:5000" \
  weather-agent:latest \
  --log-level debug
```

### Environment Variables

- `APP_URL`: The public URL where the agent is accessible (default: auto-detected)
- `IDP_URL`: The URL of the Identity Provider for OAuth 2.0 (default: `http://localhost:5000`)
- `GOOGLE_API_KEY`: Required if not using Vertex AI (set via `GOOGLE_GENAI_USE_VERTEXAI=TRUE`)

### Command-Line Arguments

- `--host`: Hostname to bind the server to (default: `0.0.0.0`)
- `--port`: Port to bind the server to (default: `10001`)
- `--log-level`: Uvicorn log level (default: `info`)

## Google Cloud Run Deployment

The Weather Agent can be deployed to Google Cloud Run using the provided `service.yaml` configuration file.

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
docker build -f weather_agent/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/weather-agent:latest .

# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/weather-agent:latest
```

### Deploying to Cloud Run

1. **Update the service.yaml file:**
   - Replace `REPOSITORY_NAME` with your Artifact Registry repository name
   - Update `APP_URL` with your Cloud Run service URL (you can update this after first deployment)
   - Update `IDP_URL` with your Identity Provider service URL

2. **Deploy the service:**
```bash
# Deploy Weather Agent service
cat weather_agent/service.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_NUMBER}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -

# (Optional) Allow unauthenticated access
gcloud run services add-iam-policy-binding horizon-integration-test--weather-agent \
  --region=${REGION} \
  --member="allUsers" \
  --role="roles/run.invoker"
```

### Testing Deployments

You can test local and deployed app with:

```bash
# Local testing
curl http://0.0.0.0:10001/.well-known/agent-card.json

# Unauthenticated (for testing only)
curl "https://horizon-integration-test--weather-agent-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/.well-known/agent-card.json"
```

## Architecture Notes

The Weather Agent validates OAuth 2.0 tokens from the IDP service using the shared `auth_lib` validation library. It uses JWT signature verification against the IDP's JWKS endpoint to ensure all incoming requests are authenticated.
