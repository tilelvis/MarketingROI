import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create an artifacts directory if you want to keep files separate
# For now, we'll keep them in the same directory as per original design.

def cleanup():
    # Remove files if they already exist from a previous run
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

def run_all():
    # Cleanup before starting
    cleanup()

    # 1. Generate Data
    from generate_data import generate_marketing_data
    print("Step 1: Generating marketing interaction data...")
    generate_marketing_data()

    # 2. Setup DB
    from setup_db import setup_sql_environment
    print("\nStep 2: Loading data into SQLite database...")
    setup_sql_environment()

    # 3. Run Attribution Queries
    from attribution_queries import run_attribution_queries
    print("\nStep 3: Executing SQL attribution queries...")
    run_attribution_queries()

    # 4. Calculate ROI
    from calculate_roi import calculate_roi
    print("\nStep 4: Calculating ROI based on attribution results...")
    calculate_roi()

    # 5. Visualize
    from visualize_results import create_visualizations
    print("\nStep 5: Generating visualizations...")
    create_visualizations()

    print("\n--- Marketing ROI Analysis Complete ---")
    print("Files Generated:")
    print("- marketing_data.csv: Raw marketing interaction data")
    print("- marketing.db: SQLite database with the marketing data")
    print("- attribution_*.csv: Results from different attribution models")
    print("- roi_analysis.csv: Comprehensive ROI calculations")
    print("- attributed_revenue.png: Visualization of attributed revenue")
    print("- attributed_conversions.png: Visualization of attributed conversions")
    print("- marketing_roi.png: Visualization of ROI per channel")

if __name__ == "__main__":
    run_all()
