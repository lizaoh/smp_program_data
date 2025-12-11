import io
from googleapiclient.http import MediaIoBaseUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_and_write_file(file_name: str, parents: list, text_content: str):
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': parents
    }

    content_bytes = text_content.encode('utf-8')
    media_content = io.BytesIO(content_bytes)

    # 3. Upload the file
    media = MediaIoBaseUpload(media_content, mimetype='text/plain', resumable=True)

    response = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,name'
    ).execute()

    # print(response)
    url = f"https://docs.google.com/document/d/{response.get('id')}/edit?usp=sharing"
    print(url)
    return response, url

