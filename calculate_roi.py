import pandas as pd

# Define hypothetical costs per click (CPC) for each channel
# This can be easily modified or moved to a config file
CHANNEL_COSTS = {
    'Search': 2.50,
    'Social': 1.50,
    'Email': 0.50,
    'Display': 1.00,
    'Direct': 0.00  # Usually free or very low cost
}

def calculate_roi(db_name='marketing.db', costs=CHANNEL_COSTS):
    # Load total interactions by channel to calculate total cost
    import sqlite3
    conn = sqlite3.connect(db_name)
    total_interactions = pd.read_sql_query("SELECT channel, COUNT(*) as clicks FROM marketing_interactions GROUP BY channel", conn)
    conn.close()

    # Calculate costs
    total_interactions['cost_per_click'] = total_interactions['channel'].map(costs)
    total_interactions['total_cost'] = total_interactions['clicks'] * total_interactions['cost_per_click']

    # Load attribution results
    df_first = pd.read_csv('attribution_first_click.csv')
    df_last = pd.read_csv('attribution_last_click.csv')
    df_linear = pd.read_csv('attribution_linear.csv')

    # Merge costs with attribution results
    def merge_roi(attr_df, costs_df, model_name):
        merged = pd.merge(attr_df, costs_df[['channel', 'total_cost']], on='channel')
        merged['roi'] = (merged['attributed_revenue'] - merged['total_cost']) / merged['total_cost']
        # Handle division by zero for Direct channel
        merged.loc[merged['total_cost'] == 0, 'roi'] = float('inf')
        merged['model'] = model_name
        return merged

    roi_first = merge_roi(df_first, total_interactions, 'First-Click')
    roi_last = merge_roi(df_last, total_interactions, 'Last-Click')
    roi_linear = merge_roi(df_linear, total_interactions, 'Linear')

    # Combine results
    all_roi = pd.concat([roi_first, roi_last, roi_linear])

    print("--- ROI Analysis (Linear Model) ---")
    print(roi_linear[['channel', 'attributed_revenue', 'total_cost', 'roi']])

    all_roi.to_csv('roi_analysis.csv', index=False)
    print("\nROI analysis saved to roi_analysis.csv")

if __name__ == "__main__":
    calculate_roi()
