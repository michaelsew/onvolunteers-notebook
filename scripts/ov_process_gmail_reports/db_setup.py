
import duckdb

DB_FILE = "onvolunteers.db"

def setup_database():
    """Creates the DuckDB database and tables if they don't exist."""
    con = duckdb.connect(DB_FILE)

    # Create volunteer_hours table
    con.execute("""
    CREATE TABLE IF NOT EXISTS volunteer_hours (
        report_id VARCHAR,
        report_type VARCHAR,
        report_date VARCHAR,
        processed_timestamp VARCHAR,
        source_filename VARCHAR,
        email_id VARCHAR,
        email_sender VARCHAR,
        email_subject VARCHAR,
        gdrive_file_id VARCHAR,
        gdrive_folder_path VARCHAR,
        "Last Name" VARCHAR,
        "First Name" VARCHAR,
        "Child Last Name" VARCHAR,
        "Child First Name" VARCHAR,
        "Children" VARCHAR,
        "Email" VARCHAR,
        "Telephone" VARCHAR,
        "Upcoming Hours" DOUBLE,
        "Pending Hours" DOUBLE,
        "Finished Hours" DOUBLE,
        "Adhoc Hours" DOUBLE,
        "Total Hours" DOUBLE,
        "FundRaising Hours" DOUBLE,
        "Target Hours" DOUBLE,
        "Adjustment Hours" DOUBLE,
        "Adjust Notes" VARCHAR
    )
    """)

    # Create parking_hours table
    con.execute("""
    CREATE TABLE IF NOT EXISTS parking_hours (
        report_id VARCHAR,
        report_type VARCHAR,
        report_date VARCHAR,
        processed_timestamp VARCHAR,
        source_filename VARCHAR,
        email_id VARCHAR,
        email_sender VARCHAR,
        email_subject VARCHAR,
        gdrive_file_id VARCHAR,
        gdrive_folder_path VARCHAR,
        "Last Name" VARCHAR,
        "First Name" VARCHAR,
        "Child Last Name" VARCHAR,
        "Child First Name" VARCHAR,
        "Children" VARCHAR,
        "Email" VARCHAR,
        "Telephone" VARCHAR,
        "Upcoming Hours" DOUBLE,
        "Pending Hours" DOUBLE,
        "Finished Hours" DOUBLE,
        "Adhoc Hours" DOUBLE,
        "Total Hours" DOUBLE,
        "FundRaising Hours" DOUBLE,
        "Target Hours" DOUBLE,
        "Adjustment Hours" DOUBLE,
        "Adjust Notes" VARCHAR
    )
    """)

    con.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
