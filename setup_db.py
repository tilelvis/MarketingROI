import sqlite3
import pandas as pd

"""
setup_db.py
-----------
Automates the creation of a SQLite database and the ingestion of CSV marketing data.
Sets the stage for SQL-based attribution modeling.
"""

def setup_sql_environment(csv_file='marketing_data.csv', db_name='marketing.db'):
    """
    Connects to SQLite, reads the marketing CSV, and loads it into a table.

    Parameters:
    - csv_file (str): Path to the CSV file to load.
    - db_name (str): Name of the SQLite database file to create.
    """
    # Connect to SQLite (creates db if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Load raw data from CSV
    df = pd.read_csv(csv_file)

    # Load data into SQL table (replacing if already exists)
    df.to_sql('marketing_interactions', conn, if_exists='replace', index=False)

    print(f"Ingested {len(df)} rows into '{db_name}.marketing_interactions' table.")

    # Close connection
    conn.close()

if __name__ == "__main__":
    setup_sql_environment()
