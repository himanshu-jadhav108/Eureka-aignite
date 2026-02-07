"""
Advanced anomaly detection module
"""

import numpy as np


def detect_anomalies_advanced(data, window=7, std_threshold=2):
    """
    Advanced anomaly detection with multiple methods
    
    Combines statistical methods (rolling mean/std) with IQR-based detection
    
    Args:
        data: DataFrame with 'units_sold' column
        window: Rolling window size for statistical analysis
        std_threshold: Number of standard deviations for outlier detection
        
    Returns:
        DataFrame with anomaly flags and severity scores
    """
    df = data.copy()

    # Statistical method: Rolling mean and standard deviation
    df['rolling_mean'] = df['units_sold'].rolling(window=window, min_periods=1).mean()
    df['rolling_std'] = df['units_sold'].rolling(window=window, min_periods=1).std().fillna(0)

    # Calculate bounds
    df['upper_bound'] = df['rolling_mean'] + (std_threshold * df['rolling_std'])
    df['lower_bound'] = df['rolling_mean'] - (std_threshold * df['rolling_std'])

    # IQR method
    Q1 = df['units_sold'].quantile(0.25)
    Q3 = df['units_sold'].quantile(0.75)
    IQR = Q3 - Q1
    iqr_upper = Q3 + 1.5 * IQR
    iqr_lower = Q1 - 1.5 * IQR

    # Combined anomaly detection
    df['is_anomaly'] = (
        (df['units_sold'] > df['upper_bound']) | 
        (df['units_sold'] < df['lower_bound']) |
        (df['units_sold'] > iqr_upper) |
        (df['units_sold'] < iqr_lower)
    )

    # Calculate anomaly severity
    df['anomaly_severity'] = np.where(
        df['is_anomaly'],
        np.abs(df['units_sold'] - df['rolling_mean']) / (df['rolling_std'] + 1),
        0
    )

    return df
