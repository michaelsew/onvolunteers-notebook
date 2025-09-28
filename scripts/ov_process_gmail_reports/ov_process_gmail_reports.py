
import os
import base64
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import argparse

# ov_process_gmail_reports.py
# This script processes GMail emails containing OnVolunteers reports
# Renames them based on their content, and
# and uploads them to a specified Google Drive folder.

# --- Get the directory of the script ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuration ---
load_dotenv(dotenv_path=os.path.join(SCRIPT_DIR, 'gmail_gdrive.env'))
GDRIVE_CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, os.getenv("GDRIVE_CREDENTIALS_FILE", "credentials.json"))
LOG_FILE = os.getenv("LOG_FILE", os.path.join(SCRIPT_DIR, "process_gmail_reports.log"))
REPORTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.getenv("REPORTS_DIR", "reports")))
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/drive"]
GDRIVE_TARGET_FOLDER = "/My Drive/PTA 2025-2026 SHARED FOLDER/SubCommittees/OnVolunteers/Reports"

# Threshold to differentiate reports. If sum of "Total Hours" is > this value, it's a volunteer report.
HOURS_THRESHOLD = 4

# --- Logging Setup ---
# --- Logging Setup ---
# Get the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
root_logger.addHandler(file_handler)

# Create a stream handler (for console output)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
root_logger.addHandler(stream_handler)

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
    """Searches for emails from a specific sender with a specific subject, unread and from the past day."""
    try:
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_date = yesterday.strftime("%Y/%m/%d")
        query = f"from:{sender} subject:{subject} is:unread after:{yesterday_date}"
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
            average_total_hours = df["Total Hours"].mean()
            report_type = "volunteer" if average_total_hours >= HOURS_THRESHOLD else "parking"
            logging.info(f"Report: {os.path.basename(file_path)} - Average Total Hours: {average_total_hours:.2f}. Threshold: {HOURS_THRESHOLD}. Determined type: {report_type}")
            return report_type
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
    parser = argparse.ArgumentParser(description="Process OnVolunteers report emails from Gmail and upload to Google Drive.")
    parser.add_argument(
        "--mark-unread",
        action="store_false",
        default=True,
        help="Do not mark processed emails as unread (default: True, i.e., mark as read)"
    )
    args = parser.parse_args()

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    logging.info(f"### ov_process_gmail_reports STARTED {start_time} ###")
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
            if part["filename"] and part["filename"].endswith(".xlsx") and "OnVolunteers_Volunteer_Hours_Report" in part["filename"]:
                attachment = get_attachment(gmail_service, msg_id, part["body"]["attachmentId"])
                if attachment:
                    file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
                    original_filename = part["filename"].lstrip('/')
                    local_path = os.path.join(REPORTS_DIR, original_filename)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(file_data)
                    logging.info(f"Downloaded attachment: {original_filename}")

                    report_type = get_report_type(local_path)
                    if report_type != "unknown":
                        # Extract date from original filename (e.g., OnVolunteers_Volunteer_Hours_Report2025-09-27__125741.xlsx)
                        # The date is typically before the double underscore and after 'Report'
                        try:
                            date_str = original_filename.split("Report")[-1].split("__")[0]
                            # Attempt to parse various date formats
                            for fmt in ("%Y-%m-%d", "%Y%m%d"):
                                try:
                                    report_date = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                                    break
                                except ValueError:
                                    pass
                            else:
                                logging.warning(f"Could not parse date from filename: {original_filename}. Using current date.")
                                report_date = datetime.now().strftime("%Y-%m-%d")
                        except IndexError:
                            logging.warning(f"Could not extract date from filename: {original_filename}. Using current date.")
                            report_date = datetime.now().strftime("%Y-%m-%d")

                        # Determine the subdirectory and base filename
                        if report_type == "parking":
                            subdir = "parking-hours"
                            base_name = f"parking-hours-{report_date}.xlsx"
                        elif report_type == "volunteer":
                            subdir = "volunteer-hours"
                            base_name = f"volunteer-hours-{report_date}.xlsx"
                        else:
                            # Fallback for unknown types, though we filter for them
                            subdir = "unknown-reports"
                            base_name = f"unknown-{report_date}.xlsx"

                        target_dir = os.path.join(REPORTS_DIR, subdir)
                        os.makedirs(target_dir, exist_ok=True)

                        final_filename = base_name
                        final_local_path = os.path.join(target_dir, final_filename)

                        # Conflict resolution logic
                        if os.path.exists(final_local_path):
                            logging.info(f"File {final_filename} already exists. Checking for timestamped version.")
                            # Try saving with a more specific timestamp
                            current_time = datetime.now().strftime("%H%M")
                            timestamped_filename = f"{report_type}-hours-{report_date}_{current_time}.xlsx"
                            timestamped_local_path = os.path.join(target_dir, timestamped_filename)

                            if os.path.exists(timestamped_local_path):
                                logging.info(f"Timestamped file {timestamped_filename} also exists. Overwriting.")
                                final_local_path = timestamped_local_path
                                final_filename = timestamped_filename
                            else:
                                logging.info(f"Saving as timestamped file: {timestamped_filename}")
                                final_local_path = timestamped_local_path
                                final_filename = timestamped_filename
                        
                        # Rename the downloaded file to its final name and location
                        os.rename(local_path, final_local_path)
                        logging.info(f"Renamed file to: {final_filename}")

                        # Upload to Google Drive
                        upload_to_gdrive(drive_service, final_local_path, folder_id)
                        
                        # Optional: Mark email as read (or delete)
                        if args.mark_unread:
                            gmail_service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    logging.info(f"### ov_process_gmail_reports FINISHED {end_time} ###")

if __name__ == "__main__":
    main()
