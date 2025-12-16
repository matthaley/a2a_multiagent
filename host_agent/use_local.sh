#!/bin/bash
# Source this script to configure host_agent to use local services
# Usage: source host_agent/use_local.sh

# Unset all Cloud Run overrides to use config.json defaults
unset AGENT_REGISTRY_BASE_URL
unset AGENT_REGISTRY_URL
unset IDP_BASE_URL
unset IDP_TOKEN_URL
unset IDP_AUTHORIZE_URL
unset REDIRECT_URI

echo "✅ Host agent configured to use local services (from config.json)"
echo "   Agent Registry: http://localhost:5001"
echo "   IDP: http://localhost:5000"
echo ""
echo "Now run: python -m host_agent"

