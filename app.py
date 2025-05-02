import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, mean_absolute_error, precision_score, recall_score, f1_score
import yfinance as yf
import joblib
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.inspection import permutation_importance
import io
import base64
from PIL import Image
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, SVC
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.figure_factory as ff

# Page configuration
st.set_page_config(
    page_title="MLmadeEasy",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with hyper-vibrant pixel art theme
st.markdown("""
    <style>
    /* Import Pixel Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=Orbitron:wght@400;500;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'VT323', monospace;
        letter-spacing: 1px;
    }
    
    /* Fix scrolling */
    .main {
        overflow-y: auto;
        height: 100vh;
    }
    
    .stApp {
        overflow-y: auto;
        height: 100vh;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        overflow-y: auto;
    }
    
    /* Sidebar scrolling */
    .css-1d391kg {
        overflow-y: auto;
        height: 100vh;
    }
    
    /* Color Variables */
    :root {
        --neon-pink: #ff00ff;
        --neon-blue: #00ffff;
        --neon-yellow: #ffff00;
        --neon-green: #00ff00;
        --neon-orange: #ff6600;
        --neon-purple: #9900ff;
        --neon-red: #ff0000;
    }
    
    /* Main container with animated background */
    .main {
        background: #000000;
        position: relative;
        overflow-y: auto;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(45deg, rgba(255, 0, 255, 0.1) 25%, transparent 25%),
            linear-gradient(-45deg, rgba(0, 255, 255, 0.1) 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, rgba(255, 255, 0, 0.1) 75%),
            linear-gradient(-45deg, transparent 75%, rgba(0, 255, 0, 0.1) 75%);
        background-size: 20px 20px;
        animation: background-scroll 20s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes background-scroll {
        0% { background-position: 0 0; }
        100% { background-position: 40px 40px; }
    }
    
    /* Pixel Art Headings with Glow */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Press Start 2P', cursive;
        color: var(--neon-pink);
        text-shadow: 
            0 0 5px var(--neon-pink),
            0 0 10px var(--neon-pink),
            0 0 20px var(--neon-pink),
            0 0 40px var(--neon-pink);
        position: relative;
        display: inline-block;
        animation: text-glow 2s infinite alternate;
    }
    
    @keyframes text-glow {
        0% { text-shadow: 0 0 5px var(--neon-pink); }
        100% { text-shadow: 0 0 20px var(--neon-pink), 0 0 30px var(--neon-pink); }
    }
    
    /* Sidebar styling with animated gradient */
    .css-1d391kg {
        background: #000000;
        border-right: 4px solid var(--neon-pink);
        box-shadow: 0 0 20px var(--neon-pink);
        position: relative;
        overflow: hidden;
    }
    
    .css-1d391kg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            45deg,
            var(--neon-pink) 0%,
            var(--neon-blue) 25%,
            var(--neon-yellow) 50%,
            var(--neon-green) 75%,
            var(--neon-purple) 100%
        );
        opacity: 0.1;
        animation: gradient-shift 10s ease infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Custom card styling with pixel border */
    .card {
        background: rgba(0, 0, 0, 0.8);
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 20px var(--neon-pink);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        width: 100%;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* Grid container for cards */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        width: 100%;
        margin: 20px 0;
    }
    
    /* Card content styling */
    .card-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 15px;
    }
    
    /* Card header styling */
    .card-header {
        width: 100%;
        padding: 10px;
        border-bottom: 2px solid var(--neon-pink);
        margin-bottom: 15px;
    }
    
    /* Card footer styling */
    .card-footer {
        width: 100%;
        padding: 10px;
        border-top: 2px solid var(--neon-pink);
        margin-top: 15px;
    }
    
    /* Metric card styling */
    .metric-card {
        background: rgba(0, 0, 0, 0.8);
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 0 20px var(--neon-pink);
        min-width: 200px;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    /* Feature card styling */
    .feature-card {
        background: rgba(0, 0, 0, 0.8);
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 0 20px var(--neon-pink);
        min-width: 250px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    /* Model card styling */
    .model-card {
        background: rgba(0, 0, 0, 0.8);
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 0 20px var(--neon-pink);
        min-width: 300px;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    /* Visualization card styling */
    .viz-card {
        background: rgba(0, 0, 0, 0.8);
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 0 20px var(--neon-pink);
        width: 100%;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* Responsive grid adjustments */
    @media (max-width: 768px) {
        .card-grid {
            grid-template-columns: 1fr;
        }
        
        .metric-card, .feature-card, .model-card {
            min-width: 100%;
            margin: 10px 0;
        }
    }
    
    /* Button styling with bounce effect */
    .stButton button {
        background: #000000;
        color: var(--neon-pink);
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 12px 24px;
        font-family: 'Press Start 2P', cursive;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 10px var(--neon-pink);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        animation: button-pulse 2s infinite;
    }
    
    @keyframes button-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stButton button:hover {
        background: var(--neon-pink);
        color: #000000;
        box-shadow: 0 0 20px var(--neon-pink);
        transform: translateY(-2px) scale(1.1);
    }
    
    /* Input field styling with glow */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background: #000000;
        border: 4px solid var(--neon-pink);
        color: #ffffff;
        border-radius: 0;
        padding: 10px;
        font-family: 'VT323', monospace;
        font-size: 18px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px var(--neon-pink);
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        box-shadow: 0 0 20px var(--neon-pink);
        outline: none;
        transform: scale(1.02);
    }
    
    /* Slider styling with trail effect */
    .stSlider>div>div>div>div {
        background: var(--neon-pink);
        box-shadow: 0 0 10px var(--neon-pink);
    }
    
    .stSlider>div>div>div>div::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: var(--neon-pink);
        opacity: 0.5;
        filter: blur(5px);
        animation: slider-trail 1s infinite;
    }
    
    @keyframes slider-trail {
        0% { transform: scale(1); opacity: 0.5; }
        100% { transform: scale(1.2); opacity: 0; }
    }
    
    /* Progress bar styling */
    .stProgress>div>div>div {
        background: var(--neon-pink);
        box-shadow: 0 0 10px var(--neon-pink);
        animation: progress-pulse 1s infinite;
    }
    
    @keyframes progress-pulse {
        0% { box-shadow: 0 0 10px var(--neon-pink); }
        50% { box-shadow: 0 0 20px var(--neon-pink); }
        100% { box-shadow: 0 0 10px var(--neon-pink); }
    }
    
    /* Navigation menu styling */
    .css-1d391kg .css-1v0mbdj {
        background: #000000;
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 10px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    
    .css-1d391kg .css-1v0mbdj:hover {
        background: var(--neon-pink);
        color: #000000;
        transform: translateX(5px) scale(1.05);
    }
    
    /* Progress checklist with pixel art checkmarks */
    .progress-checklist {
        background: #000000;
        border: 4px solid var(--neon-pink);
        border-radius: 0;
        padding: 15px;
        margin: 10px 0;
    }
    
    .progress-checklist li {
        list-style-type: none;
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid var(--neon-pink);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .progress-checklist li.completed::before {
        content: '✓';
        position: absolute;
        left: -20px;
        color: var(--neon-green);
        text-shadow: 0 0 10px var(--neon-green);
        animation: checkmark-pop 0.5s ease;
    }
    
    @keyframes checkmark-pop {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    /* Pixel art animations */
    .pixel-art {
        image-rendering: pixelated;
        image-rendering: -moz-crisp-edges;
        image-rendering: crisp-edges;
    }
    
    /* Loading animation */
    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #000000;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    
    .loading-text {
        font-family: 'Press Start 2P', cursive;
        color: var(--neon-pink);
        text-shadow: 0 0 10px var(--neon-pink);
        animation: loading-pulse 1s infinite;
    }
    
    /* Power meter styling */
    .power-meter {
        height: 20px;
        background: #000000;
        border: 4px solid var(--neon-pink);
        position: relative;
        overflow: hidden;
    }
    
    .power-meter::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: var(--neon-pink);
        animation: power-fill 2s ease-in-out infinite;
    }
    
    @keyframes power-fill {
        0% { width: 0%; }
        50% { width: 100%; }
        100% { width: 0%; }
    }
    </style>
    
    <div class="starfield" id="starfield"></div>
    <div class="matrix-rain" id="matrix-rain"></div>
    <script>
        function createStarfield() {
            const starfield = document.getElementById('starfield');
            for (let i = 0; i < 100; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 2 + 's';
                starfield.appendChild(star);
            }
        }
        
        function createMatrixRain() {
            const matrixRain = document.getElementById('matrix-rain');
            const chars = '01';
            const fontSize = 14;
            const columns = Math.floor(window.innerWidth / fontSize);
            
            for (let i = 0; i < columns; i++) {
                const column = document.createElement('div');
                column.style.position = 'absolute';
                column.style.left = i * fontSize + 'px';
                column.style.top = '-100px';
                column.style.fontSize = fontSize + 'px';
                column.style.fontFamily = 'monospace';
                column.style.color = '#0f0';
                column.style.textShadow = '0 0 10px #0f0';
                column.style.animation = 'matrix-fall ' + (Math.random() * 5 + 5) + 's linear infinite';
                column.style.animationDelay = Math.random() * 5 + 's';
                matrixRain.appendChild(column);
                
                setInterval(() => {
                    column.textContent = chars[Math.floor(Math.random() * chars.length)];
                }, 100);
            }
        }
        
        createStarfield();
        createMatrixRain();
    </script>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'preprocessed_df' not in st.session_state:
    st.session_state.preprocessed_df = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'completed_steps' not in st.session_state:
    st.session_state.completed_steps = set()

# Progress checklist component
def show_progress_checklist():
    steps = [
        ("Upload Data", "📊"),
        ("Preprocessing", "🔧"),
        ("Feature Engineering", "🛠️"),
        ("Train/Test Split", "📈"),
        ("Model Training", "🤖"),
        ("Model Evaluation", "📊"),
        ("Results", "📈"),
        ("Export", "📤")
    ]
    
    st.markdown("""
    <div class="progress-checklist pixel-flicker">
        <h3>ML Pipeline Progress</h3>
    """, unsafe_allow_html=True)
    
    for step, emoji in steps:
        status = "completed" if step in st.session_state.completed_steps else "pending"
        st.markdown(f"""
        <li class="{status}">
            {emoji} {step}
        </li>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Enhanced home page with pixel art styling
def show_home_page():
    st.title("Welcome to MLmadeEasy! 🎮")
    
    # Hero section with animated background
    st.markdown("""
    <div class="card">
        <div class="card-content">
            <h1 style="font-size: 3em; margin-bottom: 20px;">MLmadeEasy</h1>
            <p style="font-size: 1.5em; color: var(--neon-blue);">Your Journey to Machine Learning Starts Here!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="card-content">
                <h3 style="color: var(--neon-blue);">📊 Data Management</h3>
                <p>Upload or fetch financial data with ease</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="card-content">
                <h3 style="color: var(--neon-yellow);">🤖 ML Pipeline</h3>
                <p>Complete ML workflow in one place</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="card-content">
                <h3 style="color: var(--neon-green);">📈 Visualizations</h3>
                <p>Beautiful, interactive data insights</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ML Pipeline Progress
    st.markdown("""
    <div class="card">
        <div class="card-content">
            <h2 style="color: var(--neon-purple); text-align: center;">Your ML Journey</h2>
            <div class="progress-checklist">
                <li class="pending">📊 Upload Data</li>
                <li class="pending">🔧 Preprocessing</li>
                <li class="pending">🛠️ Feature Engineering</li>
                <li class="pending">📈 Train/Test Split</li>
                <li class="pending">🤖 Model Training</li>
                <li class="pending">📊 Model Evaluation</li>
                <li class="pending">🎯 Predictions</li>
                <li class="pending">📤 Export Results</li>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("""
    <div class="card">
        <div class="card-content">
            <h2 style="color: var(--neon-orange); text-align: center;">Quick Start Guide</h2>
            <div class="card-grid">
                <div class="feature-card">
                    <h4>1️⃣ Upload Data</h4>
                    <p>Start by uploading your financial data or fetching from Yahoo Finance</p>
                </div>
                <div class="feature-card">
                    <h4>2️⃣ Preprocess</h4>
                    <p>Clean and prepare your data for analysis</p>
                </div>
                <div class="feature-card">
                    <h4>3️⃣ Train Model</h4>
                    <p>Choose and train your ML model</p>
                </div>
                <div class="feature-card">
                    <h4>4️⃣ Evaluate</h4>
                    <p>Analyze model performance and make predictions</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Start Button
    if st.button("🚀 Start Your ML Journey", key="start_journey"):
        st.session_state.current_page = "Upload Data"
        st.experimental_rerun()

# Data Upload Page with enhanced UI
def show_data_upload_page():
    st.title("📊 Upload or Fetch Data")
    
    st.markdown("""
    <div class="card">
        Choose your preferred method to get started with your ML journey!
    </div>
    """, unsafe_allow_html=True)
    
    data_source = st.radio(
        "Choose your data source:",
        ["Upload CSV/Excel", "Fetch from Yahoo Finance"],
        horizontal=True
    )
    
    if data_source == "Upload CSV/Excel":
        uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            with st.spinner("Processing your data... ⏳"):
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.df = pd.read_csv(uploaded_file)
                else:
                    st.session_state.df = pd.read_excel(uploaded_file)
            
            st.success("Data uploaded successfully! 🎉")
            st.dataframe(st.session_state.df.head().style.set_properties(**{
                'background-color': 'rgba(255, 255, 255, 0.1)',
                'color': 'white',
                'border': '1px solid rgba(255, 255, 255, 0.2)'
            }))
            
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker = st.text_input("Enter stock symbol (e.g., AAPL):")
        with col2:
            start_date = st.date_input("Start date:")
        with col3:
            end_date = st.date_input("End date:")
        
        if st.button("Fetch Data", key="fetch_data"):
            with st.spinner("Fetching data from Yahoo Finance... ⏳"):
                try:
                    data = yf.download(ticker, start=start_date, end=end_date)
                    st.session_state.df = data.reset_index()
                    st.success("Data fetched successfully! 🎉")
                    st.dataframe(st.session_state.df.head().style.set_properties(**{
                        'background-color': 'rgba(255, 255, 255, 0.1)',
                        'color': 'white',
                        'border': '1px solid rgba(255, 255, 255, 0.2)'
                    }))
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")

# Preprocessing Page
def show_preprocessing_page():
    st.title("🔧 Data Preprocessing")
    
    if st.session_state.df is None:
        st.warning("Please upload or fetch data first!")
        return
    
    st.subheader("Data Overview")
    st.dataframe(st.session_state.df.head())
    
    st.subheader("Preprocessing Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Handle missing values
        st.write("### Handle Missing Values")
        na_action = st.selectbox(
            "Choose action for missing values:",
            ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode"]
        )
        
        if st.button("Apply Missing Value Treatment"):
            if na_action == "Drop rows":
                st.session_state.df = st.session_state.df.dropna()
            else:
                for col in st.session_state.df.columns:
                    if st.session_state.df[col].dtype in ['int64', 'float64']:
                        if na_action == "Fill with mean":
                            st.session_state.df[col].fillna(st.session_state.df[col].mean(), inplace=True)
                        elif na_action == "Fill with median":
                            st.session_state.df[col].fillna(st.session_state.df[col].median(), inplace=True)
                        else:
                            st.session_state.df[col].fillna(st.session_state.df[col].mode()[0], inplace=True)
            st.success("Missing values handled successfully! 🎉")
    
    with col2:
        # Encode categorical variables
        st.write("### Encode Categorical Variables")
        categorical_cols = st.multiselect(
            "Select categorical columns to encode:",
            st.session_state.df.select_dtypes(include=['object']).columns
        )
        
        if st.button("Apply Encoding"):
            for col in categorical_cols:
                le = LabelEncoder()
                st.session_state.df[col] = le.fit_transform(st.session_state.df[col])
            st.success("Categorical variables encoded successfully! 🎉")
    
    # Show processed data
    if st.button("Show Processed Data"):
        st.dataframe(st.session_state.df.head())
        st.session_state.preprocessed_df = st.session_state.df.copy()

# Feature Engineering Page
def show_feature_engineering_page():
    st.title("🛠️ Feature Engineering")
    
    if st.session_state.df is None:
        st.warning("Please upload and preprocess data first!")
        return
    
    st.subheader("Select Features")
    all_columns = st.session_state.df.columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_var = st.selectbox("Select target variable:", all_columns)
    
    with col2:
        feature_vars = st.multiselect("Select feature variables:", 
                                    [col for col in all_columns if col != target_var])
    
    if st.button("Apply Feature Selection"):
        st.session_state.features = feature_vars
        st.session_state.target = target_var
        st.success("Feature selection applied successfully! 🎉")
        
        # Show correlation matrix
        if len(feature_vars) > 0:
            corr_matrix = st.session_state.df[feature_vars + [target_var]].corr()
            fig = px.imshow(corr_matrix, text_auto=True)
            st.plotly_chart(fig)

# Train/Test Split Page
def show_train_test_split_page():
    st.title("📊 Train/Test Split")
    
    if not hasattr(st.session_state, 'features') or not hasattr(st.session_state, 'target'):
        st.warning("Please select features and target variable first!")
        return
    
    test_size = st.slider("Test size ratio:", 0.1, 0.5, 0.2, 0.05)
    random_state = st.number_input("Random state:", 0, 100, 42)
    
    if st.button("Split Data"):
        X = st.session_state.df[st.session_state.features]
        y = st.session_state.df[st.session_state.target]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        st.session_state.X_train = X_train
        st.session_state.X_test = X_test
        st.session_state.y_train = y_train
        st.session_state.y_test = y_test
        
        # Visualize split
        split_data = pd.DataFrame({
            'Dataset': ['Train', 'Test'],
            'Size': [len(X_train), len(X_test)]
        })
        
        fig = px.pie(split_data, values='Size', names='Dataset', 
                    title='Train/Test Split Distribution')
        st.plotly_chart(fig)
        
        st.success("Data split successfully! 🎉")

# Model Training Page
def show_model_training_page():
    st.title("🤖 Model Training")
    
    if not all(key in st.session_state for key in ['X_train', 'y_train']):
        st.warning("Please perform train/test split first!")
        return
    
    # Model selection with enhanced UI
    st.markdown("""
    <div class="card">
        <h2 style="color: var(--neon-pink); text-align: center;">Select Your Model</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Model type selection
    problem_type = st.radio(
        "Select Problem Type:",
        ["Regression", "Classification", "Clustering"],
        horizontal=True
    )
    
    # Model selection based on problem type
    if problem_type == "Regression":
        model_type = st.selectbox(
            "Select Regression Model:",
            ["Linear Regression", "Random Forest", "SVR", "Decision Tree", "KNN"]
        )
    elif problem_type == "Classification":
        model_type = st.selectbox(
            "Select Classification Model:",
            ["Logistic Regression", "Random Forest", "SVC", "Decision Tree", "KNN"]
        )
    else:  # Clustering
        model_type = st.selectbox(
            "Select Clustering Model:",
            ["K-Means"]
        )
    
    # Model parameters
    st.markdown("""
    <div class="card">
        <h3 style="color: var(--neon-blue);">Model Parameters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if model_type in ["Random Forest", "Decision Tree"]:
            max_depth = st.slider("Max Depth", 1, 20, 5)
            n_estimators = st.slider("Number of Estimators", 10, 200, 100) if model_type == "Random Forest" else None
        elif model_type in ["SVR", "SVC"]:
            kernel = st.selectbox("Kernel", ["linear", "rbf", "poly"])
            C = st.slider("C (Regularization)", 0.1, 10.0, 1.0)
        elif model_type == "KNN":
            n_neighbors = st.slider("Number of Neighbors", 1, 20, 5)
        elif model_type == "K-Means":
            n_clusters = st.slider("Number of Clusters", 2, 10, 3)
    
    with col2:
        if model_type in ["Random Forest", "Decision Tree"]:
            min_samples_split = st.slider("Min Samples Split", 2, 20, 2)
            min_samples_leaf = st.slider("Min Samples Leaf", 1, 10, 1)
    
    # Training button with enhanced UI
    if st.button("🚀 Train Model", key="train_model"):
        try:
            with st.spinner("Training model... ⏳"):
                # Initialize model
                if problem_type == "Regression":
                    if model_type == "Linear Regression":
                        model = LinearRegression()
                    elif model_type == "Random Forest":
                        model = RandomForestRegressor(
                            n_estimators=n_estimators,
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf
                        )
                    elif model_type == "SVR":
                        model = SVR(kernel=kernel, C=C)
                    elif model_type == "Decision Tree":
                        model = DecisionTreeRegressor(
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf
                        )
                    else:  # KNN
                        model = KNeighborsRegressor(n_neighbors=n_neighbors)
                
                elif problem_type == "Classification":
                    if model_type == "Logistic Regression":
                        model = LogisticRegression(max_iter=1000)
                    elif model_type == "Random Forest":
                        model = RandomForestClassifier(
                            n_estimators=n_estimators,
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf
                        )
                    elif model_type == "SVC":
                        model = SVC(kernel=kernel, C=C)
                    elif model_type == "Decision Tree":
                        model = DecisionTreeClassifier(
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf
                        )
                    else:  # KNN
                        model = KNeighborsClassifier(n_neighbors=n_neighbors)
                
                else:  # Clustering
                    model = KMeans(n_clusters=n_clusters)
                
                # Train model
                if problem_type != "Clustering":
                    model.fit(st.session_state.X_train, st.session_state.y_train)
                else:
                    model.fit(st.session_state.X_train)
                
                st.session_state.model = model
                st.session_state.problem_type = problem_type
                
                st.success("Model trained successfully! 🎉")
                
                # Show model details
                show_model_details(model, problem_type)
        
        except Exception as e:
            st.error(f"Error during model training: {str(e)}")

def show_model_details(model, problem_type):
    st.markdown("""
    <div class="card">
        <h2 style="color: var(--neon-pink); text-align: center;">Model Details</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if problem_type != "Clustering":
        # Feature importance
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'Feature': st.session_state.features,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            fig = px.bar(importance_df, x='Feature', y='Importance',
                        title='Feature Importance',
                        color='Importance',
                        color_continuous_scale='RdBu')
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Model coefficients for linear models
        if hasattr(model, 'coef_'):
            coef_df = pd.DataFrame({
                'Feature': st.session_state.features,
                'Coefficient': model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
            }).sort_values('Coefficient', ascending=False)
            
            fig = px.bar(coef_df, x='Feature', y='Coefficient',
                        title='Model Coefficients',
                        color='Coefficient',
                        color_continuous_scale='RdBu')
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:  # Clustering
        # Cluster visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(st.session_state.X_train)
        
        cluster_df = pd.DataFrame({
            'PC1': X_pca[:, 0],
            'PC2': X_pca[:, 1],
            'Cluster': model.labels_
        })
        
        fig = px.scatter(cluster_df, x='PC1', y='PC2', color='Cluster',
                        title='Cluster Visualization (PCA)',
                        color_continuous_scale='RdBu')
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cluster metrics
        silhouette = silhouette_score(st.session_state.X_train, model.labels_)
        calinski = calinski_harabasz_score(st.session_state.X_train, model.labels_)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-blue);">
                <h3>Silhouette Score</h3>
                <h2 style="color: var(--neon-blue);">{silhouette:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-yellow);">
                <h3>Calinski-Harabasz Score</h3>
                <h2 style="color: var(--neon-yellow);">{calinski:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)

# Enhanced model evaluation page with comprehensive visualizations
def show_model_evaluation_page():
    st.title("📊 Model Evaluation")
    
    if st.session_state.model is None:
        st.warning("Please train a model first!")
        return
    
    # Make predictions
    y_pred = st.session_state.model.predict(st.session_state.X_test)
    
    # Model Metrics Section
    st.markdown("""
    <div class="card">
        <h2 style="color: var(--neon-pink); text-align: center;">Model Performance Metrics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if it's a regression or classification problem
    is_regression = isinstance(st.session_state.model, (LinearRegression, RandomForestRegressor, SVR, DecisionTreeRegressor, KNeighborsRegressor))
    is_clustering = isinstance(st.session_state.model, KMeans)
    
    if is_regression:
        # Regression Metrics
        r2 = r2_score(st.session_state.y_test, y_pred)
        mse = mean_squared_error(st.session_state.y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(st.session_state.y_test, y_pred)
        
        # Metrics Grid
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-blue);">
                <h3>R² Score</h3>
                <h2 style="color: var(--neon-blue);">{r2:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-yellow);">
                <h3>MSE</h3>
                <h2 style="color: var(--neon-yellow);">{mse:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-green);">
                <h3>RMSE</h3>
                <h2 style="color: var(--neon-green);">{rmse:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-purple);">
                <h3>MAE</h3>
                <h2 style="color: var(--neon-purple);">{mae:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("""
        <div class="card">
            <h2 style="color: var(--neon-pink); text-align: center;">Model Visualizations</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Residual Plot
        residuals = st.session_state.y_test - y_pred
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_pred,
            y=residuals,
            mode='markers',
            marker=dict(
                color='var(--neon-pink)',
                size=10,
                line=dict(color='var(--neon-blue)', width=2)
            ),
            name='Residuals'
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="var(--neon-red)")
        fig.update_layout(
            title='Residual Plot',
            xaxis_title='Predicted Values',
            yaxis_title='Residuals',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Actual vs Predicted Plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.y_test,
            y=y_pred,
            mode='markers',
            marker=dict(
                color='var(--neon-yellow)',
                size=10,
                line=dict(color='var(--neon-green)', width=2)
            ),
            name='Predictions'
        ))
        fig.add_trace(go.Scatter(
            x=[st.session_state.y_test.min(), st.session_state.y_test.max()],
            y=[st.session_state.y_test.min(), st.session_state.y_test.max()],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='var(--neon-red)', dash='dash')
        ))
        fig.update_layout(
            title='Actual vs Predicted Values',
            xaxis_title='Actual',
            yaxis_title='Predicted',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif is_clustering:
        # Clustering Metrics
        silhouette = silhouette_score(st.session_state.X_test, y_pred)
        calinski = calinski_harabasz_score(st.session_state.X_test, y_pred)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-blue);">
                <h3>Silhouette Score</h3>
                <h2 style="color: var(--neon-blue);">{silhouette:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-yellow);">
                <h3>Calinski-Harabasz Score</h3>
                <h2 style="color: var(--neon-yellow);">{calinski:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Cluster Visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(st.session_state.X_test)
        
        cluster_df = pd.DataFrame({
            'PC1': X_pca[:, 0],
            'PC2': X_pca[:, 1],
            'Cluster': y_pred
        })
        
        fig = px.scatter(cluster_df, x='PC1', y='PC2', color='Cluster',
                        title='Cluster Visualization (PCA)',
                        color_continuous_scale='RdBu')
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:  # Classification
        # Classification Metrics
        accuracy = accuracy_score(st.session_state.y_test, y_pred)
        precision = precision_score(st.session_state.y_test, y_pred, average='weighted')
        recall = recall_score(st.session_state.y_test, y_pred, average='weighted')
        f1 = f1_score(st.session_state.y_test, y_pred, average='weighted')
        
        # Metrics Grid
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-blue);">
                <h3>Accuracy</h3>
                <h2 style="color: var(--neon-blue);">{accuracy:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-yellow);">
                <h3>Precision</h3>
                <h2 style="color: var(--neon-yellow);">{precision:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-green);">
                <h3>Recall</h3>
                <h2 style="color: var(--neon-green);">{recall:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; border: 2px solid var(--neon-purple);">
                <h3>F1 Score</h3>
                <h2 style="color: var(--neon-purple);">{f1:.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Confusion Matrix
        cm = confusion_matrix(st.session_state.y_test, y_pred)
        fig = px.imshow(cm, text_auto=True,
                       labels=dict(x="Predicted", y="Actual"),
                       title="Confusion Matrix",
                       color_continuous_scale='RdBu')
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ROC Curve (only for binary classification)
        if len(np.unique(st.session_state.y_test)) == 2:
            fpr, tpr, _ = roc_curve(st.session_state.y_test, y_pred)
            roc_auc = auc(fpr, tpr)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fpr, y=tpr,
                                    mode='lines',
                                    name=f'ROC curve (AUC = {roc_auc:.2f})',
                                    line=dict(color='var(--neon-pink)', width=2)))
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1],
                                    mode='lines',
                                    name='Random',
                                    line=dict(color='var(--neon-blue)', dash='dash')))
            fig.update_layout(
                title='ROC Curve',
                xaxis_title='False Positive Rate',
                yaxis_title='True Positive Rate',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Feature Importance for tree-based models
    if hasattr(st.session_state.model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'Feature': st.session_state.features,
            'Importance': st.session_state.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        fig = px.bar(importance_df, x='Feature', y='Importance',
                    title='Feature Importance',
                    color='Importance',
                    color_continuous_scale='RdBu')
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# Results Page
def show_results_page():
    st.title("📊 Results & Predictions")
    
    if st.session_state.model is None:
        st.warning("Please train and evaluate a model first!")
        return
    
    # Make predictions on test set
    y_pred = st.session_state.model.predict(st.session_state.X_test)
    st.session_state.predictions = y_pred
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'Actual': st.session_state.y_test,
        'Predicted': y_pred
    })
    
    st.dataframe(results_df)
    
    # Download predictions
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="Download Predictions",
        data=csv,
        file_name="predictions.csv",
        mime="text/csv"
    )

