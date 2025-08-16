# OnVolunteers Notebook Scripts

This directory contains scripts for interacting with the OnVolunteers website.

## Installation

There are two recommended ways to set up the development environment: using `uv` (recommended) or using the standard `python -m venv` with `pip`.

### Using `uv` (Recommended)

1.  **Create and activate the virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

### Using `pip`

1.  **Create and activate the virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main script is `ov_reports_list.py`. This script logs into the OnVolunteers website, lists available reports, and generates a report.

The script can be run in two ways:

### Using Environment Variables

1.  **Set your credentials as environment variables:**
    ```bash
    export OV_USERNAME="your_username"
    export OV_PASSWORD="your_password"
    ```

2.  **Run the script:**
    ```bash
    python ov_reports_list.py
    ```

### Using Interactive Prompts

If the `OV_USERNAME` and `OV_PASSWORD` environment variables are not set, the script will prompt you to enter your credentials.

1.  **Run the script:**
    ```bash
    python ov_reports_list.py
    ```

2.  **Enter your username and password when prompted.**

## Developing/Contributing

When developing and adding new dependencies, please follow these steps to ensure the project stays consistent.

### Adding a Dependency

Use `uv` to add new dependencies. This will automatically update the `pyproject.toml` file.

```bash
uv add <package-name>
```

### Syncing `requirements.txt`

After adding or removing dependencies, you need to update the `requirements.txt` file. This file is a "lock file" that ensures reproducible builds for `pip` users.

To update `requirements.txt`, run the helper script:

```bash
./sync_requirements.sh
```

This will regenerate the `requirements.txt` file based on the current state of your environment and the dependencies defined in `pyproject.toml`.

**Do not edit `requirements.txt` manually.**
