# Process Gmail Reports

This script connects to a Gmail account, searches for specific report emails, downloads the `.xlsx` attachments, renames them based on their content, and uploads them to a specified Google Drive folder.

## Setup and Usage

1.  **Navigate to the script directory:**
    ```bash
    cd scripts/ov_process_gmail_reports
    ```

2.  **Create a virtual environment (if you haven't already):**
    ```bash
    uv venv
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

5.  **Configure environment variables:**
    Copy `gmail_gdrive.env.sample` to `gmail_gdrive.env` and fill in your `GDRIVE_CREDENTIALS_FILE`.
    ```bash
    cp gmail_gdrive.env.sample gmail_gdrive.env
    # Edit gmail_gdrive.env with your credentials
    ```

6.  **Run the main processing script:**
    ```bash
    uv run python ov_process_gmail_reports.py
    ```

7.  **Run the report identification utility:**
    ```bash
    uv run python ov_identify_report.py <path_to_your_report.xlsx>
    ```