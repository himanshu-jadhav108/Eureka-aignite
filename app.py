"""
Smart Inventory Tracker MVP
A hackathon-ready inventory forecasting and restocking recommendation tool
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta
from sklearn.linear_model import LinearRegression

# ============================================================
# 1. DATA LOADING & PREPROCESSING
# ============================================================

def load_data(uploaded_file):
    """
    Load CSV data from uploaded file
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        pd.DataFrame: Raw dataframe
    """
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


def preprocess_data(df):
    """
    Clean and prepare data for analysis
    
    - Convert date to datetime
    - Handle missing values
    - Sort by date
    - Validate required columns
    
    Args:
        df: Raw dataframe
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    # Validate columns
    required_cols = ['date', 'product_id', 'units_sold']
    if not all(col in df.columns for col in required_cols):
        st.error(f"Missing required columns. Need: {required_cols}")
        return None
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Convert date column
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    
    # Drop rows with invalid dates
    df_clean = df_clean.dropna(subset=['date'])
    
    # Fill missing units_sold with 0
    df_clean['units_sold'] = df_clean['units_sold'].fillna(0)
    
    # Sort by date
    df_clean = df_clean.sort_values('date').reset_index(drop=True)
    
    return df_clean


# ============================================================
# 2. DEMAND FORECASTING
# ============================================================

def forecast_demand(df, product_id, forecast_days=7):
    """
    Forecast demand using Linear Regression
    Simple, reliable, and explainable approach
    
    Args:
        df: Preprocessed dataframe
        product_id: Product to forecast
        forecast_days: Number of days to forecast (default 7)
    
    Returns:
        dict: {
            'forecast_dates': list of dates,
            'forecast_values': list of predicted values,
            'total_demand': sum of forecasted demand,
            'trend': 'increasing'|'decreasing'|'stable'
        }
    """
    # Filter for specific product
    product_df = df[df['product_id'] == product_id].copy()
    
    if len(product_df) < 7:
        st.warning("Not enough historical data (need at least 7 days)")
        return None
    
    # Prepare features: day index as X
    product_df['day_index'] = range(len(product_df))
    X = product_df[['day_index']].values
    y = product_df['units_sold'].values
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate forecast
    last_day_index = product_df['day_index'].max()
    last_date = product_df['date'].max()
    
    future_indices = np.array([[last_day_index + i] for i in range(1, forecast_days + 1)])
    forecast_values = model.predict(future_indices)
    
    # Ensure non-negative forecasts
    forecast_values = np.maximum(forecast_values, 0)
    
    # Generate forecast dates
    forecast_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
    
    # Determine trend
    slope = model.coef_[0]
    if slope > 1:
        trend = 'increasing'
    elif slope < -1:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    return {
        'forecast_dates': forecast_dates,
        'forecast_values': forecast_values.tolist(),
        'total_demand': sum(forecast_values),
        'trend': trend,
        'slope': slope
    }


# ============================================================
# 3. ANOMALY DETECTION
# ============================================================

def detect_anomalies(df, product_id, window=7, std_threshold=2):
    """
    Detect unusual spikes or drops using rolling statistics
    
    Args:
        df: Preprocessed dataframe
        product_id: Product to analyze
        window: Rolling window size (default 7 days)
        std_threshold: Number of std deviations for anomaly (default 2)
    
    Returns:
        pd.DataFrame: Original data with anomaly flags
    """
    # Filter for specific product
    product_df = df[df['product_id'] == product_id].copy()
    
    # Calculate rolling statistics
    product_df['rolling_mean'] = product_df['units_sold'].rolling(window=window, min_periods=1).mean()
    product_df['rolling_std'] = product_df['units_sold'].rolling(window=window, min_periods=1).std()
    
    # Fill NaN std with 0 to avoid errors
    product_df['rolling_std'] = product_df['rolling_std'].fillna(0)
    
    # Detect anomalies: points beyond threshold
    product_df['upper_bound'] = product_df['rolling_mean'] + (std_threshold * product_df['rolling_std'])
    product_df['lower_bound'] = product_df['rolling_mean'] - (std_threshold * product_df['rolling_std'])
    
    product_df['is_anomaly'] = (
        (product_df['units_sold'] > product_df['upper_bound']) |
        (product_df['units_sold'] < product_df['lower_bound'])
    )
    
    return product_df


# ============================================================
# 4. RESTOCKING RECOMMENDATION
# ============================================================

