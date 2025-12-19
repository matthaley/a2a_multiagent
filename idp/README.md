```bash
#export GOOGLE_CLOUD_PROJECT_ID= [get from .env]
#export GOOGLE_CLOUD_PROJECT_NUMBER= [get from .env]
#export REGION= [get from .env]
#export REPOSITORY_NAME= [get from .env]

docker build -f idp/Dockerfile -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/idp:latest .

docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT_ID}/${REPOSITORY_NAME}/idp:latest

cat idp/service.yaml | \
  sed "s/GCP_PROJECT_ID_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_ID}/g" | \
  sed "s/GCP_PROJECT_NUMBER_PLACEHOLDER/${GOOGLE_CLOUD_PROJECT_NUMBER}/g" | \
  sed "s/GCP_SERVICE_ACCOUNT_PLACEHOLDER/${GOOGLE_CLOUD_SERVICE_ACCOUNT}/g" | \
  gcloud run services replace --region=${REGION} --project=${GOOGLE_CLOUD_PROJECT_ID} -

# (Optional) Allow unauthenticated access
gcloud run services add-iam-policy-binding horizon-integration-test--idp-service \
  --region=${REGION} \
  --member="allUsers" \
  --role="roles/run.invoker"


### Testing deployments

# local
curl "http://localhost:5000/jwks.json"
curl "http://localhost:5000/.well-known/openid-configuration"

# unauthenticated (for testing only)
curl "https://horizon-integration-test--idp-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/jwks.json"
curl "https://horizon-integration-test--idp-service-${GOOGLE_CLOUD_PROJECT_NUMBER}.us-central1.run.app/.well-known/openid-configuration"
```