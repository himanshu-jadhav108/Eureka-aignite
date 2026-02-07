"""
Explainability and business insights generation module
"""

import numpy as np


def generate_insights(product_data, forecast_result, anomaly_data, inventory_rec, accuracy_metrics):
    """
    Generate comprehensive business insights from analysis results
    
    Args:
        product_data: Historical product data
        forecast_result: Forecast values
        anomaly_data: DataFrame with anomaly detection results
        inventory_rec: Inventory recommendations dict
        accuracy_metrics: Model accuracy metrics
        
    Returns:
        List of HTML-formatted insight strings
    """
    insights = []

    # Trend Analysis
    recent_7 = product_data['units_sold'].tail(7).mean()
    prev_7 = product_data['units_sold'].tail(14).head(7).mean()
    trend_change = ((recent_7 - prev_7) / prev_7 * 100) if prev_7 > 0 else 0

    if abs(trend_change) > 15:
        trend_icon = "📈" if trend_change > 0 else "📉"
        badge = "badge-success" if trend_change > 0 else "badge-danger"
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">{trend_icon}</span>'
                       f'<strong>Significant Trend:</strong> Sales changed by '
                       f'<span class="status-badge {badge}">{abs(trend_change):.1f}%</span> '
                       f'{"up" if trend_change > 0 else "down"} compared to previous week</div>')
    else:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">➡️</span>'
                       f'<strong>Stable Trend:</strong> Sales consistent at ~{recent_7:.0f} units/day</div>')

    # Volatility Analysis
    cv = product_data['units_sold'].tail(30).std() / recent_7 if recent_7 > 0 else 0
    if cv > 0.4:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">⚠️</span>'
                       f'<strong>High Volatility</strong> <span class="status-badge badge-warning">CV: {cv:.2f}</span>: '
                       f'Demand unpredictable, {inventory_rec["dynamic_buffer"]}% safety buffer applied</div>')
    elif cv > 0.25:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">📊</span>'
                       f'<strong>Moderate Volatility</strong> <span class="status-badge badge-info">CV: {cv:.2f}</span>: '
                       f'Some demand variation expected</div>')
    else:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">✅</span>'
                       f'<strong>Low Volatility</strong> <span class="status-badge badge-success">CV: {cv:.2f}</span>: '
                       f'Very predictable demand pattern</div>')

    # Anomaly Summary
    anomalies = anomaly_data[anomaly_data['is_anomaly']]
    if len(anomalies) > 0:
        recent_anomalies = anomalies.tail(3)
        dates = recent_anomalies['date'].dt.strftime('%m-%d').tolist()
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">🚨</span>'
                       f'<strong>{len(anomalies)} Anomalies Detected:</strong> Recent unusual activity on '
                       f'{", ".join(dates)}. Review for promotions or stockouts.</div>')
    else:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">✅</span>'
                       f'<strong>No Anomalies:</strong> Sales pattern is normal and predictable</div>')

    # Forecast Accuracy
    if accuracy_metrics and accuracy_metrics.get('mape'):
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">🎯</span>'
                       f'<strong>Forecast Accuracy:</strong> Historical MAPE of '
                       f'<span class="status-badge badge-success">{accuracy_metrics["mape"]:.1f}%</span> '
                       f'(±{inventory_rec["confidence_interval"]} units confidence interval)</div>')

    # Stock Status
    days_left = inventory_rec['days_until_stockout']
    lead_time = inventory_rec.get('lead_time', 7)

    if days_left < lead_time:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">🚨</span>'
                       f'<strong>Critical Stock:</strong> Only <span class="status-badge badge-danger">'
                       f'{days_left} days</span> of inventory left! Order immediately to avoid stockout.</div>')
    elif days_left < lead_time * 2:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">⚠️</span>'
                       f'<strong>Low Stock:</strong> <span class="status-badge badge-warning">{days_left} days</span> '
                       f'remaining. Reorder recommended.</div>')
    else:
        insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">✅</span>'
                       f'<strong>Healthy Stock:</strong> <span class="status-badge badge-success">{days_left} days</span> '
                       f'of coverage available</div>')

    # Seasonality Pattern
    dow_pattern = product_data.groupby(product_data['date'].dt.dayofweek)['units_sold'].mean()
    peak_day = dow_pattern.idxmax()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    insights.append(f'<div class="insight-card fade-in"><span class="insight-icon">📅</span>'
                   f'<strong>Peak Day:</strong> {days[peak_day]} '
                   f'<span class="status-badge badge-info">avg: {dow_pattern[peak_day]:.0f} units</span></div>')

    return insights
