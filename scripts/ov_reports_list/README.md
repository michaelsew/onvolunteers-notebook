# OnVolunteers Reports List

This script logs in to OnVolunteers and provides an interactive way to generate reports.

## Setup and Usage

1.  **Navigate to the script directory:**
    ```bash
    cd scripts/ov_reports_list
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
    Copy `ov.env.sample` to `ov.env` and fill in your `OV_USERNAME` and `OV_PASSWORD`.
    ```bash
    cp ov.env.sample ov.env
    # Edit ov.env with your credentials
    ```

6.  **Run the script:**
    ```bash
    uv run python ov_reports_list.py
    ```