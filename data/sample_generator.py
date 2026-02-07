"""
Sample data generation module for demo purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime


def generate_sample_data(days=120, num_products=5):
    """
    Generate realistic sales data with multiple patterns
    
    Args:
        days: Number of days of historical data
        num_products: Number of products to generate
        
    Returns:
        DataFrame with columns: date, product_id, units_sold
    """
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    products = [f'PROD-{str(i).zfill(3)}' for i in range(1, num_products + 1)]

    data = []
    for i, product in enumerate(products):
        base = 30 + (i * 20) + np.random.randint(-5, 5)

        # Apply different trends to different products
        if i % 3 == 0:
            trend = np.linspace(0, 30, days)
        elif i % 3 == 1:
            trend = np.linspace(20, -10, days)
        else:
            trend = np.zeros(days)

        # Seasonal patterns
        seasonality = 10 * np.sin(np.linspace(0, 8*np.pi, days))
        monthly = 5 * np.sin(np.linspace(0, 4*np.pi, days))
        noise = np.random.normal(0, 3, days)

        # Add random anomalies
        anomalies = np.zeros(days)
        anomaly_days = np.random.choice(days, size=3, replace=False)
        for day in anomaly_days:
            anomalies[day] = np.random.choice([-20, 25])

        # Calculate final values
        units_sold = base + trend + seasonality + monthly + noise + anomalies
        units_sold = np.maximum(units_sold, 0).astype(int)

        # Create records
        for j, date in enumerate(dates):
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'product_id': product,
                'units_sold': units_sold[j]
            })

    return pd.DataFrame(data)
