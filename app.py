# email_assistant_agent.py

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
import os
import pickle
import google.generativeai as genai

# ==== CONFIGURATION ====
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CREDS_PATH = 'client_secret.json'  # Update this path if needed
TOKEN_PICKLE_PATH = 'token.pickle'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = 'gemini-1.5-flash-latest'

# ==== AUTHENTICATION ====
def authenticate_gmail():
    creds = None
    if os.path.exists(TOKEN_PICKLE_PATH):
        with open(TOKEN_PICKLE_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDS_PATH, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        auth_url, _ = flow.authorization_url(prompt='consent')
        print(f'Please go to this URL and authorize: {auth_url}')
        code = input('Enter the authorization code: ')
        token = flow.fetch_token(code=code)

        creds = Credentials(
            token['access_token'],
            refresh_token=token.get('refresh_token'),
            token_uri=flow.client_config['token_uri'],
            client_id=flow.client_config['client_id'],
            client_secret=flow.client_config['client_secret'],
            scopes=SCOPES
        )

        with open(TOKEN_PICKLE_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

# ==== GEMINI SETUP ====
def setup_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(MODEL_NAME)

# ==== UTILITIES ====
def extract_email_info(message):
    headers = message['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
    snippet = message.get('snippet', '')
    return subject, snippet

def classify_email(model, subject, snippet):
    prompt = f"""
    You are an intelligent email assistant. Categorize the following email into one of the following:
    - Urgent
    - Normal
    - Spam
    - Sponsorship
    - Collaboration
    - Personal
    - Inquiry

    Return only the category name.
    Subject: {subject}
    Snippet: {snippet}
    """
    return model.generate_content(prompt).text.strip()

def generate_reply(model, subject, snippet, category):
    prompt = f"""
    You are my intelligent email assistant. Based on the email content and its category, generate a short, polite and relevant reply.

    Email Category: {category}
    Subject: {subject}
    Email Content: {snippet}

    Make sure the tone is friendly, professional, and sounds like me. Don't add signatures.
    """
    return model.generate_content(prompt).text.strip()

def get_sender_email(msg_data):
    headers = msg_data['payload']['headers']
    sender = next((h['value'] for h in headers if h['name'] == 'From'), None)
    if sender and '<' in sender:
        return sender.split('<')[1].split('>')[0]
    return sender

def create_draft(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft = {'message': {'raw': raw_message}}
    created_draft = service.users().drafts().create(userId='me', body=draft).execute()
    print(f"\n✅ Draft created for: {subject} ➤ {to}")
    return created_draft

# ==== MAIN FLOW ====
def main():
    service = authenticate_gmail()
    model = setup_gemini()

    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=5).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        subject, snippet = extract_email_info(msg_data)
        category = classify_email(model, subject, snippet)
        reply = generate_reply(model, subject, snippet, category)
        to_email = get_sender_email(msg_data)
        create_draft(service, to_email, subject, reply)

if __name__ == '__main__':
    main()
