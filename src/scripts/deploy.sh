#!/bin/bash
GIT_SHA_SHORT=$(git rev-parse --short "$GIT_SHA")
REPO_LOCATION=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
REPO_EXISTS=$(aws ecr describe-repositories | grep "\"repositoryName\": \"$REPO_NAME\"")
if [ -z "$REPO_EXISTS" ]
then
    echo "$REPO_NAME ECR repository doesn't exist."
else
    echo "$REPO_NAME ECR repository exists."
    aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $REPO_LOCATION
    DOCKER_SCAN_SUGGEST=false docker build --build-arg GIT_SHA_SHORT=$GIT_SHA_SHORT -t $REPO_NAME:$GIT_SHA_SHORT -f Dockerfile . && docker tag $REPO_NAME:$GIT_SHA_SHORT $REPO_LOCATION/$REPO_NAME:$GIT_SHA_SHORT && docker push $REPO_LOCATION/$REPO_NAME:$GIT_SHA_SHORT
fi