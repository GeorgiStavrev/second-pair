#!/bin/bash
SERVICE_NAME=ak-second-pair
REPO_NAME=$SERVICE_NAME-$BUILD_ENV
IMAGE_DIGESTS=($(aws ecr list-images --repository-name $REPO_NAME | jq -r '.imageIds[].imageDigest'))

PARAM=""
for element in "${IMAGE_DIGESTS[@]}"
do
    PARAM="${PARAM} imageDigest=${element}"
done
aws ecr batch-delete-image --repository-name $REPO_NAME --image-ids $PARAM
