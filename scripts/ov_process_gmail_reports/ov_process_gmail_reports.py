
import os
import base64
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import pandas as pd
from dotenv import load_dotenv

# --- Get the directory of the script ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuration ---
load_dotenv(dotenv_path=os.path.join(SCRIPT_DIR, '.env'))
GDRIVE_CREDENTIALS_FILE = os.getenv("GDRIVE_CREDENTIALS_FILE", "credentials.json")
LOG_FILE = os.getenv("LOG_FILE", os.path.join(SCRIPT_DIR, "process_gmail_reports.log"))
REPORTS_DIR = os.getenv("REPORTS_DIR", os.path.join(SCRIPT_DIR, "reports"))
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/drive"]
GDRIVE_TARGET_FOLDER = "/My Drive/PTA 2025-2026 SHARED FOLDER/SubCommittees/OnVolunteers/Reports"
# Threshold to differentiate reports. If sum of "Total Hours" is > this value, it's a volunteer report.
HOURS_THRESHOLD = 1000

# --- Logging Setup ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_credentials():
    """Gets user credentials from the specified credentials file."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GDRIVE_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def search_emails(service, sender, subject):
    """Searches for emails from a specific sender with a specific subject."""
    try:
        query = f"from:{sender} subject:{subject}"
        result = service.users().messages().list(userId="me", q=query).execute()
        messages = result.get("messages", [])
        return messages
    except HttpError as error:
        logging.error(f"An error occurred while searching for emails: {error}")
        return []

def get_attachment(service, msg_id, attachment_id):
    """Gets a specific attachment from a message."""
    try:
        return service.users().messages().attachments().get(userId="me", messageId=msg_id, id=attachment_id).execute()
    except HttpError as error:
        logging.error(f"An error occurred while getting an attachment: {error}")
        return None

def get_report_type(file_path):
    """Determines the report type by summing the 'Total Hours' column."""
    try:
        df = pd.read_excel(file_path, header=0)
        if "Total Hours" in df.columns:
            total_hours = df["Total Hours"].sum()
            if total_hours > HOURS_THRESHOLD:
                return "volunteer"
            else:
                return "parking"
        else:
            logging.warning(f"'Total Hours' column not found in {file_path}. Could not determine report type.")
            return "unknown"
    except Exception as e:
        logging.error(f"An error occurred while reading the excel file: {e}")
        return "unknown"

def get_gdrive_folder_id(service, folder_name):
    """Finds the ID of a Google Drive folder by its name."""
    try:
        # This is a simplified search. It will find the first folder with that name.
        # For a more robust solution, you might need to traverse the folder hierarchy.
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get("files", [])
        if not items:
            logging.error(f"Google Drive folder '{folder_name}' not found.")
            return None
        return items[0]["id"]
    except HttpError as error:
        logging.error(f"An error occurred while searching for the Google Drive folder: {error}")
        return None

def upload_to_gdrive(service, file_path, folder_id):
    """Uploads a file to a specific Google Drive folder."""
    try:
        file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
        media = MediaFileUpload(file_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        logging.info(f"File uploaded successfully. File ID: {file.get('id')}")
        return file.get("id")
    except HttpError as error:
        logging.error(f"An error occurred while uploading the file to Google Drive: {error}")
        return None

def main():
    """Main function to process emails and attachments."""
    logging.info("Starting email processing...")
    creds = get_credentials()
    gmail_service = build("gmail", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    messages = search_emails(gmail_service, "no-reply@onvolunteers.com", "Requested OnVolunteers Report")
    if not messages:
        logging.info("No new report emails found.")
        return

    # Find the Google Drive folder ID
    # We are taking the last part of the path as the folder name to search for
    target_folder_name = os.path.basename(GDRIVE_TARGET_FOLDER)
    folder_id = get_gdrive_folder_id(drive_service, target_folder_name)
    if not folder_id:
        return

    for msg in messages:
        msg_id = msg["id"]
        message = gmail_service.users().messages().get(userId="me", id=msg_id).execute()
        for part in message["payload"]["parts"]:
            if part["filename"] and part["filename"].endswith(".xlsx"):
                attachment = get_attachment(gmail_service, msg_id, part["body"]["attachmentId"])
                if attachment:
                    file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
                    original_filename = part["filename"]
                    local_path = os.path.join(REPORTS_DIR, original_filename)
                    with open(local_path, "wb") as f:
                        f.write(file_data)
                    logging.info(f"Downloaded attachment: {original_filename}")

                    report_type = get_report_type(local_path)
                    if report_type != "unknown":
                        # Create the new filename
                        timestamp = original_filename.split("__")[-1].split(".")[0]
                        new_filename = f"{report_type}_hours_report_{timestamp}.xlsx"
                        new_local_path = os.path.join(REPORTS_DIR, new_filename)
                        os.rename(local_path, new_local_path)
                        logging.info(f"Renamed file to: {new_filename}")

                        # Upload to Google Drive
                        upload_to_gdrive(drive_service, new_local_path, folder_id)
                        
                        # Optional: Mark email as read (or delete)
                        # gmail_service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

    logging.info("Email processing finished.")

if __name__ == "__main__":
    main()
