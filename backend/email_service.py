import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json not found. Please download it from Google Cloud Console.")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def fetch_recent_emails(service, max_results=10) -> List[Dict]:
    """Fetches recent unread emails from the inbox."""
    try:
        # Fetch unread messages from INBOX
        results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
        messages = results.get('messages', [])

        email_data_list = []
        for msg in messages:
            msg_id = msg['id']
            msg_info = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            
            headers = msg_info.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown")
            
            snippet = msg_info.get('snippet', '')
            thread_id = msg_info.get('threadId', '')
            
            email_data_list.append({
                'message_id': msg_id,
                'thread_id': thread_id,
                'sender': sender,
                'subject': subject,
                'snippet': snippet,
                'raw_payload': msg_info
            })
            
        return email_data_list
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def apply_label_to_email(service, message_id: str, label_name: str):
    """Applies a specific label to an email, creating it if it doesn't exist."""
    try:
        # First check if label exists
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        label_id = None
        
        for label in labels:
            if label['name'].lower() == label_name.lower():
                label_id = label['id']
                break
                
        # If label doesn't exist, create it
        if not label_id:
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            created_label = service.users().labels().create(userId='me', body=label_object).execute()
            label_id = created_label['id']
            
        # Apply label to message (and remove UNREAD to mark as processed if desired, 
        # but for now we just add the category label)
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': [label_id], 'removeLabelIds': []}
        ).execute()
        
        return True
    except HttpError as error:
        print(f'An error occurred applying label: {error}')
        return False
