#!/bin/bash

# Check if it's the first run
if [ ! -f "${PWD}/.init" ]; then
  # # Wait for Dremio to start 
  # sleep 30

  # Set Dremio user and password
  DREMIO_USER='dremio'
  DREMIO_PASSWORD='dremio123'

  # Create first user
  curl 'http://localhost:9047/apiv2/bootstrap/firstuser' -X PUT \
  -H 'Authorization: _dremionull' \
  -H 'Content-Type: application/json' \
  --data-binary "{\"userName\":\"${DREMIO_USER}\",\"firstName\":\"root\",\"lastName\":\"banana\",\"email\":\"admin@admin.com\",\"createdAt\":1526186430755,\"password\":\"${DREMIO_PASSWORD}\"}"

  # Login to obtain Dremio token
  output=$(curl -X POST 'http://localhost:9047/apiv2/login' \
    -H 'Accept: */*' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/json' \
    --data-raw "{\"userName\":\"${DREMIO_USER}\",\"password\":\"${DREMIO_PASSWORD}\"}" \
    --compressed
  )

  # Check for errors in the login response
  if [[ $output == *"token"* ]]; then
    dremio_token=$(echo "$output" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
    echo "Dremio Token: $dremio_token"

    # Create Dremio Tatooine Space
    curl 'http://localhost:9047/api/v3/catalog' \
      -H 'Accept: */*' \
      -H "Authorization: _dremio${dremio_token}" \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/json' \
      --data-raw '{"name":"home","entityType":"space"}' \
      --compressed

    # Additional commands for creating folders, if needed

    # Mark that initialization is complete
    touch "${PWD}/.init"

  else
    echo "Error: Unable to obtain Dremio token. Check Dremio initialization."
  fi
else
  echo "Dremio already initialized. Skipping initialization."
fi

