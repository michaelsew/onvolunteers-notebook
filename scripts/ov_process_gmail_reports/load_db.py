
import duckdb
import os
import glob
import pandas as pd

DB_FILE = "onvolunteers.db"
DATA_LAKE_DIR = "reports/data_lake"

def get_latest_file(report_type):
    """Finds the latest parquet file for a given report type."""
    files = glob.glob(os.path.join(DATA_LAKE_DIR, f"{report_type}-*.parquet"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_data():
    """Loads data from the latest parquet files into the DuckDB database."""
    con = duckdb.connect(DB_FILE)

    # Load volunteer hours
    latest_volunteer_file = get_latest_file("volunteer")
    if latest_volunteer_file:
        print(f"Loading data from {latest_volunteer_file} into volunteer_hours table...")
        df = pd.read_parquet(latest_volunteer_file)
        columns = '", "'.join(df.columns)
        con.execute(f'INSERT INTO volunteer_hours ("{columns}") SELECT * FROM df')
        print("Volunteer hours data loaded.")
    else:
        print("No volunteer hours parquet files found.")

    # Load parking hours
    latest_parking_file = get_latest_file("parking")
    if latest_parking_file:
        print(f"Loading data from {latest_parking_file} into parking_hours table...")
        df = pd.read_parquet(latest_parking_file)
        columns = '", "'.join(df.columns)
        con.execute(f'INSERT INTO parking_hours ("{columns}") SELECT * FROM df')
        print("Parking hours data loaded.")
    else:
        print("No parking hours parquet files found.")

    con.close()

if __name__ == "__main__":
    load_data()
