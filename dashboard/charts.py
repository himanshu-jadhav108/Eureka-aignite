"""
Chart and visualization generation module
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def create_dashboard(historical_df, forecast_dates, forecast_values, confidences, anomaly_df):
    """
    Create comprehensive visualization dashboard with premium styling
    
    Args:
        historical_df: Historical sales data
        forecast_dates: List of forecast dates
        forecast_values: List of forecast values
        confidences: List of confidence intervals
        anomaly_df: DataFrame with anomaly detection results
        
    Returns:
        Plotly figure object
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('📊 Sales History & AI Forecast', '🔍 Anomaly Detection Timeline', 
                       '📅 Weekly Demand Pattern', '📦 Inventory Projection'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )

    # Color scheme
    colors = {
        'historical': '#667eea',
        'anomaly': '#ef4444',
        'forecast': '#10b981',
        'confidence': 'rgba(16, 185, 129, 0.15)',
        'weekly': '#f59e0b',
        'inventory': '#8b5cf6'
    }

    # 1. Main Chart: Historical + Forecast
    normal_data = anomaly_df[~anomaly_df['is_anomaly']]
    fig.add_trace(
        go.Scatter(
            x=normal_data['date'], 
            y=normal_data['units_sold'],
            mode='lines', 
            name='Historical Sales', 
            line=dict(color=colors['historical'], width=3),
            hovertemplate='<b>%{x}</b><br>Sales: %{y} units<extra></extra>'
        ),
        row=1, col=1
    )

    # Add anomalies
    anomaly_data = anomaly_df[anomaly_df['is_anomaly']]
    if len(anomaly_data) > 0:
        fig.add_trace(
            go.Scatter(
                x=anomaly_data['date'], 
                y=anomaly_data['units_sold'],
                mode='markers', 
                name='Anomalies',
                marker=dict(
                    color=colors['anomaly'], 
                    size=12, 
                    symbol='x',
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>ANOMALY</b><br>Date: %{x}<br>Sales: %{y} units<extra></extra>'
            ),
            row=1, col=1
        )

    # Add forecast
    fig.add_trace(
        go.Scatter(
            x=forecast_dates, 
            y=forecast_values,
            mode='lines+markers', 
            name='AI Forecast',
            line=dict(color=colors['forecast'], width=4, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
            hovertemplate='<b>FORECAST</b><br>%{x}<br>Predicted: %{y} units<extra></extra>'
        ),
        row=1, col=1
    )

    # Confidence interval
    upper = [f + c for f, c in zip(forecast_values, confidences)]
    lower = [max(0, f - c) for f, c in zip(forecast_values, confidences)]
    fig.add_trace(
        go.Scatter(
            x=forecast_dates + forecast_dates[::-1],
            y=upper + lower[::-1],
            fill='toself', 
            fillcolor=colors['confidence'],
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence', 
            showlegend=True,
            hoverinfo='skip'
        ),
        row=1, col=1
    )

    # 2. Anomaly Timeline
    anomaly_colors = [colors['anomaly'] if x else '#cbd5e1' for x in anomaly_df['is_anomaly']]
    fig.add_trace(
        go.Bar(
            x=anomaly_df['date'], 
            y=anomaly_df['anomaly_severity'],
            marker_color=anomaly_colors,
            name='Anomaly Score',
            hovertemplate='<b>%{x}</b><br>Severity: %{y:.2f}<extra></extra>'
        ),
        row=1, col=2
    )

    # 3. Weekly Pattern
    historical_df['day_of_week'] = pd.to_datetime(historical_df['date']).dt.dayofweek
    weekly = historical_df.groupby('day_of_week')['units_sold'].mean()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    bar_colors = [colors['weekly'] if i == weekly.idxmax() else '#94a3b8' for i in range(7)]
    
    fig.add_trace(
        go.Bar(
            x=days, 
            y=weekly.values, 
            marker_color=bar_colors,
            name='Weekly Pattern',
            text=[f'{v:.0f}' for v in weekly.values],
            textposition='outside',
            textfont=dict(color="#1e293b", size=12),
            hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f} units<extra></extra>'
        ),
        row=2, col=1
    )

    # 4. Inventory Projection
    cumulative_demand = np.cumsum(forecast_values)
    fig.add_trace(
        go.Scatter(
            x=forecast_dates, 
            y=cumulative_demand,
            mode='lines+markers', 
            name='Cumulative Demand',
            line=dict(color=colors['inventory'], width=4),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)',
            hovertemplate='<b>%{x}</b><br>Total Demand: %{y:.0f} units<extra></extra>'
        ),
        row=2, col=2
    )

    # Update layout with premium styling
    fig.update_layout(
        height=900,
        showlegend=True,
        template='plotly_white',
        font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
        title=dict(
            text="<b>AI-Powered Inventory Intelligence Dashboard</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=24, color='#1e293b')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(248, 250, 252, 0.5)',
        paper_bgcolor='white'
    )

    # Update axes
    fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(203, 213, 225, 0.3)',
    tickfont=dict(color="#1e293b"),
    title_font=dict(color="#1e293b")
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(203, 213, 225, 0.3)',
        tickfont=dict(color="#1e293b"),
        title_font=dict(color="#1e293b")
    )
    return fig

