"""
Advanced forecasting engine with ensemble methods
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')


class ForecastingEngine:
    """Advanced forecasting engine with multiple methods"""
    
    def __init__(self, data):
        """
        Initialize forecasting engine
        
        Args:
            data: DataFrame with 'date' and 'units_sold' columns
        """
        self.data = data.copy()
        self.data['day_index'] = range(len(self.data))

    def ewma_forecast(self, span=14):
        """
        Exponential Weighted Moving Average
        
        Args:
            span: Smoothing span
            
        Returns:
            Series of EWMA values
        """
        return self.data['units_sold'].ewm(span=span, adjust=False).mean()

    def linear_trend(self):
        """
        Linear regression trend
        
        Returns:
            Tuple of (model, predictions)
        """
        X = self.data[['day_index']].values
        y = self.data['units_sold'].values
        model = LinearRegression()
        model.fit(X, y)
        return model, model.predict(X)

    def seasonal_pattern(self):
        """
        Weekly seasonality pattern
        
        Returns:
            Series with normalized seasonal factors by day of week
        """
        self.data['day_of_week'] = pd.to_datetime(self.data['date']).dt.dayofweek
        pattern = self.data.groupby('day_of_week')['units_sold'].mean()
        return pattern / pattern.mean()

    def ensemble_forecast(self, forecast_days=14):
        """
        Combine multiple methods for robust forecasting
        
        Args:
            forecast_days: Number of days to forecast
            
        Returns:
            Tuple of (forecast_dates, forecast_values, confidences)
        """
        # Get component forecasts
        ewma = self.ewma_forecast()
        model, linear_pred = self.linear_trend()
        seasonal = self.seasonal_pattern()

        # Calculate recent trends
        recent_data = self.data.tail(14)
        recent_avg = recent_data['units_sold'].mean()
        recent_trend = (recent_data['units_sold'].iloc[-1] - recent_data['units_sold'].iloc[0]) / 14

        # Generate forecast dates
        last_date = pd.to_datetime(self.data['date'].max())
        forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]

        forecasts = []
        confidences = []

        for i, date in enumerate(forecast_dates):
            day_idx = len(self.data) + i
            day_of_week = date.dayofweek

            # Linear projection
            linear_future = model.predict([[day_idx]])[0]
            
            # EWMA projection
            ewma_future = recent_avg + (recent_trend * i)
            
            # Seasonal adjustment
            seasonal_factor = seasonal[day_of_week]
            seasonal_future = recent_avg * seasonal_factor

            # Ensemble combination (weighted average)
            ensemble = (0.3 * linear_future + 0.4 * ewma_future + 0.3 * seasonal_future)
            ensemble = max(0, ensemble)

            # Confidence interval
            historical_std = self.data['units_sold'].tail(30).std()
            confidence = 1.96 * historical_std

            forecasts.append(ensemble)
            confidences.append(confidence)

        return forecast_dates, forecasts, confidences

    def calculate_accuracy(self):
        """
        Calculate model accuracy on recent data using walk-forward validation
        
        Returns:
            Dict with mae, mape, actual, and predicted values or None
        """
        if len(self.data) < 30:
            return None

        # Split data: train on all but last 7 days, test on last 7
        train = self.data[:-7]
        test = self.data[-7:]

        if len(train) < 14:
            return None

        # Train model on training data
        train_engine = ForecastingEngine(train)
        _, pred, _ = train_engine.ensemble_forecast(forecast_days=7)
        actual = test['units_sold'].values

        # Calculate metrics
        mae = mean_absolute_error(actual, pred)
        mape = np.mean(np.abs((actual - pred) / actual)) * 100 if np.all(actual > 0) else None

        return {
            'mae': mae, 
            'mape': mape, 
            'actual': actual, 
            'predicted': pred
        }
