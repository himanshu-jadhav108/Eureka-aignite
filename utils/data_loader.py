"""
Data loading and validation utilities
"""

import streamlit as st
import pandas as pd
from data.sample_generator import generate_sample_data


def load_and_validate_data(uploaded_file=None):
    """
    Load data from upload or generate sample data
    
    Args:
        uploaded_file: Streamlit uploaded file object or None
        
    Returns:
        DataFrame with validated data or None on error
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None
    else:
        df = generate_sample_data()
        st.sidebar.info("📊 Using AI-generated sample data")

    # Validate required columns
    required_cols = ['date', 'product_id', 'units_sold']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"❌ Missing required columns: {', '.join(missing)}")
        return None

    # Clean and validate data
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce').fillna(0)
    df = df.sort_values('date').reset_index(drop=True)

    return df
