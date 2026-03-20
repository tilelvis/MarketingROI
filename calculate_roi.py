import pandas as pd
import sqlite3

"""
calculate_roi.py
----------------
Integrates marketing cost data with the attribution results to calculate ROI.
Demonstrates the impact of attribution models on profitability metrics.
"""

# Hypothetical costs per interaction (e.g., Cost-Per-Click)
CHANNEL_COSTS = {
    'Search': 2.50,
    'Social': 1.50,
    'Email': 0.50,
    'Display': 1.00,
    'Direct': 0.00  # Usually free or considered zero direct cost
}

def calculate_roi(db_name='marketing.db', costs=CHANNEL_COSTS):
    """
    Calculates ROI for each marketing channel based on three attribution models.

    Parameters:
    - db_name (str): SQLite database file.
    - costs (dict): Dictionary mapping channel names to their per-interaction cost.
    """
    # 1. Load interaction counts from SQLite to compute total channel costs
    conn = sqlite3.connect(db_name)
    interaction_counts = pd.read_sql_query("SELECT channel, COUNT(*) as clicks FROM marketing_interactions GROUP BY channel", conn)
    conn.close()

    # Map costs and calculate total spend per channel
    interaction_counts['cpc'] = interaction_counts['channel'].map(costs)
    interaction_counts['total_cost'] = interaction_counts['clicks'] * interaction_counts['cpc']

    # 2. Load the previously calculated attribution results
    df_first = pd.read_csv('attribution_first_click.csv')
    df_last = pd.read_csv('attribution_last_click.csv')
    df_linear = pd.read_csv('attribution_linear.csv')

    def merge_and_calculate_roi(attr_df, cost_df, model_name):
        """
        Helper function to merge costs and calculate ROI for a specific model.
        """
        merged = pd.merge(attr_df, cost_df[['channel', 'total_cost']], on='channel')
        # ROI Formula: (Attributed Revenue - Total Cost) / Total Cost
        merged['roi'] = (merged['attributed_revenue'] - merged['total_cost']) / merged['total_cost']
        # Handle 'inf' for zero-cost channels (e.g., Direct)
        merged.loc[merged['total_cost'] == 0, 'roi'] = float('inf')
        merged['model'] = model_name
        return merged

    # Process all three models
    roi_first = merge_and_calculate_roi(df_first, interaction_counts, 'First-Click')
    roi_last = merge_and_calculate_roi(df_last, interaction_counts, 'Last-Click')
    roi_linear = merge_and_calculate_roi(df_linear, interaction_counts, 'Linear')

    # 3. Consolidate ROI results and export to CSV
    all_roi = pd.concat([roi_first, roi_last, roi_linear])
    all_roi.to_csv('roi_analysis.csv', index=False)

    print("Merged cost data and calculated ROI across all models.")
    return all_roi

if __name__ == "__main__":
    calculate_roi()
