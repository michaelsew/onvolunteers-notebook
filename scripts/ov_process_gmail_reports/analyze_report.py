
import pandas as pd
import numpy as np
import logging
import logging.config
import os
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Logging Configuration ---
LOG_DIR = os.path.join(SCRIPT_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "analyze_report.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE,
            "level": "DEBUG",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        }
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "DEBUG",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description='Analyze an OnVolunteers report.')
parser.add_argument('file_path', type=str, help='The path to the report file.')
args = parser.parse_args()

# Load the Excel file
df = pd.read_excel(args.file_path)

# Data Cleaning and Preparation
# It's common for column names to have leading/trailing spaces
df.columns = df.columns.str.strip()

# --- Analysis ---

# 1. Families who have completed their target hours
# Assuming 'Total Hours' and 'Target Hours' are columns in the dataframe
if 'Total Hours' in df.columns and 'Target Hours' in df.columns:
    completed_target_hours = df[df['Total Hours'] >= df['Target Hours']]
    num_completed_target_hours = len(completed_target_hours)
    logging.info(f"Number of families who have completed their target hours: {num_completed_target_hours}")

# 2. Families who have finished hours
# Assuming 'Finished Hours' is a column in the dataframe
if 'Finished Hours' in df.columns:
    finished_hours = df[df['Finished Hours'] > 0]
    num_finished_hours = len(finished_hours)
    logging.info(f"Number of families who have finished hours: {num_finished_hours}")

# 3. Families who have completed or registered their fundraising hours
# Assuming 'FundRaising Hours' is a column in the dataframe
if 'FundRaising Hours' in df.columns:
    fundraising_hours = df[df['FundRaising Hours'] > 0]
    num_fundraising_hours = len(fundraising_hours)
    logging.info(f"Number of families who have completed or registered fundraising hours: {num_fundraising_hours}")

# 4. Additional Insights
# Average number of hours contributed
if 'Total Hours' in df.columns:
    average_hours = df['Total Hours'].mean()
    logging.info(f"Average number of hours contributed per family: {average_hours:.2f}")

# Distribution of families by percentage of target hours completed
if 'Total Hours' in df.columns and 'Target Hours' in df.columns:
    df['Percent Complete'] = (df['Total Hours'] / df['Target Hours'])
    df['Percent Complete'] = df['Percent Complete'].fillna(0)
    df['Percent Complete'] = df['Percent Complete'].replace([np.inf, -np.inf], 0)
    df['Percent Complete'] = df['Percent Complete'] * 100
    bins = [0, 25, 50, 75, 100, np.inf]
    labels = ['0-25%', '26-50%', '51-75%', '76-100%', '>100%']
    df['Completion Bracket'] = pd.cut(df['Percent Complete'], bins=bins, labels=labels, right=False)
    completion_distribution = df['Completion Bracket'].value_counts().sort_index()
    logging.info("\nDistribution of families by percentage of target hours completed:")
    logging.info(completion_distribution)
