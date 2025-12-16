#!/bin/bash
# Source this script to configure host_agent to use Cloud Run services
# Usage: source host_agent/use_cloud_run.sh

# Make sure environment variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT_NUMBER" ]; then
    echo "Error: GOOGLE_CLOUD_PROJECT_NUMBER environment variable not set"
    return 1
fi

# Agent Registry URLs
export AGENT_REGISTRY_BASE_URL="https://horizon-integration-test--agent-registry-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app"
export AGENT_REGISTRY_URL="https://horizon-integration-test--agent-registry-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/agents"

# IDP URLs
export IDP_BASE_URL="https://horizon-integration-test--idp-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app"
export IDP_TOKEN_URL="https://horizon-integration-test--idp-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/generate-token"
export IDP_AUTHORIZE_URL="https://horizon-integration-test--idp-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/authorize"

# Host Agent callback (still local)
export REDIRECT_URI="http://localhost:8083/callback"

echo "✅ Host agent configured to use Cloud Run services"
echo "   Agent Registry: $AGENT_REGISTRY_BASE_URL"
echo "   IDP: $IDP_BASE_URL"
echo ""
echo "Now run: python -m host_agent"