def recommend_restock(current_stock, forecast_total, lead_time, safety_factor=1.2):
    """
    Calculate recommended reorder quantity
    
    Logic:
    - Expected demand during lead time = (forecast_total / 7) * lead_time
    - Safety stock = expected demand * safety_factor
    - Reorder quantity = max(0, expected demand + safety stock - current stock)
    
    Args:
        current_stock: Current inventory level
        forecast_total: Total forecasted demand (7 days)
        lead_time: Days until new stock arrives
        safety_factor: Multiplier for safety buffer (default 1.2 = 20% buffer)
    
    Returns:
        dict: {
            'reorder_quantity': units to order,
            'expected_demand': demand during lead time,
            'safety_stock': buffer amount,
            'should_reorder': boolean
        }
    """
    # Calculate daily demand rate
    daily_demand = forecast_total / 7
    
    # Expected demand during lead time
    expected_demand = daily_demand * lead_time
    
    # Safety stock (buffer)
    safety_stock = expected_demand * (safety_factor - 1)
    
    # Total needed
    total_needed = expected_demand + safety_stock
    
    # Reorder quantity
    reorder_quantity = max(0, total_needed - current_stock)
    
    # Should we reorder?
    should_reorder = reorder_quantity > 0
    
    return {
        'reorder_quantity': round(reorder_quantity),
        'expected_demand': round(expected_demand),
        'safety_stock': round(safety_stock),
        'should_reorder': should_reorder,
        'daily_demand': round(daily_demand, 1)
    }


# ============================================================
# 5. EXPLAINABILITY LAYER
# ============================================================

def generate_explanation(forecast_result, anomaly_df, restock_result):
    """
    Generate plain-English explanation of the analysis
    
    Args:
        forecast_result: Dict from forecast_demand()
        anomaly_df: DataFrame from detect_anomalies()
        restock_result: Dict from recommend_restock()
    
    Returns:
        str: Human-readable explanation
    """
    explanation = []
    
    # Trend explanation
    trend = forecast_result['trend']
    slope = forecast_result['slope']
    
    if trend == 'increasing':
        explanation.append(f"📈 **Demand Trend**: Your sales are increasing at a rate of approximately {abs(slope):.1f} units per day.")
    elif trend == 'decreasing':
        explanation.append(f"📉 **Demand Trend**: Your sales are decreasing at a rate of approximately {abs(slope):.1f} units per day.")
    else:
        explanation.append(f"➡️ **Demand Trend**: Your sales are relatively stable with minimal day-to-day variation.")
    
    # Anomaly explanation
    num_anomalies = anomaly_df['is_anomaly'].sum()
    if num_anomalies > 0:
        recent_anomalies = anomaly_df[anomaly_df['is_anomaly']].tail(3)
        anomaly_dates = recent_anomalies['date'].dt.strftime('%Y-%m-%d').tolist()
        explanation.append(f"⚠️ **Anomalies Detected**: {num_anomalies} unusual sales events found. Most recent: {', '.join(anomaly_dates)}. These could indicate promotions, stockouts, or external events.")
    else:
        explanation.append(f"✅ **No Anomalies**: Sales patterns are consistent with no unusual spikes or drops.")
    
    # Forecast explanation
    total_demand = round(forecast_result['total_demand'])
    explanation.append(f"🔮 **7-Day Forecast**: Expected to sell approximately **{total_demand} units** over the next week.")
    
    # Restocking explanation
    if restock_result['should_reorder']:
        explanation.append(f"📦 **Restocking Recommendation**: Order **{restock_result['reorder_quantity']} units** to maintain adequate stock during the lead time and safety buffer.")
        explanation.append(f"   - Expected demand during lead time: {restock_result['expected_demand']} units")
        explanation.append(f"   - Safety buffer: {restock_result['safety_stock']} units")
    else:
        explanation.append(f"✅ **No Reorder Needed**: Your current stock is sufficient to cover expected demand plus safety buffer.")
    
    return "\n\n".join(explanation)


# ============================================================
# 6. VISUALIZATION
# ============================================================

