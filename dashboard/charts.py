"""
Chart and visualization generation module
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from config.theme import is_dark_theme


def create_dashboard(historical_df, forecast_dates, forecast_values, confidences, anomaly_df):
    """
    Create comprehensive visualization dashboard with dark-mode styling

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

    # Theme-aware colors
    dark = is_dark_theme()

    colors = {
        'historical': '#667eea' if dark else '#7c3aed',
        'anomaly': '#f87171' if dark else '#e11d48',
        'forecast': '#34d399' if dark else '#059669',
        'confidence': 'rgba(52, 211, 153, 0.12)' if dark else 'rgba(5, 150, 105, 0.1)',
        'weekly': '#fbbf24' if dark else '#d97706',
        'inventory': '#a78bfa' if dark else '#7c3aed',
        'text': '#a0aec0' if dark else '#4a2040',
        'text_light': '#8898b9' if dark else '#6b3a5e',
        'grid': 'rgba(100, 126, 234, 0.08)' if dark else 'rgba(236, 72, 153, 0.08)',
        'bar_inactive': 'rgba(100, 126, 234, 0.25)' if dark else 'rgba(236, 72, 153, 0.2)',
        'anomaly_bar_bg': 'rgba(100, 126, 234, 0.25)' if dark else 'rgba(236, 72, 153, 0.15)',
        'fill_inv': 'rgba(167, 139, 250, 0.08)' if dark else 'rgba(124, 58, 237, 0.06)',
    }

    # 1. Main Chart: Historical + Forecast
    normal_data = anomaly_df[~anomaly_df['is_anomaly']]
    fig.add_trace(
        go.Scatter(
            x=normal_data['date'],
            y=normal_data['units_sold'],
            mode='lines',
            name='Historical Sales',
            line=dict(color=colors['historical'], width=2.5),
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
                    size=10,
                    symbol='x',
                    line=dict(width=2, color='rgba(248, 113, 113, 0.5)')
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
            line=dict(color=colors['forecast'], width=3, dash='dash'),
            marker=dict(size=7, symbol='diamond', color=colors['forecast']),
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
    anomaly_colors = [colors['anomaly'] if x else colors['anomaly_bar_bg'] for x in anomaly_df['is_anomaly']]
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

    # 3. Weekly Pattern (using a copy to avoid mutation)
    hist_copy = historical_df.copy()
    hist_copy['day_of_week'] = pd.to_datetime(hist_copy['date']).dt.dayofweek
    weekly = hist_copy.groupby('day_of_week')['units_sold'].mean()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    bar_colors = [colors['weekly'] if i == weekly.idxmax() else colors['bar_inactive'] for i in range(7)]

    fig.add_trace(
        go.Bar(
            x=days,
            y=weekly.values,
            marker_color=bar_colors,
            name='Weekly Pattern',
            text=[f'{v:.0f}' for v in weekly.values],
            textposition='outside',
            textfont=dict(color=colors['text'], size=11),
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
            line=dict(color=colors['inventory'], width=3),
            marker=dict(size=7, color=colors['inventory']),
            fill='tozeroy',
            fillcolor=colors['fill_inv'],
            hovertemplate='<b>%{x}</b><br>Total Demand: %{y:.0f} units<extra></extra>'
        ),
        row=2, col=2
    )

    # Update layout — Theme-aware
    template = 'plotly_dark' if dark else 'plotly_white'
    title_color = '#e2e8f0' if dark else '#1e1b2e'
    legend_bg = 'rgba(15, 20, 40, 0.7)' if dark else 'rgba(255, 255, 255, 0.7)'
    legend_border = 'rgba(100, 126, 234, 0.15)' if dark else 'rgba(236, 72, 153, 0.1)'
    plot_bg = 'rgba(15, 20, 40, 0.3)' if dark else 'rgba(253, 242, 248, 0.2)'

    fig.update_layout(
        height=900,
        showlegend=True,
        template=template,
        font=dict(family="Inter, sans-serif", size=12, color=colors['text']),
        title=dict(
            text="<b>AI-Powered Inventory Intelligence Dashboard</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=22, color=title_color)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor=legend_bg,
            bordercolor=legend_border,
            borderwidth=1,
            font=dict(color=colors['text'])
        ),
        hovermode='x unified',
        plot_bgcolor=plot_bg,
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    # Update subplot title colors
    subtitle_color = '#c8d2e6' if dark else '#4a2040'
    for annotation in fig.layout.annotations:
        annotation.font.color = subtitle_color

    # Update axes — dark grid
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['grid'],
        tickfont=dict(color=colors['text_light']),
        title_font=dict(color=colors['text']),
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['grid'],
        tickfont=dict(color=colors['text_light']),
        title_font=dict(color=colors['text']),
        zeroline=False
    )

    return fig
