import sqlite3
import pandas as pd

def run_attribution_queries(db_name='marketing.db'):
    conn = sqlite3.connect(db_name)

    # 1. Identify converting users and their full journeys
    # Only touchpoints before (and including) conversion are relevant
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

    # 2. First-Click Attribution
    first_click_query = """
    WITH first_clicks AS (
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
    FROM first_clicks
    WHERE rank = 1
    GROUP BY channel
    ORDER BY attributed_revenue DESC
    """

    # 3. Last-Click Attribution
    last_click_query = """
    WITH last_clicks AS (
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
    FROM last_clicks
    WHERE rank = 1
    GROUP BY channel
    ORDER BY attributed_revenue DESC
    """

    # 4. Linear Attribution
    linear_query = """
    WITH journey_counts AS (
        SELECT user_id, COUNT(*) as touchpoints, MAX(revenue) as total_revenue
        FROM converted_journeys
        GROUP BY user_id
    )
    SELECT
        cj.channel,
        SUM(1.0 / jc.touchpoints) as conversions,
        SUM(jc.total_revenue / jc.touchpoints) as attributed_revenue
    FROM converted_journeys cj
    JOIN journey_counts jc ON cj.user_id = jc.user_id
    GROUP BY cj.channel
    ORDER BY attributed_revenue DESC
    """

    print("--- First-Click Attribution ---")
    df_first = pd.read_sql_query(first_click_query, conn)
    print(df_first)

    print("\n--- Last-Click Attribution ---")
    df_last = pd.read_sql_query(last_click_query, conn)
    print(df_last)

    print("\n--- Linear Attribution ---")
    df_linear = pd.read_sql_query(linear_query, conn)
    print(df_linear)

    # Save results to CSV for visualization step
    df_first.to_csv('attribution_first_click.csv', index=False)
    df_last.to_csv('attribution_last_click.csv', index=False)
    df_linear.to_csv('attribution_linear.csv', index=False)

    conn.close()

if __name__ == "__main__":
    run_attribution_queries()
