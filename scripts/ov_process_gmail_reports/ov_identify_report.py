#!/usr/bin/env python
"""
Identifies the type of an OnVolunteers report file.

Usage:
  python ov_identify_report.py <path_to_report.xlsx>
"""

import sys
import os

# Add the script's directory to the Python path to allow importing from the parent script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ov_process_gmail_reports import get_report_type

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
