# Marketing Attribution & ROI Analysis Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, end-to-end data science pipeline for analyzing marketing campaign performance. This project integrates SQL-based attribution modeling with Python-driven ROI analysis and professional data visualization.

| Tech Stack | Tools Used |
| :--- | :--- |
| **Language** | Python 3.x |
| **Data Manipulation** | Pandas, NumPy |
| **Database** | SQLite, SQL Window Functions |
| **Visualization** | Seaborn, Matplotlib |
| **Workflow** | Modular Python Pipeline |

---

## Project Overview

In multi-channel marketing, understanding the true value of each touchpoint is critical. This project implements and compares three fundamental attribution models:

- **First-Click Attribution**: Assigns 100% of conversion credit to the initial customer touchpoint.
- **Last-Click Attribution**: Credits the final interaction immediately preceding the conversion.
- **Linear Attribution**: Distributes credit equally across all touchpoints in the customer journey.

The pipeline further extends these results by incorporating channel-specific cost structures to calculate **Return on Investment (ROI)** for each model.

## Key Insights (Simulation Results)

Based on the generated marketing dataset (~10,000 touchpoints):

- **High-Intent Closing**: The **Email** channel consistently shows the highest conversion volume in the **Last-Click** model, indicating its strength as a high-intent conversion closer.
- **Upper-Funnel Efficiency**: **Display** advertising shows significantly higher ROI in the **Linear** and **First-Click** models compared to Last-Click, suggesting it plays a vital role in awareness and assisted conversions.
- **Profitability Leaders**: **Email** and **Display** maintain the strongest ROI ratios across all models, while **Search** represents the largest total investment with steady, reliable returns.
- **Direct Traffic Value**: **Direct** interactions remain a major contributor to revenue with zero direct acquisition cost, highlighting the importance of brand equity.

## Dataset Simulation

This project uses a custom-built synthetic dataset engine (`generate_data.py`) to simulate realistic multi-touch customer journeys.
- **Scale**: 2,000 unique users and ~10,000+ total marketing touchpoints.
- **Channels**: Search, Social, Email, Display, and Direct Traffic.
- **Dynamics**: Incorporates varying conversion probabilities per channel and a "multi-touch boost" where subsequent interactions increase conversion likelihood.

---

## Visualizations

### 1. Attributed Revenue by Model
*Bar chart comparing revenue attribution across First-Click, Last-Click, and Linear models for each channel.*

![Attributed Revenue by Model](attributed_revenue.png)

### 2. Attributed Conversions
*Distribution of total conversion counts (or shares) across marketing channels based on different attribution logic.*

![Attributed Conversions by Model](attributed_conversions.png)

### 3. Marketing ROI (Return on Investment)
*ROI comparison per channel across models (excluding Direct traffic due to zero-cost skew).*

![Marketing ROI by Channel and Model](marketing_roi.png)

---

## Repository Structure

- `main.py`: Master orchestration script to run the full pipeline.
- `generate_data.py`: Synthetic marketing data generator (~10k rows).
- `setup_db.py`: Database creation and data ingestion using SQLite.
- `attribution_queries.py`: SQL-based attribution modeling logic.
- `calculate_roi.py`: Cost-integration and ROI calculation engine.
- `visualize_results.py`: Professional chart generation.

## How to Run

1. **Clone the repository**.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the full analysis**:
   ```bash
   python main.py
   ```

## Future Improvements
- **Time-Decay Attribution**: Implement models that give more credit to touchpoints closer in time to the conversion.
- **Markov Chain Modeling**: Add a data-driven, probabilistic attribution model.
- **Real-World Integration**: Connect to Google Analytics 4 (GA4) or BigQuery APIs for live data analysis.
- **Streamlit Dashboard**: Develop an interactive web interface to explore attribution shifts in real-time.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
