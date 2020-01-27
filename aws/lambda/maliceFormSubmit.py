import boto3
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

import io
import json

# Name of service account parameter in parameter store
SERVICE_ACCOUNT_PARAMETER_NAME = "drive-service-account"
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", 
          "https://www.googleapis.com/auth/drive.readonly"]
# Key prefix and suffix for file to be uploaded to s3
BUCKET = "malice"
KEY_PREFIX = "input/"
KEY_SUFFIX = ".csv"
# Only process files that are owned by us in Google Drive.
TRUSTED_EMAILS = ["redcliffesalaman@gmail.com"]
# Email address to send results from
FROM_EMAIL = "redcliffesalaman@gmail.com"
DYNAMO_TABLE_NAME = "FileMetadata"

# Pre-load aws services
s3_service = boto3.client('s3')
ssm_service = boto3.client('ssm')
ses_service = boto3.client("ses")
dynamo_resource = boto3.resource("dynamodb")

table = dynamo_resource.Table(DYNAMO_TABLE_NAME)

# Get drive service account from parameter store.
response = ssm_service.get_parameter(Name=SERVICE_ACCOUNT_PARAMETER_NAME,
                                     WithDecryption=True)
service_account_string = response["Parameter"]["Value"]
service_account_info = json.loads(service_account_string)

# Pre-load drive service
credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Returns a BytesIO representation of the file stored in Google Drive
# with the given file_id.
def get_drive_file(file_id):
    metadata = drive_service.files().get(fileId=file_id, fields="owners").execute()
    owner_email = metadata["owners"][0]["emailAddress"]
    if owner_email not in TRUSTED_EMAILS:
        raise RuntimeError(("Expected file to be owned by one of: {} " +
            "Untrusted file owned by: {}").format(TRUSTED_EMAILS, owner_email))

    bytes = drive_service.files().get_media(fileId=file_id).execute()
    return io.BytesIO(bytes)

# Uploads a file to s3.
def upload_to_s3(f, bucket, file_id, key=None):
    if not key:
        key = KEY_PREFIX + file_id + KEY_SUFFIX
    s3_service.upload_fileobj(f, bucket, key)

# Sends an email
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
    
def set_email(file_id, email):
    table.put_item(
        Item={
            "file_id": file_id,
            "email": email,
        }
    )
    
def lambda_handler(event, context):
    print("Incoming event", event)
    body = json.loads(event["body"])
    file_id = body["fileId"]
    email = body["email"]
    print("File id: {} Email: {}".format(file_id, email))
    f = get_drive_file(file_id)
    upload_to_s3(f, BUCKET, file_id)
    set_email(file_id, email)
    send_email(email, 
        "Malice Results", 
        "Your MaLICE data has been accepted and a run will begin soon")
    return {
        'statusCode': 200,
        'body': json.dumps('All good~')
    }