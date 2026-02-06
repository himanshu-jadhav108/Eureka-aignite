"""
🏆 ULTIMATE SMART INVENTORY TRACKER
Hybrid AI-Powered Demand Forecasting & Inventory Optimization System
Combines the best of app.py and app2.py with enterprise-grade features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION & THEME
# ============================================================

st.set_page_config(
    page_title="Smart Inventory AI Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #1E3A8A; }
    .recommendation-box { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                          padding: 30px; border-radius: 15px; color: white; 
                          box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
    .critical-box { background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); 
                    padding: 30px; border-radius: 15px; color: white; 
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
    .safe-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 30px; border-radius: 15px; color: white; 
                 box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 1. DATA GENERATION & LOADING
# ============================================================

def generate_sample_data(days=120, num_products=5):
    """Generate realistic sales data with multiple patterns"""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    products = [f'PROD-{str(i).zfill(3)}' for i in range(1, num_products + 1)]

    data = []
    for i, product in enumerate(products):
        base = 30 + (i * 20) + np.random.randint(-5, 5)

        if i % 3 == 0:
            trend = np.linspace(0, 30, days)
        elif i % 3 == 1:
            trend = np.linspace(20, -10, days)
        else:
            trend = np.zeros(days)

        seasonality = 10 * np.sin(np.linspace(0, 8*np.pi, days))
        monthly = 5 * np.sin(np.linspace(0, 4*np.pi, days))
        noise = np.random.normal(0, 3, days)

        anomalies = np.zeros(days)
        anomaly_days = np.random.choice(days, size=3, replace=False)
        for day in anomaly_days:
            anomalies[day] = np.random.choice([-20, 25])

        units_sold = base + trend + seasonality + monthly + noise + anomalies
        units_sold = np.maximum(units_sold, 0).astype(int)

        for j, date in enumerate(dates):
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'product_id': product,
                'units_sold': units_sold[j]
            })

    return pd.DataFrame(data)


def load_and_validate_data(uploaded_file=None):
    """Load data from upload or generate sample"""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None
    else:
        df = generate_sample_data()
        st.sidebar.info("📊 Using generated sample data")

    required_cols = ['date', 'product_id', 'units_sold']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"❌ Missing required columns: {', '.join(missing)}")
        return None

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce').fillna(0)
    df = df.sort_values('date').reset_index(drop=True)

    return df

# ============================================================
# 2. ADVANCED FORECASTING ENGINE
# ============================================================

class ForecastingEngine:
    def __init__(self, data):
        self.data = data.copy()
        self.data['day_index'] = range(len(self.data))

    def ewma_forecast(self, span=14):
        """Exponential Weighted Moving Average"""
        return self.data['units_sold'].ewm(span=span, adjust=False).mean()

    def linear_trend(self):
        """Linear regression trend"""
        X = self.data[['day_index']].values
        y = self.data['units_sold'].values
        model = LinearRegression()
        model.fit(X, y)
        return model, model.predict(X)

    def seasonal_pattern(self):
        """Weekly seasonality"""
        self.data['day_of_week'] = pd.to_datetime(self.data['date']).dt.dayofweek
        pattern = self.data.groupby('day_of_week')['units_sold'].mean()
        return pattern / pattern.mean()

    def ensemble_forecast(self, forecast_days=14):
        """Combine multiple methods for robust forecasting"""
        ewma = self.ewma_forecast()
        model, linear_pred = self.linear_trend()
        seasonal = self.seasonal_pattern()

        recent_data = self.data.tail(14)
        recent_avg = recent_data['units_sold'].mean()
        recent_trend = (recent_data['units_sold'].iloc[-1] - recent_data['units_sold'].iloc[0]) / 14

        last_date = pd.to_datetime(self.data['date'].max())
        forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]

        forecasts = []
        confidences = []

        for i, date in enumerate(forecast_dates):
            day_idx = len(self.data) + i
            day_of_week = date.dayofweek

            linear_future = model.predict([[day_idx]])[0]
            ewma_future = recent_avg + (recent_trend * i)
            seasonal_factor = seasonal[day_of_week]
            seasonal_future = recent_avg * seasonal_factor

            ensemble = (0.3 * linear_future + 0.4 * ewma_future + 0.3 * seasonal_future)
            ensemble = max(0, ensemble)

            historical_std = self.data['units_sold'].tail(30).std()
            confidence = 1.96 * historical_std

            forecasts.append(ensemble)
            confidences.append(confidence)

        return forecast_dates, forecasts, confidences

    def calculate_accuracy(self):
        """Calculate model accuracy on recent data"""
        if len(self.data) < 30:
            return None

        train = self.data[:-7]
        test = self.data[-7:]

        if len(train) < 14:
            return None

        train_engine = ForecastingEngine(train)
        _, pred, _ = train_engine.ensemble_forecast(forecast_days=7)
        actual = test['units_sold'].values

        mae = mean_absolute_error(actual, pred)
        mape = np.mean(np.abs((actual - pred) / actual)) * 100 if np.all(actual > 0) else None

        return {'mae': mae, 'mape': mape, 'actual': actual, 'predicted': pred}

# ============================================================
# 3. ANOMALY DETECTION
# ============================================================

def detect_anomalies_advanced(data, window=7, std_threshold=2):
    """Advanced anomaly detection with multiple methods"""
    df = data.copy()

    df['rolling_mean'] = df['units_sold'].rolling(window=window, min_periods=1).mean()
    df['rolling_std'] = df['units_sold'].rolling(window=window, min_periods=1).std().fillna(0)

    df['upper_bound'] = df['rolling_mean'] + (std_threshold * df['rolling_std'])
    df['lower_bound'] = df['rolling_mean'] - (std_threshold * df['rolling_std'])

    Q1 = df['units_sold'].quantile(0.25)
    Q3 = df['units_sold'].quantile(0.75)
    IQR = Q3 - Q1
    iqr_upper = Q3 + 1.5 * IQR
    iqr_lower = Q1 - 1.5 * IQR

    df['is_anomaly'] = (
        (df['units_sold'] > df['upper_bound']) | 
        (df['units_sold'] < df['lower_bound']) |
        (df['units_sold'] > iqr_upper) |
        (df['units_sold'] < iqr_lower)
    )

    df['anomaly_severity'] = np.where(
        df['is_anomaly'],
        np.abs(df['units_sold'] - df['rolling_mean']) / (df['rolling_std'] + 1),
        0
    )

    return df

# ============================================================
# 4. INVENTORY OPTIMIZATION
# ============================================================

def calculate_optimal_inventory(forecast_values, confidences, current_stock, lead_time, 
                                service_level=0.95):
    """Advanced inventory optimization"""
    total_demand = sum(forecast_values)
    daily_demand = total_demand / len(forecast_values)

    forecast_std = np.std(forecast_values)
    lead_time_demand = daily_demand * lead_time
    lead_time_variance = forecast_std * np.sqrt(lead_time)

    try:
        from scipy.stats import norm
        z_score = norm.ppf(service_level)
    except:
        z_score = 1.65  # Default for 95% service level

    safety_stock = z_score * lead_time_variance

    cv = forecast_std / daily_demand if daily_demand > 0 else 0
    dynamic_buffer = max(0.15, min(0.35, cv * 0.5))

    reorder_point = lead_time_demand + safety_stock
    stock_position = current_stock

    if stock_position <= reorder_point:
        order_quantity = (reorder_point - stock_position) + (daily_demand * 7)
        should_order = True
    else:
        order_quantity = 0
        should_order = False

    return {
        'reorder_point': round(reorder_point),
        'order_quantity': round(order_quantity),
        'safety_stock': round(safety_stock),
        'should_order': should_order,
        'daily_demand': round(daily_demand, 1),
        'total_forecast': round(total_demand),
        'dynamic_buffer': round(dynamic_buffer * 100),
        'stock_position': stock_position,
        'days_until_stockout': round(stock_position / daily_demand, 1) if daily_demand > 0 else 999,
        'confidence_interval': round(np.mean(confidences), 1)
    }

# ============================================================
# 5. EXPLAINABILITY ENGINE
# ============================================================

def generate_insights(product_data, forecast_result, anomaly_data, inventory_rec, accuracy_metrics):
    """Generate comprehensive business insights"""
    insights = []

    recent_7 = product_data['units_sold'].tail(7).mean()
    prev_7 = product_data['units_sold'].tail(14).head(7).mean()
    trend_change = ((recent_7 - prev_7) / prev_7 * 100) if prev_7 > 0 else 0

    if abs(trend_change) > 15:
        trend_icon = "📈" if trend_change > 0 else "📉"
        insights.append(f"{trend_icon} **Significant Trend**: Sales changed by {abs(trend_change):.1f}% "
                       f"({'up' if trend_change > 0 else 'down'}) compared to previous week")
    else:
        insights.append(f"➡️ **Stable Trend**: Sales consistent at ~{recent_7:.0f} units/day")

    cv = product_data['units_sold'].tail(30).std() / recent_7 if recent_7 > 0 else 0
    if cv > 0.4:
        insights.append(f"⚠️ **High Volatility** (CV: {cv:.2f}): Demand unpredictable, "
                       f"{inventory_rec['dynamic_buffer']}% safety buffer applied")
    elif cv > 0.25:
        insights.append(f"📊 **Moderate Volatility** (CV: {cv:.2f}): Some demand variation expected")
    else:
        insights.append(f"✅ **Low Volatility** (CV: {cv:.2f}): Very predictable demand pattern")

    anomalies = anomaly_data[anomaly_data['is_anomaly']]
    if len(anomalies) > 0:
        recent_anomalies = anomalies.tail(3)
        dates = recent_anomalies['date'].dt.strftime('%m-%d').tolist()
        insights.append(f"🚨 **{len(anomalies)} Anomalies Detected**: Recent unusual activity on "
                       f"{', '.join(dates)}. Review for promotions or stockouts.")
    else:
        insights.append(f"✅ **No Anomalies**: Sales pattern is normal and predictable")

    if accuracy_metrics and accuracy_metrics.get('mape'):
        insights.append(f"🎯 **Forecast Accuracy**: Historical MAPE of {accuracy_metrics['mape']:.1f}% "
                       f"(±{inventory_rec['confidence_interval']} units confidence interval)")

    days_left = inventory_rec['days_until_stockout']
    lead_time = inventory_rec.get('lead_time', 7)

    if days_left < lead_time:
        insights.append(f"🚨 **Critical Stock**: Only {days_left} days of inventory left! "
                       f"Order immediately to avoid stockout.")
    elif days_left < lead_time * 2:
        insights.append(f"⚠️ **Low Stock**: {days_left} days remaining. Reorder recommended.")
    else:
        insights.append(f"✅ **Healthy Stock**: {days_left} days of coverage available")

    dow_pattern = product_data.groupby(product_data['date'].dt.dayofweek)['units_sold'].mean()
    peak_day = dow_pattern.idxmax()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    insights.append(f"📅 **Peak Day**: {days[peak_day]} (avg: {dow_pattern[peak_day]:.0f} units)")

    return insights

# ============================================================
# 6. VISUALIZATION DASHBOARD
# ============================================================

def create_dashboard(historical_df, forecast_dates, forecast_values, confidences, anomaly_df):
    """Create comprehensive visualization dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Sales History & Forecast', 'Anomaly Detection', 
                       'Weekly Pattern', 'Inventory Projection'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )

    # 1. Main Chart: Historical + Forecast
    normal_data = anomaly_df[~anomaly_df['is_anomaly']]
    fig.add_trace(
        go.Scatter(x=normal_data['date'], y=normal_data['units_sold'],
                  mode='lines', name='Historical', line=dict(color='#2E86AB', width=2)),
        row=1, col=1
    )

    anomaly_data = anomaly_df[anomaly_df['is_anomaly']]
    if len(anomaly_data) > 0:
        fig.add_trace(
            go.Scatter(x=anomaly_data['date'], y=anomaly_data['units_sold'],
                      mode='markers', name='Anomalies',
                      marker=dict(color='#E63946', size=10, symbol='x')),
            row=1, col=1
        )

    fig.add_trace(
        go.Scatter(x=forecast_dates, y=forecast_values,
                  mode='lines', name='Forecast',
                  line=dict(color='#06D6A0', width=3, dash='dash')),
        row=1, col=1
    )

    upper = [f + c for f, c in zip(forecast_values, confidences)]
    lower = [max(0, f - c) for f, c in zip(forecast_values, confidences)]
    fig.add_trace(
        go.Scatter(x=forecast_dates + forecast_dates[::-1],
                  y=upper + lower[::-1],
                  fill='toself', fillcolor='rgba(6, 214, 160, 0.2)',
                  line=dict(color='rgba(255,255,255,0)'),
                  name='Confidence Interval', showlegend=True),
        row=1, col=1
    )

    # 2. Anomaly Timeline
    fig.add_trace(
        go.Bar(x=anomaly_df['date'], y=anomaly_df['anomaly_severity'],
               marker_color=['#E63946' if x else '#A8DADC' for x in anomaly_df['is_anomaly']],
               name='Anomaly Score'),
        row=1, col=2
    )

    # 3. Weekly Pattern
    historical_df['day_of_week'] = pd.to_datetime(historical_df['date']).dt.dayofweek
    weekly = historical_df.groupby('day_of_week')['units_sold'].mean()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig.add_trace(
        go.Bar(x=days, y=weekly.values, marker_color='#457B9D', name='Weekly Pattern'),
        row=2, col=1
    )

    # 4. Inventory Projection
    cumulative_demand = np.cumsum(forecast_values)
    fig.add_trace(
        go.Scatter(x=forecast_dates, y=cumulative_demand,
                  mode='lines', name='Cumulative Demand',
                  line=dict(color='#F4A261', width=3)),
        row=2, col=2
    )

    fig.update_layout(height=800, showlegend=True, template='plotly_white',
                     title_text="Inventory Intelligence Dashboard", title_x=0.5)

    return fig

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    # Header
    st.markdown('<p class="main-header">🧠 Smart Inventory AI Pro</p>', unsafe_allow_html=True)
    st.markdown("### Enterprise-grade demand forecasting & inventory optimization")
    st.markdown("---")

    # Sidebar
    st.sidebar.header("⚙️ Configuration")

    # Data source
    data_source = st.sidebar.radio("Data Source:", ["📊 Sample Data", "📁 Upload CSV"])

    uploaded_file = None
    if data_source == "📁 Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Choose CSV file", type=['csv'])
        if uploaded_file is None:
            st.info("👈 Please upload a CSV file with columns: date, product_id, units_sold")
            st.code("""date,product_id,units_sold
2024-01-01,PROD001,45
2024-01-02,PROD001,52
2024-01-03,PROD001,48""")
            return

    # Load data
    df = load_and_validate_data(uploaded_file)
    if df is None:
        return

    # Product selection
    products = sorted(df['product_id'].unique())
    selected_product = st.sidebar.selectbox("Select Product:", products)

    # Configuration
    st.sidebar.markdown("---")
    st.sidebar.subheader("Forecast Settings")
    forecast_days = st.sidebar.slider("Forecast Days:", 7, 30, 14)
    service_level = st.sidebar.slider("Service Level:", 0.80, 0.99, 0.95, 0.01)

    st.sidebar.subheader("Inventory Settings")
    current_stock = st.sidebar.number_input("Current Stock:", 0, 10000, 100)
    lead_time = st.sidebar.number_input("Lead Time (days):", 1, 30, 7)

    # Filter product data
    product_data = df[df['product_id'] == selected_product].copy()

    if len(product_data) < 14:
        st.error("❌ Insufficient data (minimum 14 days required)")
        return

    # Run Analysis
    if st.sidebar.button("🚀 Run Advanced Analysis", type="primary"):

        with st.spinner("🔍 Analyzing data with ensemble forecasting..."):

            # Initialize engine
            engine = ForecastingEngine(product_data)

            # Generate forecast
            forecast_dates, forecast_values, confidences = engine.ensemble_forecast(forecast_days)

            # Detect anomalies
            anomaly_df = detect_anomalies_advanced(product_data)

            # Calculate accuracy
            accuracy = engine.calculate_accuracy()

            # Inventory recommendation
            inventory = calculate_optimal_inventory(
                forecast_values, confidences, current_stock, lead_time, service_level
            )
            inventory['lead_time'] = lead_time

            # Generate insights
            insights = generate_insights(product_data, forecast_values, anomaly_df, inventory, accuracy)

        # Display Results

        # Top Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        metrics = [
            ("📦 Current Stock", f"{current_stock}"),
            ("📈 7-Day Forecast", f"{sum(forecast_values[:7]):.0f}"),
            ("⚠️ Anomalies", f"{anomaly_df['is_anomaly'].sum()}"),
            ("📊 Daily Avg", f"{inventory['daily_demand']}"),
            ("⏱️ Stockout In", f"{inventory['days_until_stockout']} days")
        ]

        for col, (label, value) in zip([col1, col2, col3, col4, col5], metrics):
            with col:
                st.metric(label, value)

        st.markdown("---")

        # Main Recommendation Box
        if inventory['should_order']:
            if inventory['days_until_stockout'] < lead_time:
                box_class = "critical-box"
                urgency = "🚨 CRITICAL: ORDER NOW"
            else:
                box_class = "recommendation-box"
                urgency = "📦 ORDER RECOMMENDED"

            st.markdown(f"""
            <div class="{box_class}">
                <h2 style="margin-top: 0;">{urgency}</h2>
                <h1 style="font-size: 4rem; margin: 10px 0;">{inventory['order_quantity']} units</h1>
                <p style="font-size: 1.2rem;">
                    Reorder Point: {inventory['reorder_point']} units | 
                    Safety Stock: {inventory['safety_stock']} units ({inventory['dynamic_buffer']}% buffer)<br>
                    Expected demand: {inventory['total_forecast']} units over {forecast_days} days
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-box">
                <h2 style="margin-top: 0;">✅ NO ORDER NEEDED</h2>
                <h1 style="font-size: 3rem;">Stock Level Optimal</h1>
                <p>Current stock sufficient for {inventory['days_until_stockout']} days</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # Dashboard
        fig = create_dashboard(product_data, forecast_dates, forecast_values, confidences, anomaly_df)
        st.plotly_chart(fig, use_container_width=True)

        # Insights
        st.subheader("📋 Business Intelligence Insights")
        for insight in insights:
            st.markdown(insight)

        # Detailed Data
        with st.expander("🔍 View Detailed Forecast Data"):
            forecast_df = pd.DataFrame({
                'Date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
                'Forecast': [round(v) for v in forecast_values],
                'Lower Bound': [round(max(0, v - c)) for v, c in zip(forecast_values, confidences)],
                'Upper Bound': [round(v + c) for v, c in zip(forecast_values, confidences)]
            })
            st.dataframe(forecast_df, use_container_width=True)

            if accuracy:
                st.markdown(f"**Model Accuracy (Backtest):** MAE = {accuracy['mae']:.2f}, MAPE = {accuracy['mape']:.2f}%")

    else:
        # Preview mode
        st.info("👆 Configure settings and click 'Run Advanced Analysis'")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Products", df['product_id'].nunique())
        with col3:
            st.metric("Date Range", f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")

        st.subheader("📊 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Quick chart
        fig = go.Figure()
        for prod in products[:3]:
            prod_data = df[df['product_id'] == prod]
            fig.add_trace(go.Scatter(x=prod_data['date'], y=prod_data['units_sold'],
                           mode='lines', name=prod))
        fig.update_layout(title="Sample Product Trends", height=400)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
