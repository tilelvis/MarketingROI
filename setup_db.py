import sqlite3
import pandas as pd

def setup_sql_environment(csv_file='marketing_data.csv', db_name='marketing.db'):
    # Connect to SQLite
    conn = sqlite3.connect(db_name)

    # Read CSV
    df = pd.read_csv(csv_file)

    # Load into SQL table
    df.to_sql('marketing_interactions', conn, if_exists='replace', index=False)

    print(f"Data from {csv_file} successfully loaded into {db_name}.marketing_interactions")

    # Return connection for later use
    return conn

if __name__ == "__main__":
    setup_sql_environment()
