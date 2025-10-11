
import duckdb
import argparse

DB_FILE = "onvolunteers.db"

def query_database(query):
    """Executes a query against the DuckDB database and prints the results."""
    con = duckdb.connect(DB_FILE)
    result = con.execute(query).fetchdf()
    con.close()
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query the OnVolunteers database.')
    parser.add_argument('query', type=str, help='The SQL query to execute.')
    args = parser.parse_args()

    query_database(args.query)
