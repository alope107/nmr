from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
service = build('drive', 'v3')

def hello_world(request):
    """Lists the files available to the service account.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        A string enumerating the available files.
    """
    
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    res = str(results.get('files', []))
    return res
