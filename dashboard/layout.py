"""
Dashboard layout and UI components
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from dashboard.metrics import create_metric_card
from dashboard.charts import create_dashboard


def render_header():
    """Render the application header"""
    st.markdown('<p class="main-header fade-in">🧠 Smart Inventory AI Pro</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Enterprise-Grade Demand Forecasting & Inventory Optimization '
        '<span class="feature-tag">AI-Powered</span></p>', 
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)


def render_sidebar():
    """
    Render sidebar with all configuration options
    
    Returns:
        Dict with all configuration values
    """
    st.sidebar.markdown("## ⚙️ Configuration Panel")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    # Data source
    data_source = st.sidebar.radio(
        "📂 Data Source:",
        ["📊 AI-Generated Sample", "📁 Upload Custom CSV"],
        help="Choose between demo data or upload your own sales history"
    )

    uploaded_file = None
    if data_source == "📁 Upload Custom CSV":
        uploaded_file = st.sidebar.file_uploader(
            "Choose CSV file", 
            type=['csv'],
            help="Upload a CSV with columns: date, product_id, units_sold"
        )
        if uploaded_file is None:
            st.markdown("""
            <div class="insight-card">
                <h3>📋 Required CSV Format</h3>
                <p>Your file must include these columns:</p>
            </div>
            """, unsafe_allow_html=True)
            st.code("""date,product_id,units_sold
2024-01-01,PROD001,45
2024-01-02,PROD001,52
2024-01-03,PROD001,48""")

    # Product selection
    from utils.data_loader import load_and_validate_data
    temp_df = load_and_validate_data(uploaded_file)
    
    if temp_df is None:
        return {'uploaded_file': None}
    
    products = sorted(temp_df['product_id'].unique())
    st.sidebar.markdown("### 🏷️ Product Selection")
    selected_product = st.sidebar.selectbox(
        "Choose Product:",
        products,
        help=f"Select from {len(products)} available products"
    )

    # Forecast configuration
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("### 🔮 Forecast Configuration")
    
    forecast_days = st.sidebar.slider(
        "Forecast Horizon (days):",
        min_value=7,
        max_value=30,
        value=14,
        help="Number of days to forecast ahead"
    )
    
    service_level = st.sidebar.slider(
        "Service Level Target:",
        min_value=0.80,
        max_value=0.99,
        value=0.95,
        step=0.01,
        format="%.2f",
        help="Probability of not stocking out (95% = industry standard)"
    )

    # Inventory parameters
    st.sidebar.markdown("### 📦 Inventory Parameters")
    
    current_stock = st.sidebar.number_input(
        "Current Stock Level:",
        min_value=0,
        max_value=100000,
        value=100,
        step=10,
        help="Current units in inventory"
    )
    
    lead_time = st.sidebar.number_input(
        "Supplier Lead Time (days):",
        min_value=1,
        max_value=90,
        value=7,
        help="Days until new stock arrives after ordering"
    )

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    # Run Analysis Button
    analyze_button = st.sidebar.button(
        "🚀 Run Advanced Analysis",
        type="primary",
        use_container_width=True
    )

    return {
        'uploaded_file': uploaded_file,
        'selected_product': selected_product,
        'products': products,
        'forecast_days': forecast_days,
        'service_level': service_level,
        'current_stock': current_stock,
        'lead_time': lead_time,
        'analyze_button': analyze_button
    }


def render_welcome_screen(df, products):
    """Render welcome screen with data overview"""
    st.markdown("## 👋 Welcome to Smart Inventory AI Pro", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card fade-in">
        <h3>🚀 Get Started</h3>
        <p>Configure your settings in the sidebar and click <strong>"Run Advanced Analysis"</strong> to:</p>
        <ul>
            <li>📈 Generate AI-powered demand forecasts</li>
            <li>🔍 Detect anomalies and unusual patterns</li>
            <li>📦 Optimize inventory levels</li>
            <li>💡 Receive actionable business insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Data Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Total Records",
            f"{len(df):,}",
            icon="📊"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Products",
            f"{df['product_id'].nunique()}",
            icon="🏷️"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Date Range",
            f"{(df['date'].max() - df['date'].min()).days} days",
            icon="📅"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Avg Daily Sales",
            f"{df['units_sold'].mean():.0f}",
            icon="📈"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Data Preview
    st.markdown("### 📋 Data Preview", unsafe_allow_html=True)
    st.dataframe(
        df.head(20).style.background_gradient(cmap='Blues', subset=['units_sold']),
        use_container_width=True,
        height=400
    )

    # Quick Trend Visualization
    st.markdown("### 📊 Product Trends Overview", unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for i, prod in enumerate(products[:5]):  # Show top 5 products
        prod_data = df[df['product_id'] == prod]
        fig.add_trace(go.Scatter(
            x=prod_data['date'],
            y=prod_data['units_sold'],
            mode='lines',
            name=prod,
            line=dict(width=2),
            hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>Sales: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Feature Highlights
    st.markdown("### ✨ Key Features", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-card">
            <h4>🤖 AI Ensemble Forecasting</h4>
            <p>Combines multiple algorithms (EWMA, Linear Regression, Seasonal Patterns) for superior accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4>🔍 Advanced Anomaly Detection</h4>
            <p>Multi-method approach using statistical and IQR-based techniques</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-card">
            <h4>📊 Dynamic Safety Stock</h4>
            <p>Adapts to demand volatility with intelligent buffer calculation</p>
        </div>
        """, unsafe_allow_html=True)


