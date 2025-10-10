
import pandas as pd
import numpy as np

# Load the Excel file
file_path = 'ov_process_gmail_reports/reports/volunteer-hours/volunteer-hours-2025-10-10.xlsx'
df = pd.read_excel(file_path)

# Data Cleaning and Preparation
# It's common for column names to have leading/trailing spaces
df.columns = df.columns.str.strip()

# --- Analysis ---

# 1. Families who have completed their target hours
# Assuming 'Total Hours' and 'Target Hours' are columns in the dataframe
if 'Total Hours' in df.columns and 'Target Hours' in df.columns:
    completed_target_hours = df[df['Total Hours'] >= df['Target Hours']]
    num_completed_target_hours = len(completed_target_hours)
    print(f"Number of families who have completed their target hours: {num_completed_target_hours}")

# 2. Families who have finished hours
# Assuming 'Finished Hours' is a column in the dataframe
if 'Finished Hours' in df.columns:
    finished_hours = df[df['Finished Hours'] > 0]
    num_finished_hours = len(finished_hours)
    print(f"Number of families who have finished hours: {num_finished_hours}")

# 3. Families who have completed or registered their fundraising hours
# Assuming 'FundRaising Hours' is a column in the dataframe
if 'FundRaising Hours' in df.columns:
    fundraising_hours = df[df['FundRaising Hours'] > 0]
    num_fundraising_hours = len(fundraising_hours)
    print(f"Number of families who have completed or registered fundraising hours: {num_fundraising_hours}")

# 4. Additional Insights
# Average number of hours contributed
if 'Total Hours' in df.columns:
    average_hours = df['Total Hours'].mean()
    print(f"Average number of hours contributed per family: {average_hours:.2f}")

# Distribution of families by percentage of target hours completed
if 'Total Hours' in df.columns and 'Target Hours' in df.columns:
    df['Percent Complete'] = (df['Total Hours'] / df['Target Hours']) * 100
    bins = [0, 25, 50, 75, 100, np.inf]
    labels = ['0-25%', '26-50%', '51-75%', '76-100%', '>100%']
    df['Completion Bracket'] = pd.cut(df['Percent Complete'], bins=bins, labels=labels, right=False)
    completion_distribution = df['Completion Bracket'].value_counts().sort_index()
    print("\nDistribution of families by percentage of target hours completed:")
    print(completion_distribution)
