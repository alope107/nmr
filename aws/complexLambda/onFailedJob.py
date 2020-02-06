import boto3

import json

STATE_CHANGE_DETAIL = "Batch Job State Change"
FAILED_STATUS = "FAILED"
FROM_EMAIL = "redcliffesalaman@gmail.com"
DYNAMO_TABLE_NAME = "FileMetadata"

ses_service = boto3.client("ses")
dynamo_resource = boto3.resource("dynamodb")
metadata_table = dynamo_resource.Table(DYNAMO_TABLE_NAME)


# TODO(auberon): Find good way to share code between lambdas.
def get_file_id(key):
    slash_loc = key.rindex("/")
    dot_loc = key.rindex(".")
    return key[slash_loc + 1:dot_loc]

# TODO(auberon): Find good way to share code between lambdas.
def send_email(to_addr, subj, body):
    print("Sending email to " + to_addr)
    resp = ses_service.send_email(
        Source=FROM_EMAIL,
        Destination={"ToAddresses": [to_addr]},
        Message={
            "Subject": {
                "Data": subj,
            },
            "Body": {
                "Text": {
                    "Data": body,
                }
            }
        }
    )
    print(resp)

def fetch_email(file_id):
    resp = metadata_table.get_item(Key={"file_id" : file_id})
    if "Item" not in resp:
        return None
    return resp["Item"]["email"]

def lambda_handler(event, context):
    # Do not handle any non-failure results
    if not (event["detail-type"] == STATE_CHANGE_DETAIL and
            event["detail"]["status"] == FAILED_STATUS):
        return {'statusCode': 200}
    
    
    key = event["detail"]["container"]["command"][0]
    file_id = get_file_id(key)
    print("Failure for file: " + file_id)
    email = fetch_email(file_id)
    print("Sending error email to: " + email)
    send_email(email, 
            "Failed CompLEx Run", 
            "There was an error while running your CompLEx job. " + \
            "We are looking into the issue. Thank you for your patience.")
