import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(roi_file='roi_analysis.csv'):
    # Load combined ROI data
    df = pd.read_csv(roi_file)

    # 1. Attributed Revenue by Model and Channel
    plt.figure(figsize=(12, 6))
    sns.barplot(x='channel', y='attributed_revenue', hue='model', data=df)
    plt.title('Attributed Revenue by Marketing Channel and Model')
    plt.ylabel('Revenue ($)')
    plt.xlabel('Channel')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('attributed_revenue.png')
    plt.close()

    # 2. Conversions by Model and Channel
    plt.figure(figsize=(12, 6))
    sns.barplot(x='channel', y='conversions', hue='model', data=df)
    plt.title('Attributed Conversions by Marketing Channel and Model')
    plt.ylabel('Conversions')
    plt.xlabel('Channel')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('attributed_conversions.png')
    plt.close()

    # 3. ROI Comparison (excluding Direct for visual clarity if needed)
    # Let's keep it but handle inf
    plot_df = df[df['channel'] != 'Direct'].copy()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='channel', y='roi', hue='model', data=plot_df)
    plt.title('Marketing ROI by Channel and Model (Excl. Direct)')
    plt.ylabel('ROI (e.g., 2.0 = 200%)')
    plt.xlabel('Channel')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('marketing_roi.png')
    plt.close()

    print("Visualizations saved as attributed_revenue.png, attributed_conversions.png, and marketing_roi.png")

if __name__ == "__main__":
    create_visualizations()
