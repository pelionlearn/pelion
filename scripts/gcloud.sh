#!/bin/bash

if [[ $1 == "build" ]]; then
    gcloud builds submit --config=cloudbuild.yml .
elif [[ $1 == "pull" ]]; then
    docker pull us-central1-docker.pkg.dev/pelion-503219/docker-repo/pelion-frontend:latest
    docker pull us-central1-docker.pkg.dev/pelion-503219/docker-repo/pelion-api:latest
    docker pull us-central1-docker.pkg.dev/pelion-503219/docker-repo/pelion-celery:latest
    docker tag us-central1-docker.pkg.dev/pelion-503219/docker-repo/pelion-frontend:latest pelion-frontend:latest
    docker tag us-central1-docker.pkg.dev/pelion-503219/docker-repo/pelion-api:latest pelion-api:latest
    docker tag us-central1-docker.pkg.dev/pelion-503219/docker-repo/pelion-celery:latest pelion-celery:latest
fi
