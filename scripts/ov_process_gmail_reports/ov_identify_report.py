#!/usr/bin/env python
"""
Identifies the type of an OnVolunteers report file.

Usage:
  python ov_identify_report.py <path_to_report.xlsx>
"""

import sys
import os
import pandas as pd

# Threshold to differentiate reports. If sum of "Total Hours" is > this value, it's a volunteer report.
HOURS_THRESHOLD = 4

def get_report_type(file_path):
    """Determines the report type by summing the 'Total Hours' column."""
    try:
        df = pd.read_excel(file_path, header=0)
        if "Total Hours" in df.columns:
            average_total_hours = df["Total Hours"].mean()
            if average_total_hours >= HOURS_THRESHOLD:
                return "volunteer"
            else:
                return "parking"
        else:
            print(f"Warning: 'Total Hours' column not found in {file_path}. Could not determine report type.", file=sys.stderr)
            return "unknown"
    except Exception as e:
        print(f"An error occurred while reading the excel file: {e}", file=sys.stderr)
        return "unknown"

def main():
    if len(sys.argv) < 2:
        print("Usage: python ov_identify_report.py <path_to_report.xlsx>")
        sys.exit(1)

    report_path = sys.argv[1]

    if not os.path.exists(report_path):
        print(f"Error: File not found at '{report_path}'")
        sys.exit(1)

    report_type = get_report_type(report_path)

    if report_type == "unknown":
        print(f"Could not determine the report type for '{report_path}'.")
    else:
        print(f"The report '{report_path}' is a '{report_type}-hours' report.")

if __name__ == "__main__":
    main()