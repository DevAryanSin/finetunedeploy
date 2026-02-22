# GCP Deployment (Cloud Run)

This backend is configured to run on Google Cloud Run.

## 1. Prerequisites

- `gcloud` CLI installed and authenticated
- Billing enabled on your GCP project
- APIs enabled:
  - Cloud Run API
  - Cloud Build API
  - Artifact Registry API

## 2. One-time setup

```bash
gcloud config set project <YOUR_PROJECT_ID>
gcloud artifacts repositories create hackfest \
  --repository-format=docker \
  --location=us-central1
```

## 3. Deploy with Cloud Build

Run from the `backend` directory:

```bash
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions _SERVICE=hackfest-backend,_REGION=us-central1,_IMAGE=us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/hackfest/backend:latest,_GROQ_CLOUD_API=<YOUR_GROQ_KEY>
```

## 4. Deploy directly (alternative)

```bash
gcloud run deploy hackfest-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_CLOUD_API=<YOUR_GROQ_KEY>
```

## 5. Recommended production env vars

- `GROQ_CLOUD_API`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `DEMO_CACHE_SESSION_ID` (optional)

For production, store secrets in Secret Manager and map them in Cloud Run instead of passing raw values.

