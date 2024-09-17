# ManageEngine Service Desk Plus to Slack Integration

This project provides a script for automating the notification of support requests from ManageEngine Service Desk Plus to a Slack channel. The script reads support request details from a JSON file and sends a formatted message to a specified Slack channel using a webhook.

## Overview

The script performs the following tasks:

1. **Reads JSON File**: Extracts support request data from a JSON file.
2. **Formats Data**: Processes and formats the request information.
3. **Sends to Slack**: Sends a notification message to a Slack channel using a webhook URL.

## Prerequisites

- Python 3.x
- `requests` library (can be installed via `pip install requests`)
- Access to a ManageEngine Service Desk Plus instance
- Slack workspace and a configured incoming webhook URL

## Script Details

### File Structure

- `your_script.py`: The main script that handles the JSON processing and sends the message to Slack.

### How to Use

1. **Prepare the JSON File**:
   - Ensure your JSON file contains the support request data in the expected format.

2. **Write the Script**:
   - Go to ManageEngine Service Desk Plus Admin > Custom Triggers > Add Custom Triggers Group And Custom Trigger
   - Go to the action section and copy the relevant py file to the folder "ManageEngine\ServiceDesk\integration\custom_scripts" where the manage engine is installed.
   - Then, on the custom trigger's page, Execute Script is selected from the Actions section and the .txt that will run the py file is written in the relevant field.
   - The relevant example is located below the text box.

### Code Explanation

1. **File Name Retrieval**:
   - The script takes the JSON file name as a command-line argument.

2. **Read the JSON File**:
   - It opens the JSON file and loads the data into a Python dictionary.

3. **Extract and Format Data**:
   - The script extracts key pieces of information such as request ID, requester name, creation time, and priority.
   - It maps technician names to Slack user mentions and formats the creation time.

4. **Prepare Slack Message**:
   - Constructs a payload containing the formatted support request details.

5. **Send Message to Slack**:
   - Uses a Slack webhook URL to send the message to a specified Slack channel.

6. **Response Handling**:
   - Checks the HTTP response status to confirm whether the message was sent successfully.

### Configuration

- **Webhook URL**: Update the `slack_webhook_url` variable in the script with your Slack webhook URL.
- **Slack Channel**: Set the `channel` variable to the appropriate Slack channel where you want to post the notifications.

### Example

An example JSON file might look like this:

```json
{
  "request": {
    "id": "12345",
    "requester": {
      "name": "John Doe"
    },
    "created_by": {
      "name": "Jane Smith"
    },
    "priority": {
      "name": "High"
    },
    "subject": "Issue with login",
    "technician": {
      "name": "Alex Johnson"
    },
    "created_time": {
      "value": "1677601200000"
    }
  }
}
