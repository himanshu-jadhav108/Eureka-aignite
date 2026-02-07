"""
Advanced inventory optimization module
"""

import numpy as np


def calculate_optimal_inventory(forecast_values, confidences, current_stock, lead_time, 
                                service_level=0.95):
    """
    Advanced inventory optimization with dynamic safety stock
    
    Calculates reorder point, order quantity, and safety stock based on
    forecast demand, lead time, and desired service level.
    
    Args:
        forecast_values: List of forecasted demand values
        confidences: List of confidence intervals
        current_stock: Current inventory level
        lead_time: Supplier lead time in days
        service_level: Target service level (probability of not stocking out)
        
    Returns:
        Dict with inventory recommendations and metrics
    """
    # Calculate demand statistics
    total_demand = sum(forecast_values)
    daily_demand = total_demand / len(forecast_values)
    forecast_std = np.std(forecast_values)
    
    # Lead time demand
    lead_time_demand = daily_demand * lead_time
    lead_time_variance = forecast_std * np.sqrt(lead_time)

    # Calculate z-score for service level
    try:
        from scipy.stats import norm
        z_score = norm.ppf(service_level)
    except:
        z_score = 1.65  # Default for 95% service level

    # Safety stock calculation
    safety_stock = z_score * lead_time_variance

    # Dynamic buffer based on coefficient of variation
    cv = forecast_std / daily_demand if daily_demand > 0 else 0
    dynamic_buffer = max(0.15, min(0.35, cv * 0.5))

    # Reorder point
    reorder_point = lead_time_demand + safety_stock
    stock_position = current_stock

    # Order decision
    if stock_position <= reorder_point:
        # Order enough to cover lead time demand + 1 week buffer
        order_quantity = (reorder_point - stock_position) + (daily_demand * 7)
        should_order = True
    else:
        order_quantity = 0
        should_order = False

    # Days until stockout
    days_until_stockout = round(stock_position / daily_demand, 1) if daily_demand > 0 else 999

    return {
        'reorder_point': round(reorder_point),
        'order_quantity': round(order_quantity),
        'safety_stock': round(safety_stock),
        'should_order': should_order,
        'daily_demand': round(daily_demand, 1),
        'total_forecast': round(total_demand),
        'dynamic_buffer': round(dynamic_buffer * 100),
        'stock_position': stock_position,
        'days_until_stockout': days_until_stockout,
        'confidence_interval': round(np.mean(confidences), 1)
    }
