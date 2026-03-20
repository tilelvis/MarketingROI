import sqlite3
import pandas as pd

"""
attribution_queries.py
----------------------
Executes SQL queries to calculate revenue attribution using three common models:
1. First-Click: Full credit to the first touchpoint.
2. Last-Click: Full credit to the last touchpoint before conversion.
3. Linear: Equal credit to all touchpoints in a journey.
"""

def run_attribution_queries(db_name='marketing.db'):
    """
    Runs attribution SQL queries and saves the results as CSV files.

    Parameters:
    - db_name (str): Name of the SQLite database to query.
    """
    conn = sqlite3.connect(db_name)

    # 1. Identify converting users and their full journeys
    # This SQL View filters for touchpoints leading up to (and including) conversion.
    conn.execute("DROP VIEW IF EXISTS converted_journeys")
    conn.execute("""
    CREATE VIEW converted_journeys AS
    WITH conversion_times AS (
        SELECT user_id, MIN(timestamp) as conv_time
        FROM marketing_interactions
        WHERE conversion = 1
        GROUP BY user_id
    ),
    conversion_revenue AS (
        SELECT user_id, timestamp, revenue
        FROM marketing_interactions
        WHERE conversion = 1
    )
    SELECT m.user_id, m.timestamp, m.channel, m.campaign, m.conversion, cr.revenue
    FROM marketing_interactions m
    JOIN conversion_times ct ON m.user_id = ct.user_id
    JOIN conversion_revenue cr ON m.user_id = cr.user_id AND ct.conv_time = cr.timestamp
    WHERE m.timestamp <= ct.conv_time
    """)

    # 2. First-Click Attribution Query
    # Uses ROW_NUMBER() to identify the first touchpoint for each customer journey.
    first_click_query = """
    WITH ranked_touches AS (
        SELECT
            user_id,
            channel,
            revenue,
            ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY timestamp ASC) as rank
        FROM converted_journeys
    )
    SELECT
        channel,
        COUNT(*) as conversions,
        SUM(revenue) as attributed_revenue
    FROM ranked_touches
    WHERE rank = 1
    GROUP BY channel
    ORDER BY attributed_revenue DESC
    """

    # 3. Last-Click Attribution Query
    # Uses ROW_NUMBER() with DESC order to find the final touchpoint before conversion.
    last_click_query = """
    WITH ranked_touches AS (
        SELECT
            user_id,
            channel,
            revenue,
            ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY timestamp DESC) as rank
        FROM converted_journeys
    )
    SELECT
        channel,
        COUNT(*) as conversions,
        SUM(revenue) as attributed_revenue
    FROM ranked_touches
    WHERE rank = 1
    GROUP BY channel
    ORDER BY attributed_revenue DESC
    """

    # 4. Linear Attribution Query
    # Divides the total conversion revenue by the count of touchpoints in that user's journey.
    linear_query = """
    WITH journey_stats AS (
        SELECT user_id, COUNT(*) as total_touchpoints, MAX(revenue) as total_revenue
        FROM converted_journeys
        GROUP BY user_id
    )
    SELECT
        cj.channel,
        SUM(1.0 / js.total_touchpoints) as conversions,
        SUM(js.total_revenue / js.total_touchpoints) as attributed_revenue
    FROM converted_journeys cj
    JOIN journey_stats js ON cj.user_id = js.user_id
    GROUP BY cj.channel
    ORDER BY attributed_revenue DESC
    """

    # Run and export First-Click
    df_first = pd.read_sql_query(first_click_query, conn)
    df_first.to_csv('attribution_first_click.csv', index=False)

    # Run and export Last-Click
    df_last = pd.read_sql_query(last_click_query, conn)
    df_last.to_csv('attribution_last_click.csv', index=False)

    # Run and export Linear
    df_linear = pd.read_sql_query(linear_query, conn)
    df_linear.to_csv('attribution_linear.csv', index=False)

    print("Calculated First-Click, Last-Click, and Linear attribution results.")

    conn.close()

if __name__ == "__main__":
    run_attribution_queries()