# Enhanced Export Page with Report Generation
def show_export_page():
    st.title("📤 Export & Download")
    
    if st.session_state.model is None:
        st.warning("Please train a model first!")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Model")
        if st.button("Save Model"):
            model_path = "trained_model.pkl"
            joblib.dump(st.session_state.model, model_path)
            
            with open(model_path, "rb") as f:
                st.download_button(
                    label="Download Model",
                    data=f,
                    file_name="trained_model.pkl",
                    mime="application/octet-stream"
                )
    
    with col2:
        st.subheader("Generate Report")
        if st.button("Create Report"):
            # Create a comprehensive report
            report = []
            
            # Add header
            report.append("# MLmadeEasy Model Report")
            report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("\n## Model Information")
            
            # Add model details based on model type
            if isinstance(st.session_state.model, (LinearRegression, LogisticRegression)):
                model_type = "Linear Regression" if isinstance(st.session_state.model, LinearRegression) else "Logistic Regression"
                report.append(f"### Model Type: {model_type}")
                
                # Handle intercept
                if hasattr(st.session_state.model, 'intercept_'):
                    if isinstance(st.session_state.model.intercept_, np.ndarray):
                        report.append(f"Intercept: {st.session_state.model.intercept_[0]:.4f}")
                    else:
                        report.append(f"Intercept: {st.session_state.model.intercept_:.4f}")
                
                # Handle coefficients
                if hasattr(st.session_state.model, 'coef_'):
                    report.append("\n### Feature Coefficients:")
                    if len(st.session_state.model.coef_.shape) > 1:
                        coefs = st.session_state.model.coef_[0]
                    else:
                        coefs = st.session_state.model.coef_
                    for feature, coef in zip(st.session_state.features, coefs):
                        report.append(f"- {feature}: {coef:.4f}")
            
            elif isinstance(st.session_state.model, (RandomForestRegressor, RandomForestClassifier)):
                model_type = "Random Forest Regression" if isinstance(st.session_state.model, RandomForestRegressor) else "Random Forest Classification"
                report.append(f"### Model Type: {model_type}")
                report.append(f"Number of Trees: {st.session_state.model.n_estimators}")
                report.append(f"Max Depth: {st.session_state.model.max_depth}")
                
                if hasattr(st.session_state.model, 'feature_importances_'):
                    report.append("\n### Feature Importances:")
                    for feature, importance in zip(st.session_state.features, st.session_state.model.feature_importances_):
                        report.append(f"- {feature}: {importance:.4f}")
            
            elif isinstance(st.session_state.model, (SVR, SVC)):
                model_type = "Support Vector Regression" if isinstance(st.session_state.model, SVR) else "Support Vector Classification"
                report.append(f"### Model Type: {model_type}")
                report.append(f"Kernel: {st.session_state.model.kernel}")
                report.append(f"C: {st.session_state.model.C}")
            
            elif isinstance(st.session_state.model, (DecisionTreeRegressor, DecisionTreeClassifier)):
                model_type = "Decision Tree Regression" if isinstance(st.session_state.model, DecisionTreeRegressor) else "Decision Tree Classification"
                report.append(f"### Model Type: {model_type}")
                report.append(f"Max Depth: {st.session_state.model.max_depth}")
                
                if hasattr(st.session_state.model, 'feature_importances_'):
                    report.append("\n### Feature Importances:")
                    for feature, importance in zip(st.session_state.features, st.session_state.model.feature_importances_):
                        report.append(f"- {feature}: {importance:.4f}")
            
            elif isinstance(st.session_state.model, (KNeighborsRegressor, KNeighborsClassifier)):
                model_type = "K-Nearest Neighbors Regression" if isinstance(st.session_state.model, KNeighborsRegressor) else "K-Nearest Neighbors Classification"
                report.append(f"### Model Type: {model_type}")
                report.append(f"Number of Neighbors: {st.session_state.model.n_neighbors}")
            
            elif isinstance(st.session_state.model, KMeans):
                report.append("### Model Type: K-Means Clustering")
                report.append(f"Number of Clusters: {st.session_state.model.n_clusters}")
                report.append(f"Number of Iterations: {st.session_state.model.n_iter_}")
            
            # Add evaluation metrics
            report.append("\n## Model Performance")
            y_pred = st.session_state.model.predict(st.session_state.X_test)
            
            if isinstance(st.session_state.model, (LinearRegression, RandomForestRegressor, SVR, DecisionTreeRegressor, KNeighborsRegressor)):
                r2 = r2_score(st.session_state.y_test, y_pred)
                mse = mean_squared_error(st.session_state.y_test, y_pred)
                rmse = np.sqrt(mse)
                mae = mean_absolute_error(st.session_state.y_test, y_pred)
                
                report.append(f"- R² Score: {r2:.4f}")
                report.append(f"- Mean Squared Error: {mse:.4f}")
                report.append(f"- Root Mean Squared Error: {rmse:.4f}")
                report.append(f"- Mean Absolute Error: {mae:.4f}")
            
            elif isinstance(st.session_state.model, (LogisticRegression, RandomForestClassifier, SVC, DecisionTreeClassifier, KNeighborsClassifier)):
                accuracy = accuracy_score(st.session_state.y_test, y_pred)
                precision = precision_score(st.session_state.y_test, y_pred, average='weighted')
                recall = recall_score(st.session_state.y_test, y_pred, average='weighted')
                f1 = f1_score(st.session_state.y_test, y_pred, average='weighted')
                
                report.append(f"- Accuracy: {accuracy:.4f}")
                report.append(f"- Precision: {precision:.4f}")
                report.append(f"- Recall: {recall:.4f}")
                report.append(f"- F1 Score: {f1:.4f}")
            
            elif isinstance(st.session_state.model, KMeans):
                silhouette = silhouette_score(st.session_state.X_test, y_pred)
                calinski = calinski_harabasz_score(st.session_state.X_test, y_pred)
                
                report.append(f"- Silhouette Score: {silhouette:.4f}")
                report.append(f"- Calinski-Harabasz Score: {calinski:.4f}")
            
            # Add data summary
            report.append("\n## Data Summary")
            report.append(f"- Number of Features: {len(st.session_state.features)}")
            report.append(f"- Training Samples: {len(st.session_state.X_train)}")
            report.append(f"- Test Samples: {len(st.session_state.X_test)}")
            
            # Convert report to string
            report_text = "\n".join(report)
            
            # Create download button
            st.download_button(
                label="Download Report",
                data=report_text,
                file_name="ml_report.md",
                mime="text/markdown"
            )
            
            # Display report preview
            st.subheader("Report Preview")
            st.markdown(report_text)

