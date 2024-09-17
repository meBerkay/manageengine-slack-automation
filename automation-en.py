import requests
import sys
import json
import datetime

# The 'requests' package must be installed using -pip install requests-.

# Get the filename from command line arguments
filename = str(sys.argv[1])

# Read the JSON file
with open(filename, encoding='utf-8') as data_file:
    data = json.load(data_file)

requestObj = data['request']

# Assign values to variables
workorderid = requestObj['id']
requester = requestObj['requester']['name']
createdby = requestObj['created_by']['name']
priority = requestObj.get('priority', {}).get('name', '-')  # Default to '-' if 'priority' is not available
subject = requestObj.get('subject', 'Not Specified')  # Default to 'Not Specified' if 'subject' is not available

# Technician information and tagging (Using Slack user IDs for mentions)
technician = requestObj.get('technician', {}).get('name', 'Not Specified')  # Default to 'Not Specified' if 'technician' is not available
if technician == "John Doe":
    technician_mention = "<@USER1234>"
elif technician == "Jane Smith":
    technician_mention = "<@USER5678>"
elif technician == "Alex Johnson":
    technician_mention = "<@USER91011>"
elif technician == "Chris Lee":
    technician_mention = "<@USER12131>"
else:
    technician_mention = "Technician Not Specified."  # Message to indicate unspecified technician

channel = "#supportchannel"
CREATEDTIME = requestObj['created_time']['value']
scheduledstarttime = datetime.datetime.fromtimestamp(int(CREATEDTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')

# Formatted payload
# Update the 'url_template' with the ManageEngine Service Desk Plus ticket viewing link.
url_template = "https://example.com/WorkOrder.do?woMode=viewWO&woID="
url_with_id = url_template + workorderid
payload = {
    "channel": channel,
    "text": (
        "*A new support request has been created.*\n\n"
        "⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n"
        f"**Subject:** {subject}\n"
        f"**Click to View Ticket:** <{url_with_id}|Click Here>\n"
        f"**Priority:** {priority}\n"
        f"**Creation Time:** {scheduledstarttime}\n"
        f"**Created By:** {createdby}\n"
        f"**Requester:** {requester}\n"
        f"**Technician:** {technician_mention}"
    )
}

# Slack Webhook URL
slack_webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

# Send the message to Slack
response = requests.post(slack_webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

# Check the response
if response.status_code == 200:
    print("Message sent successfully.")
else:
    print(f"An error occurred while sending the message. Status code: {response.status_code}")
