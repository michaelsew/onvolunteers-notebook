# onvolunteers-notebook
A repository for a Google Colab notebook that analyzes data from Google Drive.

## Opening in Google Colab

1.  Navigate to [Google Colab](https.colab.research.google.com).
2.  Click on the "GitHub" tab.
3.  Enter the URL of this repository in the search bar.
4.  Select the `google_drive_reporting.ipynb` notebook.

## Running Locally with Jupyter

### Recommended: Using `uv`

1.  Clone the repository, create a virtual environment, install dependencies, and start the notebook server:
    ```bash
    git clone https://github.com/michaelsew/onvolunteers-notebook.git && \
    cd onvolunteers-notebook && \
    uv venv && \
    source .venv/bin/activate && \
    pip install -r requirements.txt && \
    jupyter notebook
    ```
2.  Open the `google_drive_reporting.ipynb` notebook in your browser.


### Alternative: Using `venv` and `pip`

1.  Clone the repository, create a virtual environment, install dependencies, and start the notebook server:
    ```bash
    git clone https://github.com/michaelsew/onvolunteers-notebook.git && \
    cd onvolunteers-notebook && \
    python3 -m venv .venv && \
    source .venv/bin/activate && \
    pip install -r requirements.txt && \
    jupyter notebook
    ```
2.  Open the `google_drive_reporting.ipynb` notebook in your browser.


## Running with Podman

For those who prefer containerization, you can run the Jupyter notebook using Podman:

```bash
podman run -p 8888:8888 -v "$(pwd)":/home/jovyan/work jupyter/minimal-notebook
```

## Cleaning Up: `uv cleanup` Operations

To remove the virtual environment and any logs generated during usage, you can use the following commands:

```bash
# Remove the virtual environment created by uv
uv venv remove

# Remove log files (example: app.log)
rm -f scripts/app.log
```

This will help keep your workspace clean by deleting the `.venv` folder and any log files such as `app.log`. Adjust the log file path as needed for your setup.
