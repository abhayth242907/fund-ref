#!/bin/bash

INSTANCE_ID="i-0b7970a8bbaeceda6"
AWS_REGION="eu-west-1"

PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$AWS_REGION" \
    --query "Reservations[0].Instances[0].PublicIpAddress" \
    --output text)

FRONTEND_URL="http://$PUBLIC_IP:3000"

sed -i "s|FRONTEND_URL=.*|FRONTEND_URL=$FRONTEND_URL|g" ../backend/.env.docker

echo "Updated backend FRONTEND_URL with: $FRONTEND_URL"
