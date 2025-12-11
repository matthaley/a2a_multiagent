curl http://0.0.0.0:10008/.well-known/agent-card.json

curl -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://horizon-integration-test--horizon-agent-tenant-abc-833546053256.us-central1.run.app/.well-known/agent-card.json"

