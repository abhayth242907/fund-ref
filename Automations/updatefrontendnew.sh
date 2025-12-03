#!/bin/bash

INSTANCE_ID="i-0a4e3a2feba169a50"

ipv4_address=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

file_to_find="../frontend/.env.docker"

if [ ! -f "$file_to_find" ]; then
  echo "ERROR: $file_to_find not found."
  exit 1
fi

sed -i -e "s|REACT_APP_API_BASE_URL=.*|REACT_APP_API_BASE_URL=http://${ipv4_address}:8000|g" $file_to_find

echo "Updated frontend REACT_APP_API_BASE_URL with: http://${ipv4_address}:8000"
