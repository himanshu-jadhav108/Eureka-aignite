"""
🏆 ULTIMATE SMART INVENTORY TRACKER - PREMIUM UI EDITION
Hybrid AI-Powered Demand Forecasting & Inventory Optimization System
Enhanced with modern, professional frontend design
"""

import streamlit as st
from datetime import datetime
import time

from config.theme import apply_theme
from data.sample_generator import generate_sample_data
from utils.data_loader import load_and_validate_data
from models.forecasting import ForecastingEngine
from models.anomaly import detect_anomalies_advanced
from models.inventory import calculate_optimal_inventory
from models.explainability import generate_insights
from dashboard.charts import create_dashboard
from dashboard.metrics import create_metric_card
from dashboard.layout import render_header, render_sidebar, render_welcome_screen, render_results
from PIL import Image

# Centered Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.sidebar.image("assets/sia_logo.jpeg", width=200)

def initialize_session_state():
    """Initialize session state variables"""
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None


def main():
    logo = Image.open("assets/sia_logo.jpeg")

    st.set_page_config(
        page_title="SIA – Smart Inventory AI",
        page_icon=logo,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_theme()
    initialize_session_state()

    render_header()

    config = render_sidebar()

    with st.spinner("🔄 Loading and validating data..."):
        df = load_and_validate_data(config['uploaded_file'])

    if df is None:
        return

    product_data = df[df['product_id'] == config['selected_product']].copy()

    if len(product_data) < 14:
        st.error("❌ **Insufficient Data**: Minimum 14 days of history required for accurate forecasting")
        return

    # If analyze button clicked → run and STORE results
    if config['analyze_button']:
        run_analysis(product_data, config, df)

    # If already analyzed → show stored results
    if st.session_state.analysis_done and st.session_state.analysis_results:
        render_results(**st.session_state.analysis_results)

    # Otherwise show welcome
    if not st.session_state.analysis_done:
        render_welcome_screen(df, config['products'])


def run_analysis(product_data, config, df):
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("🔧 Initializing AI forecasting engine...")
        progress_bar.progress(20)
        engine = ForecastingEngine(product_data)

        status_text.text("🔮 Generating ensemble predictions...")
        progress_bar.progress(40)
        forecast_dates, forecast_values, confidences = engine.ensemble_forecast(config['forecast_days'])

        status_text.text("🔍 Detecting anomalies...")
        progress_bar.progress(60)
        anomaly_df = detect_anomalies_advanced(product_data)

        status_text.text("📊 Calculating model accuracy...")
        progress_bar.progress(75)
        accuracy = engine.calculate_accuracy()

        status_text.text("🎯 Optimizing inventory levels...")
        progress_bar.progress(90)
        inventory = calculate_optimal_inventory(
            forecast_values,
            confidences,
            config['current_stock'],
            config['lead_time'],
            config['service_level']
        )
        inventory['lead_time'] = config['lead_time']

        status_text.text("💡 Generating business insights...")
        progress_bar.progress(95)
        insights = generate_insights(product_data, forecast_values, anomaly_df, inventory, accuracy)

        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")

        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        # 🔥 STORE EVERYTHING IN SESSION STATE
        st.session_state.analysis_results = {
            "product_data": product_data,
            "forecast_dates": forecast_dates,
            "forecast_values": forecast_values,
            "confidences": confidences,
            "anomaly_df": anomaly_df,
            "inventory": inventory,
            "insights": insights,
            "accuracy": accuracy,
            "config": config
        }

        st.session_state.analysis_done = True

    except Exception as e:
        st.error(f"❌ **Analysis Error:** {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