def create_visualization(historical_df, forecast_result, anomaly_df):
    """
    Create interactive Plotly chart showing historical data, forecast, and anomalies
    
    Args:
        historical_df: Historical sales data
        forecast_result: Forecast results dict
        anomaly_df: Data with anomaly flags
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    # Historical sales (normal points)
    normal_data = anomaly_df[~anomaly_df['is_anomaly']]
    fig.add_trace(go.Scatter(
        x=normal_data['date'],
        y=normal_data['units_sold'],
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='#2E86AB', width=2),
        marker=dict(size=6)
    ))
    
    # Anomalies
    anomaly_data = anomaly_df[anomaly_df['is_anomaly']]
    if len(anomaly_data) > 0:
        fig.add_trace(go.Scatter(
            x=anomaly_data['date'],
            y=anomaly_data['units_sold'],
            mode='markers',
            name='Anomalies',
            marker=dict(color='#E63946', size=12, symbol='x')
        ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_result['forecast_dates'],
        y=forecast_result['forecast_values'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#06D6A0', width=2, dash='dash'),
        marker=dict(size=8, symbol='diamond')
    ))
    
    # Layout
    fig.update_layout(
        title='Sales History & 7-Day Demand Forecast',
        xaxis_title='Date',
        yaxis_title='Units Sold',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


# ============================================================
# 7. STREAMLIT APP (MAIN)
# ============================================================

def main():
    """
    Main Streamlit application
    """
    # Page config
    st.set_page_config(
        page_title="Smart Inventory Tracker",
        page_icon="📦",
        layout="wide"
    )
    
    # Title and description
    st.title("📦 Smart Inventory Tracker")
    st.markdown("**AI-powered demand forecasting and restocking recommendations for small retail businesses**")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Sales Data (CSV)",
        type=['csv'],
        help="CSV must contain: date, product_id, units_sold"
    )
    
    # Show sample data info
    st.sidebar.info("**Need sample data?** Download sample_sales_data.csv from the project folder")
    
    # Check if file is uploaded
    if uploaded_file is None:
        st.info("👈 Please upload a CSV file to get started")
        st.markdown("### Expected CSV Format")
        st.code("""date,product_id,units_sold
2024-01-01,PROD001,45
2024-01-02,PROD001,52
2024-01-03,PROD001,48
...""")
        return
    
    # Load and preprocess data
    with st.spinner("Loading data..."):
        df_raw = load_data(uploaded_file)
        if df_raw is None:
            return
        
        df = preprocess_data(df_raw)
        if df is None:
            return
    
    # Product selection
    products = df['product_id'].unique().tolist()
    selected_product = st.sidebar.selectbox(
        "Select Product",
        options=products,
        index=0
    )
    
    # User inputs
    current_stock = st.sidebar.number_input(
        "Current Stock Level",
        min_value=0,
        value=100,
        step=10,
        help="How many units do you currently have in stock?"
    )
    
    lead_time = st.sidebar.number_input(
        "Lead Time (days)",
        min_value=1,
        max_value=30,
        value=7,
        help="How many days until new stock arrives?"
    )
    
    st.sidebar.markdown("---")
    
    # Run analysis button
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        
        with st.spinner("Analyzing data..."):
            
            # 1. Forecast demand
            forecast_result = forecast_demand(df, selected_product, forecast_days=7)
            if forecast_result is None:
                return
            
            # 2. Detect anomalies
            anomaly_df = detect_anomalies(df, selected_product)
            
            # 3. Recommend restocking
            restock_result = recommend_restock(
                current_stock=current_stock,
                forecast_total=forecast_result['total_demand'],
                lead_time=lead_time
            )
            
            # 4. Generate explanation
            explanation = generate_explanation(forecast_result, anomaly_df, restock_result)
            
            # 5. Create visualization
            fig = create_visualization(df[df['product_id'] == selected_product], forecast_result, anomaly_df)
        
        # Display results
        st.success("✅ Analysis Complete!")
        
        # Main visualization
        st.plotly_chart(fig, use_container_width=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="7-Day Forecast",
                value=f"{round(forecast_result['total_demand'])} units"
            )
        
        with col2:
            st.metric(
                label="Daily Demand",
                value=f"{restock_result['daily_demand']} units/day"
            )
        
        with col3:
            st.metric(
                label="Anomalies Detected",
                value=anomaly_df['is_anomaly'].sum()
            )
        
        with col4:
            reorder_qty = restock_result['reorder_quantity']
            st.metric(
                label="Recommended Reorder",
                value=f"{reorder_qty} units",
                delta="Order Now" if reorder_qty > 0 else "Stock OK",
                delta_color="inverse" if reorder_qty > 0 else "normal"
            )
        
        st.markdown("---")
        
        # Explanation section
        st.subheader("📊 Analysis Insights")
        st.markdown(explanation)
        
        # Additional details (collapsible)
        with st.expander("🔍 View Detailed Data"):
            st.markdown("### Forecast Details")
            forecast_df = pd.DataFrame({
                'Date': forecast_result['forecast_dates'],
                'Forecasted Demand': [round(v) for v in forecast_result['forecast_values']]
            })
            st.dataframe(forecast_df, use_container_width=True)
            
            st.markdown("### Recent Sales with Anomaly Flags")
            display_df = anomaly_df[['date', 'units_sold', 'is_anomaly']].tail(14).copy()
            display_df.columns = ['Date', 'Units Sold', 'Anomaly']
            st.dataframe(display_df, use_container_width=True)
    
    else:
        st.info("👆 Configure your settings and click 'Run Analysis' to generate insights")
        
        # Show data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.markdown(f"**Total records:** {len(df)} | **Date range:** {df['date'].min().date()} to {df['date'].max().date()}")


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    main()
