"""
Theme configuration and CSS styling for the application
"""

import streamlit as st


def apply_theme():
    """Apply premium custom CSS theme to the application"""
    st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: #ffffff;
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Header Styles */
    .main-header {
        color: #667eea;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #475569;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #475569;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
        margin: 0;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 0.25rem;
    }
    
    /* Recommendation Boxes */
    .recommendation-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .critical-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 20px 40px rgba(239, 68, 68, 0.3);
        margin: 2rem 0;
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .safe-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        margin: 2rem 0;
    }
    
    .recommendation-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .recommendation-value {
        font-size: 4.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .recommendation-details {
        font-size: 1.1rem;
        line-height: 1.8;
        opacity: 0.95;
    }
    
    /* Insight Cards */
    .insight-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .insight-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    /* Progress Bars */
    .progress-container {
        background: #e2e8f0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 1s ease;
    }
    
    /* Data Table Styles */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Charts Container */
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin: 1.5rem 0;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* Info/Warning/Error Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #667eea;
        font-weight: 600;
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Feature Tag */
    .feature-tag {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    /* Glassmorphism Effect */
    .glass {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
    }
    
    /* Additional Visibility Improvements */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
    }
    
    p, span, div {
        color: #334155;
    }
    
    .stMarkdown {
        color: #334155;
    }
    
    /* Improve expander visibility */
    .streamlit-expanderHeader p {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    /* Info boxes */
    .stAlert p {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)
