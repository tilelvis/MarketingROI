import pandas as pd
import numpy as np
from datetime import datetime, timedelta

"""
generate_data.py
---------------
Simulates a multi-touch marketing dataset with user journeys across 5 channels.
Each user has multiple touchpoints leading up to a potential conversion.
"""

def generate_marketing_data(num_users=2000, max_touchpoints=10):
    """
    Generates synthetic marketing interaction data.

    Parameters:
    - num_users (int): Number of unique customers to simulate.
    - max_touchpoints (int): Maximum interactions per user journey.

    Returns:
    - pd.DataFrame: The generated marketing dataset.
    """
    np.random.seed(42)

    users = [f'user_{i}' for i in range(num_users)]
    channels = ['Search', 'Social', 'Email', 'Display', 'Direct']
    campaigns = ['Spring_Sale', 'Summer_Promo', 'Fall_Discount', 'Winter_Special', 'Always_On']

    data = []

    for user in users:
        # Each user has a random number of touchpoints before potentially converting
        num_user_interactions = np.random.randint(1, max_touchpoints + 1)
        user_interactions = []
        has_converted = False

        # Random start date within a 60-day window
        start_time = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 60))

        for i in range(num_user_interactions):
            if has_converted:
                break

            channel = np.random.choice(channels)
            campaign = np.random.choice(campaigns)
            timestamp = start_time + timedelta(days=i, hours=np.random.randint(0, 24))

            # Simulated conversion probabilities (e.g., Email is high intent, Display is low)
            base_prob = {'Search': 0.05, 'Social': 0.03, 'Email': 0.08, 'Display': 0.02, 'Direct': 0.04}
            # Multi-touch effect: probability increases slightly with each subsequent touchpoint
            prob = base_prob[channel] * (1 + 0.15 * i)

            conversion = 1 if np.random.random() < prob else 0
            # Higher revenue for high-intent channels (Search, Direct)
            revenue_base = {'Search': 120, 'Social': 80, 'Email': 100, 'Display': 70, 'Direct': 110}
            revenue = round(np.random.normal(revenue_base[channel], 30), 2) if conversion == 1 else 0
            revenue = max(0, revenue) # Ensure revenue is positive

            user_interactions.append([user, timestamp, channel, campaign, conversion, revenue])

            if conversion == 1:
                has_converted = True

        data.extend(user_interactions)

    df = pd.DataFrame(data, columns=['user_id', 'timestamp', 'channel', 'campaign', 'conversion', 'revenue'])
    df = df.sort_values(['user_id', 'timestamp'])

    # Save to CSV
    df.to_csv('marketing_data.csv', index=False)
    print(f"Dataset generated: {len(df)} touchpoints for {num_users} users saved to marketing_data.csv")
    return df

if __name__ == "__main__":
    generate_marketing_data()
