#!/bin/bash
# Generate agent_registry_cloud_run_resolved.json with actual Cloud Run URLs
# Usage: ./demo_agent_registry/generate_cloud_registry.sh

if [ -z "$GOOGLE_CLOUD_PROJECT_NUMBER" ]; then
    echo "Error: GOOGLE_CLOUD_PROJECT_NUMBER environment variable not set"
    exit 1
fi

echo "Generating agent_registry_cloud_run_resolved.json with Cloud Run URLs..."

cat demo_agent_registry/agent_registry_cloud_run_unresolved.json | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_NUMBER}/g" \
  > demo_agent_registry/agent_registry_cloud_run_resolved.json

echo "✅ Created demo_agent_registry/agent_registry_cloud_run_resolved.json"
echo ""
echo "File contains actual Cloud Run URLs:"
echo "  - Tenant ABC: ...horizon-agent-tenant-abc-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app"
echo "  - Tenant XYZ: ...horizon-agent-tenant-xyz-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app"
echo "  - IDP: ...idp-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app"

