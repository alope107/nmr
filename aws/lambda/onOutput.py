import json
import os
import urllib.parse
import boto3
from time import gmtime, strftime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# Scopes to access google drive with
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
# ID of the drive folder to store the output in
folder_id = "1yt_4wcu1sEa0e4eTPuqPMcQXW3qZ0KPH"
# Name of service account parameter in parameter store
SERVICE_ACCOUNT_PARAMETER_NAME = "drive-service-account"
# Name of the table that maps file id to email
DYNAMO_TABLE_NAME = "FileMetadata"

# Email to send results from.
SOURCE_EMAIL = "redcliffesalaman@gmail.com"

# Scratch space location
TMP_DIR = "/tmp"

print('Loading function')

RESULT_PREFIX = "results"

# Pre-load aws services
s3 = boto3.client('s3')
ssm_service = boto3.client('ssm')
dynamo_resource = boto3.resource("dynamodb")
email_client = boto3.client("ses")

metadata_table = dynamo_resource.Table(DYNAMO_TABLE_NAME)

# Get drive service account from parameter store.
response = ssm_service.get_parameter(Name=SERVICE_ACCOUNT_PARAMETER_NAME,
                                     WithDecryption=True)
service_account_string = response["Parameter"]["Value"]
service_account_info = json.loads(service_account_string)

# Pre-load drive service
credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

def lambda_handler(event, context):
    print("Got called!!!")
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    distribute_results(bucket, key)
    
def get_file_id(key):
    slash_loc = key.rindex("/")
    dot_loc = key.rindex(".")
    return key[slash_loc + 1:dot_loc]

# Uploads a file to drive and shares it with the world.
# Returns link to the file.
def upload_to_drive(local_name):
    print("Uploading file")
    file_metadata = {"name" : local_name,
                     "parents": [folder_id]}
    media = MediaFileUpload(local_name)
    f = drive_service.files().create(body=file_metadata,
                                     media_body=media,
                                     fields="id,webContentLink").execute()
    fid = f.get("id")
    link = f.get("webContentLink")
    print("Uploaded. New file id: " + fid)
    print("Download link: " + link)
    return {"id": fid, "link": link}

# Set it so anyone can download file if they have the link
def share_file(fid):
    global_permission = {
        "type": "anyone",
        "role": "reader",
    }
    drive_service.permissions().create(fileId=fid,
                                       body=global_permission).execute()

# Returns the email associated with a file id
def fetch_email(file_id):
    resp = metadata_table.get_item(Key={"file_id" : file_id})
    if "Item" not in resp:
        return None
    return resp["Item"]["email"]


def fetch_and_upload(bucket, key):
    uploaded = None
    local_name = os.path.join(TMP_DIR, get_file_id(key) + ".zip")
    s3.download_file(bucket, key, local_name)
    try:
        uploaded = upload_to_drive(local_name)
        share_file(uploaded["id"])
    finally:
        # Clean up file regardless of whether upload worked.
        print("Removing " + local_name + " from local disk")
        os.remove(local_name)
    return uploaded

def send_email(to_addr, subj, body):
    print("Sending result email to: " + to_addr)
    email_client.send_email(
        Source=SOURCE_EMAIL,
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

def email_body(link):
    return "The results of your MaLICE run can be downloaded here: " + link

# Uploads the results of the MaLICE run to a public drive link.
# Emails the user who requested the run a link to the file.
def distribute_results(bucket, key):
    fid = get_file_id(key)
    user_email = fetch_email(fid)
    uploaded = fetch_and_upload(bucket, key)
    send_email(user_email, "MaLICE Results", email_body(uploaded["link"]))