import requests
import json
import sys
import os

# This script will be called from /home/team-4/team-4/app
# python3 ../scripts/canary_alert.py $avg_response_time

sys.path.append('auto_deployment/')
from emailer import send_email
from logger import Logger

# get the logger initialized
log = Logger(os.path.join(os.getcwd(), "auto_deployment"), "canary_fail")
avg_response_time = sys.argv[1]

message = f"The Canary release could not be deployed. Switching from canary to stable deployment. The average response time was more than 500ms: {avg_response_time}ms."
log.error("The Canary release could not be deployed. Switching from canary to stable deployment.")
log.error(f"The average response time was more than 500ms: {avg_response_time}")

def slack_post():
    url = 'https://hooks.slack.com/services/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'
    payload = {"text": message}
    json_payload = json.dumps(payload)

    # Set the headers to indicate that the payload is in JSON format
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print('POST request successful')
        log.debug("Successfully sent slack notification for Canary container abort.")
    else:
        log.error("Canary container abort slack notification failed with status code {response.status_code}.")

def email_alert():
    send_email("ALERT: Canary release was aborted.", message)
    log.debug("Successfully sent email alert for Canary container abort.")

if __name__ == "__main__":
    email_alert()
    slack_post()
