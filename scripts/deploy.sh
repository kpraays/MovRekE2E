#!/bin/bash
 
# Build the canary version of the application
cd ~/team-4
git checkout main 
cd app 
docker compose up -d --build --force-recreate inference_canary

# Sleep for 12 hours
echo "Monitoring the average response time... See you in 12 hours :)"
sleep $((12 * 60 * 60))

threshold=0.5
# Calculate averag response time over the last 12 hours
response=$(curl -g 'http://localhost:9090/api/v1/query' --data-urlencode 'query=sum(flask_http_request_duration_seconds_sum{path=~"/recommend/.*"}) / sum(flask_http_request_duration_seconds_count{path=~"/recommend/.*"})')
avg_response_time=$(echo $response | awk -F'[][]' '/value/{print $3}' | awk -F',' '/".*"/{gsub(/"/, "", $2); print $2}')

echo "Average response time over the last 12 hours: $avg_response_time"

if (( $(echo "$avg_response_time < $threshold" | bc -l) )); then
  echo "Switching from canary to stable deployment..."
  docker compose up -d --build --force-recreate inference_stable
else
  echo "Average response time is greater than threshold ($avg_response_time ms > 500 ms). Canary release aborted."
  python3 ../scripts/canary_alert.py $avg_response_time
  docker compose down inference_canary 
fi
