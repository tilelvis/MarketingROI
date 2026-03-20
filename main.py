import os
import sqlite3
import pandas as pd

"""
main.py
-------
The master script that orchestrates the entire marketing attribution and ROI analysis pipeline.
It handles data generation, database setup, SQL queries, ROI calculation, and visualization.
"""

def cleanup():
    """
    Removes temporary files and database from previous runs to ensure a clean pipeline.
    """
    print("Step 0: Cleaning up existing analysis artifacts...")
    files_to_remove = [
        'marketing.db', 'marketing_data.csv',
        'attribution_first_click.csv', 'attribution_last_click.csv',
        'attribution_linear.csv', 'roi_analysis.csv',
        'attributed_conversions.png', 'attributed_revenue.png',
        'marketing_roi.png'
    ]
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)

def run_pipeline():
    """
    Main entry point for running the marketing analytics pipeline.
    """
    print("--- Starting Marketing Attribution & ROI Analysis Pipeline ---")

    # 0. Initial Cleanup
    cleanup()

    # 1. Generate Synthetic Marketing Data
    # 2000 users with multiple touchpoints for realistic analysis
    from generate_data import generate_marketing_data
    print("\nStep 1: Generating marketing interaction data...")
    generate_marketing_data(num_users=2000)

    # 2. Setup SQLite Environment and Ingest Data
    from setup_db import setup_sql_environment
    print("\nStep 2: Setting up SQL environment and ingesting data...")
    setup_sql_environment()

    # 3. Perform SQL-based Attribution Modeling
    from attribution_queries import run_attribution_queries
    print("\nStep 3: Calculating First-Click, Last-Click, and Linear attribution models using SQL...")
    run_attribution_queries()

    # 4. Integrate Costs and Calculate ROI
    from calculate_roi import calculate_roi
    print("\nStep 4: Integrating channel costs and calculating ROI across models...")
    calculate_roi()

    # 5. Generate Visualizations and Insights
    from visualize_results import create_visualizations
    print("\nStep 5: Generating professional visualizations and finalizing insights...")
    create_visualizations()

    print("\n--- Marketing Attribution & ROI Analysis Pipeline Complete! ---")
    print("\nOutputs Generated:")
    print("  - marketing_data.csv: Raw marketing touchpoints (~10,000+ interactions)")
    print("  - attribution_*.csv: Results from three different attribution models")
    print("  - roi_analysis.csv: Detailed Return-on-Investment metrics")
    print("  - attributed_revenue.png: Visual comparison of revenue attribution")
    print("  - attributed_conversions.png: Visual comparison of conversion attribution")
    print("  - marketing_roi.png: Visual comparison of ROI across marketing channels")

if __name__ == "__main__":
    run_pipeline()
