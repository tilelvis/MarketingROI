import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_marketing_data(num_users=1000, num_interactions=5000):
    np.random.seed(42)

    users = [f'user_{i}' for i in range(num_users)]
    channels = ['Search', 'Social', 'Email', 'Display', 'Direct']
    campaigns = ['Spring_Sale', 'Summer_Promo', 'Fall_Discount', 'Winter_Special', 'Always_On']

    data = []

    for user in users:
        # Each user has a random number of touchpoints before potentially converting
        num_user_interactions = np.random.randint(1, 10)
        user_interactions = []
        has_converted = False

        start_time = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 60))

        for i in range(num_user_interactions):
            if has_converted:
                break

            channel = np.random.choice(channels)
            campaign = np.random.choice(campaigns)
            timestamp = start_time + timedelta(days=i, hours=np.random.randint(0, 24))

            # Probability of conversion increases slightly with more touchpoints
            base_prob = {'Search': 0.05, 'Social': 0.02, 'Email': 0.08, 'Display': 0.01, 'Direct': 0.03}
            prob = base_prob[channel] * (1 + 0.1 * i)

            conversion = 1 if np.random.random() < prob else 0
            revenue = round(np.random.uniform(50, 200), 2) if conversion == 1 else 0

            user_interactions.append([user, timestamp, channel, campaign, conversion, revenue])

            if conversion == 1:
                has_converted = True

        data.extend(user_interactions)

    df = pd.DataFrame(data, columns=['user_id', 'timestamp', 'channel', 'campaign', 'conversion', 'revenue'])
    df = df.sort_values(['user_id', 'timestamp'])

    # Save to CSV
    df.to_csv('marketing_data.csv', index=False)
    print("Dataset generated and saved to marketing_data.csv")
    return df

if __name__ == "__main__":
    generate_marketing_data()
