import google.auth
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file

scopes = ['https://www.googleapis.com/auth/chat.bot']
credentials, project_id = google.auth.default()
# credentials = load_credentials_from_file("./keys/service_account.json", scopes=scopes)
credentials = credentials.with_scopes(scopes=scopes)
chat = build('chat', 'v1', credentials=credentials)


def send_async_test(space_name, text):
    response = {"text": text}
    chat.spaces().messages().create(
        parent=space_name,
        body=response).execute()


if __name__ == '__main__':
    space = "spaces/i2uCdgAAAAE"
    text = "Hello World!"
    send_async_test(space, text)
