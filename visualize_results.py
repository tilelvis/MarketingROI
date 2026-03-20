import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
visualize_results.py
--------------------
Generates professional visualizations comparing attribution results and ROI.
Uses Seaborn and Matplotlib to create three core charts for marketing analysis.
"""

def create_visualizations(roi_file='roi_analysis.csv'):
    """
    Loads ROI analysis results and produces PNG visualization files.

    Parameters:
    - roi_file (str): Path to the ROI results CSV file.
    """
    # Load combined ROI data across all models
    df = pd.read_csv(roi_file)

    # Set the general style and color palette
    sns.set_theme(style="whitegrid", palette="muted")

    # --- Chart 1: Attributed Revenue per Model and Channel ---
    plt.figure(figsize=(12, 7))
    sns.barplot(x='channel', y='attributed_revenue', hue='model', data=df)
    plt.title('Attributed Revenue by Marketing Channel and Model', fontsize=16)
    plt.ylabel('Attributed Revenue ($)', fontsize=12)
    plt.xlabel('Marketing Channel', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Attribution Model')
    plt.tight_layout()
    plt.savefig('attributed_revenue.png', dpi=300)
    plt.close()

    # --- Chart 2: Conversions per Model and Channel ---
    plt.figure(figsize=(12, 7))
    sns.barplot(x='channel', y='conversions', hue='model', data=df)
    plt.title('Attributed Conversions by Marketing Channel and Model', fontsize=16)
    plt.ylabel('Conversions (Count / Shares)', fontsize=12)
    plt.xlabel('Marketing Channel', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Attribution Model')
    plt.tight_layout()
    plt.savefig('attributed_conversions.png', dpi=300)
    plt.close()

    # --- Chart 3: ROI Comparison (excluding Direct for visual clarity) ---
    # The 'Direct' channel often has 'inf' ROI (as its cost is 0), which makes plotting difficult.
    plot_df = df[df['channel'] != 'Direct'].copy()

    plt.figure(figsize=(12, 7))
    sns.barplot(x='channel', y='roi', hue='model', data=plot_df)
    plt.title('Marketing ROI by Channel and Model (Excl. Direct Traffic)', fontsize=16)
    plt.ylabel('ROI (Return on Investment Ratio)', fontsize=12)
    plt.xlabel('Marketing Channel', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Attribution Model')
    plt.tight_layout()
    plt.savefig('marketing_roi.png', dpi=300)
    plt.close()

    print("Generated professional visualizations: attributed_revenue.png, attributed_conversions.png, and marketing_roi.png.")

if __name__ == "__main__":
    create_visualizations()