# About Page
def show_about_page():
    st.title("ℹ️ About MLmadeEasy")
    
    st.markdown("""
    ## Welcome to MLmadeEasy! 🎯
    
    MLmadeEasy is a user-friendly application designed to make machine learning accessible 
    to everyone, especially finance students and beginners. Our goal is to simplify the 
    machine learning workflow while maintaining professional standards.
    
    ### Features:
    - 📊 Easy data upload and fetching
    - 🔧 Comprehensive data preprocessing
    - 🛠️ Powerful feature engineering
    - 🤖 Multiple model options
    - 📈 Detailed evaluation metrics
    - 📤 Easy export and sharing
    
    ### How to Use:
    1. Upload your data or fetch from Yahoo Finance
    2. Preprocess and clean your data
    3. Select and engineer features
    4. Split your data into train/test sets
    5. Train your model
    6. Evaluate the results
    7. Export your findings
    
    ### Need Help?
    Feel free to reach out with any questions or suggestions!
    """)

# Main App with enhanced sidebar
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: var(--neon-pink); margin-bottom: 20px; text-shadow: 0 0 10px var(--neon-pink);">
                MLmadeEasy 🎮
            </h1>
            <div style="
                width: 120px;
                height: 120px;
                margin: 0 auto 20px;
                background: linear-gradient(45deg, var(--neon-pink), var(--neon-blue));
                border: 4px solid var(--neon-pink);
                box-shadow: 0 0 20px var(--neon-pink);
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Press Start 2P', cursive;
                font-size: 24px;
                color: white;
                text-shadow: 0 0 10px var(--neon-pink);
                animation: logo-pulse 2s infinite;
            ">
                ML
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Upload Data", "Preprocessing", "Feature Engineering", 
                    "Train/Test Split", "Model Training", "Model Evaluation", 
                    "Results", "Export", "About"],
            icons=["house", "cloud-upload", "gear", "sliders", 
                   "graph-up", "robot", "bar-chart", 
                   "file-earmark-text", "download", "info-circle"],
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background": "#000000"},
                "icon": {"color": "var(--neon-pink)", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "color": "white"},
                "nav-link-selected": {"background": "var(--neon-pink)", "color": "#000000"},
            }
        )
    
    # Page routing
    if selected == "Home":
        show_home_page()
    elif selected == "Upload Data":
        show_data_upload_page()
    elif selected == "Preprocessing":
        show_preprocessing_page()
    elif selected == "Feature Engineering":
        show_feature_engineering_page()
    elif selected == "Train/Test Split":
        show_train_test_split_page()
    elif selected == "Model Training":
        show_model_training_page()
    elif selected == "Model Evaluation":
        show_model_evaluation_page()
    elif selected == "Results":
        show_results_page()
    elif selected == "Export":
        show_export_page()
    elif selected == "About":
        show_about_page()

if __name__ == "__main__":
    main() 