def render_results(product_data, forecast_dates, forecast_values, confidences, 
                   anomaly_df, inventory, insights, accuracy, config):
    """Render analysis results"""
    st.markdown("## 📊 Analysis Results", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Top Metrics
    render_top_metrics(product_data, forecast_values, anomaly_df, inventory, config)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Recommendation Box
    render_recommendation_box(inventory, config)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = create_dashboard(product_data, forecast_dates, forecast_values, confidences, anomaly_df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Business Insights
    render_business_insights(insights)

    # Detailed Data
    render_detailed_data(forecast_dates, forecast_values, confidences, accuracy)

    # Export Options
    render_export_options(forecast_dates, forecast_values, confidences, insights, config)


def render_top_metrics(product_data, forecast_values, anomaly_df, inventory, config):
    """Render top-level metric cards"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    recent_avg = product_data['units_sold'].tail(7).mean()
    prev_avg = product_data['units_sold'].tail(14).head(7).mean()
    trend_delta = ((recent_avg - prev_avg) / prev_avg * 100) if prev_avg > 0 else 0
    
    with col1:
        st.markdown(create_metric_card(
            "Current Stock",
            f"{config['current_stock']:,}",
            icon="📦"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "7-Day Forecast",
            f"{sum(forecast_values[:7]):,.0f}",
            delta=trend_delta,
            icon="📈"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Anomalies",
            f"{anomaly_df['is_anomaly'].sum()}",
            icon="⚠️"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Daily Demand",
            f"{inventory['daily_demand']:.1f}",
            icon="📊"
        ), unsafe_allow_html=True)
    
    with col5:
        days_color = "🚨" if inventory['days_until_stockout'] < config['lead_time'] else "✅"
        st.markdown(create_metric_card(
            "Days to Stockout",
            f"{inventory['days_until_stockout']:.0f}",
            icon=days_color
        ), unsafe_allow_html=True)


def render_recommendation_box(inventory, config):
    """Render inventory recommendation box"""
    if inventory['should_order']:
        if inventory['days_until_stockout'] < config['lead_time']:
            st.markdown(f"""
            <div class="critical-box fade-in">
                <div class="recommendation-title">🚨 CRITICAL: IMMEDIATE ACTION REQUIRED</div>
                <div class="recommendation-value">{inventory['order_quantity']:,}</div>
                <div style="font-size: 1.5rem; margin-bottom: 1rem;">UNITS TO ORDER NOW</div>
                <div class="recommendation-details">
                    ⚡ <strong>Urgency:</strong> Only {inventory['days_until_stockout']:.0f} days of stock remaining<br>
                    📊 <strong>Reorder Point:</strong> {inventory['reorder_point']:,} units<br>
                    🛡️ <strong>Safety Stock:</strong> {inventory['safety_stock']:,} units ({inventory['dynamic_buffer']}% buffer)<br>
                    📈 <strong>Forecast Demand:</strong> {inventory['total_forecast']:,} units over {config['forecast_days']} days<br>
                    🎯 <strong>Service Level:</strong> {config['service_level']*100:.0f}% (Industry Standard)<br>
                    ⏱️ <strong>Lead Time:</strong> {config['lead_time']} days
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="recommendation-box fade-in">
                <div class="recommendation-title">📦 RESTOCKING RECOMMENDED</div>
                <div class="recommendation-value">{inventory['order_quantity']:,}</div>
                <div style="font-size: 1.5rem; margin-bottom: 1rem;">UNITS TO ORDER</div>
                <div class="recommendation-details">
                    ✅ <strong>Stock Status:</strong> {inventory['days_until_stockout']:.0f} days remaining<br>
                    📊 <strong>Reorder Point:</strong> {inventory['reorder_point']:,} units<br>
                    🛡️ <strong>Safety Stock:</strong> {inventory['safety_stock']:,} units ({inventory['dynamic_buffer']}% buffer)<br>
                    📈 <strong>Forecast Demand:</strong> {inventory['total_forecast']:,} units over {config['forecast_days']} days<br>
                    🎯 <strong>Service Level:</strong> {config['service_level']*100:.0f}% confidence<br>
                    ⏱️ <strong>Lead Time:</strong> {config['lead_time']} days
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="safe-box fade-in">
            <div class="recommendation-title">✅ INVENTORY LEVEL OPTIMAL</div>
            <div class="recommendation-value">NO ORDER NEEDED</div>
            <div class="recommendation-details">
                🎯 <strong>Stock Coverage:</strong> {inventory['days_until_stockout']:.0f} days<br>
                📊 <strong>Current Position:</strong> {config['current_stock']:,} units<br>
                📈 <strong>Daily Demand:</strong> {inventory['daily_demand']:.1f} units<br>
                🛡️ <strong>Reorder Point:</strong> {inventory['reorder_point']:,} units<br>
                ✅ <strong>Status:</strong> Well above reorder threshold
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_business_insights(insights):
    """Render business insights section"""
    st.markdown("## 💡 AI-Generated Business Insights", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    for insight in insights:
        st.markdown(insight, unsafe_allow_html=True)


def render_detailed_data(forecast_dates, forecast_values, confidences, accuracy):
    """Render detailed forecast data in expander"""
    with st.expander("🔍 **View Detailed Forecast Data & Model Performance**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Forecast Table")
            forecast_df = pd.DataFrame({
                'Date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
                'Forecast': [round(v) for v in forecast_values],
                'Lower Bound': [round(max(0, v - c)) for v, c in zip(forecast_values, confidences)],
                'Upper Bound': [round(v + c) for v, c in zip(forecast_values, confidences)],
                'Confidence (±)': [round(c) for c in confidences]
            })
            st.dataframe(forecast_df, use_container_width=True, height=400)
        
        with col2:
            st.markdown("### 🎯 Model Performance")
            if accuracy:
                st.metric("Mean Absolute Error (MAE)", f"{accuracy['mae']:.2f} units")
                st.metric("Mean Absolute % Error (MAPE)", f"{accuracy['mape']:.2f}%")
                
                # Accuracy interpretation
                if accuracy['mape'] < 10:
                    acc_status = "🟢 Excellent"
                elif accuracy['mape'] < 20:
                    acc_status = "🟡 Good"
                else:
                    acc_status = "🔴 Fair"
                
                st.markdown(f"**Accuracy Rating:** {acc_status}")
                
                # Comparison chart
                comp_df = pd.DataFrame({
                    'Actual': accuracy['actual'],
                    'Predicted': accuracy['predicted']
                })
                st.line_chart(comp_df, use_container_width=True)
            else:
                st.info("Insufficient data for accuracy calculation (need 30+ days)")


def render_export_options(forecast_dates, forecast_values, confidences, insights, config):
    """Render export options"""
    st.markdown("## 📥 Export Options", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    # Prepare forecast CSV
    forecast_df = pd.DataFrame({
        'Date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
        'Forecast': [round(v) for v in forecast_values],
        'Lower Bound': [round(max(0, v - c)) for v, c in zip(forecast_values, confidences)],
        'Upper Bound': [round(v + c) for v, c in zip(forecast_values, confidences)],
        'Confidence (±)': [round(c) for c in confidences]
    })
    
    with col1:
        forecast_csv = forecast_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Forecast CSV",
            data=forecast_csv,
            file_name=f"forecast_{config['selected_product']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        insights_text = "\n\n".join([insight.replace('<div class="insight-card fade-in">', '').replace('</div>', '') for insight in insights])
        st.download_button(
            label="💡 Download Insights",
            data=insights_text,
            file_name=f"insights_{config['selected_product']}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col3:
        st.markdown("📧 **Email Report** *(Coming Soon)*")
