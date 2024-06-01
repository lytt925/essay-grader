import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from pydantic import BaseModel
import os


class Mail(BaseModel):
    to: str
    subject: str
    content: str


SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    "https://www.googleapis.com/auth/gmail.send"
]


def send_mail(mail: Mail):
    creds = None
    if os.path.exists("./private/token.json"):
        creds = Credentials.from_authorized_user_file("./private/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./private/client_secret_desktop.json", SCOPES
            )

            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("./private/token.json", "w") as token:
                token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    body = mail.content
    message = MIMEText(body, 'html')

    # message = MIMEText('This is the body of the email')
    message['to'] = mail.to
    message['subject'] = mail.subject
    create_message = {'raw': base64.urlsafe_b64encode(
        message.as_bytes()).decode()}

    try:
        message = (
            service.users()
                   .messages()
                   .send(userId="me", body=create_message)
                   .execute()
        )
        return {"message": "Email sent successfully"}
    except HTTPError as error:
        print(f"An error occurred: {error}")


def main():
    mail = Mail(to="r12227113@ntu.edu.tw", subject="Test",
                content="This is a test email")
    res = send_mail(mail)
    print(res)


if __name__ == "__main__":
    main()
