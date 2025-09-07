"""
AI Research Agent - Enhanced Interactive Layout
Improved styling and interactive design while maintaining all functionality
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import os
import logging
from typing import Dict, List
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Core imports with error handling
try:
    from modules.web_search import WebSearchEngine
    from modules.content_extractor import ContentExtractor  
    from modules.ai_summarizer import AISummarizer
    from utils.pdf_generator import PDFGenerator
    from config import Config
    CORE_MODULES_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Core modules missing: {e}")
    st.stop()

# Enhanced modules (graceful fallback)
try:
    from modules.enhanced_search import EnhancedSearchEngine
    from modules.enhanced_ai import EnhancedSummarizer
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False

try:
    from modules.historical_data import HistoricalDataAnalyzer
    HISTORICAL_DATA_AVAILABLE = True
except ImportError:
    HISTORICAL_DATA_AVAILABLE = False

try:
    from modules.enhanced_images import EnhancedImageProcessor
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False

# Enhanced page configuration for network access
st.set_page_config(
    page_title="AI Research Agent - Network Ready",
    page_icon="🤖📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/ai-research-agent',
        'Report a bug': 'https://github.com/your-repo/ai-research-agent/issues',
        'About': "# 🌐 AI Research Agent - Network Access\n\n✅ **Multi-Device Access**: Use from any device on your network\n✅ **Mobile Friendly**: Works on phones, tablets, computers\n✅ **Real-time Sync**: All devices see the same research results\n\n**Network URL**: Check terminal for your network IP address"
    }
)

# Modern CSS styling with day/night theme support
def get_theme_css(theme_mode):
    if theme_mode == "night":
        return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }
    
    .main .block-container {
        padding: 2rem;
        background: rgba(30, 30, 50, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        color: #63b3ed;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .main-header h3 {
        color: rgba(226, 232, 240, 0.9);
        font-size: 1.4rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .feature-badge {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        margin: 2rem auto;
        max-width: 900px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 10px 30px rgba(66, 153, 225, 0.4);
        animation: pulse 2s infinite;
    }
    
    .search-container {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        margin: 2rem 0;
        border: 2px solid rgba(99, 179, 237, 0.2);
        transition: all 0.3s ease;
    }
    
    .search-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        border-color: rgba(99, 179, 237, 0.4);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(66, 153, 225, 0.6);
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border-left: 4px solid;
        text-align: center;
        color: #e2e8f0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin: 2rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        font-weight: 500;
        color: #cbd5e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(66, 153, 225, 0.4);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(66, 153, 225, 0.2);
        transform: translateY(-3px);
        border-color: rgba(66, 153, 225, 0.3);
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border: 2px solid #4a5568;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        color: #e2e8f0;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4299e1;
        box-shadow: 0 10px 30px rgba(66, 153, 225, 0.3);
        transform: translateY(-2px);
    }
    
    .stSelectbox > div > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border: 2px solid #4a5568;
        border-radius: 12px;
        color: #e2e8f0;
    }
    
    .stRadio > div {
        background: rgba(45, 55, 72, 0.3);
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stCheckbox > label {
        color: #cbd5e0;
    }
    
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(66, 153, 225, 0.2);
        border: 2px solid rgba(66, 153, 225, 0.3);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        color: #63b3ed;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        background: rgba(66, 153, 225, 0.3);
        transform: scale(1.05);
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 10px 30px rgba(66, 153, 225, 0.4); }
        50% { box-shadow: 0 15px 40px rgba(66, 153, 225, 0.6); }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
    else:  # Day theme
        return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1rem;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h3 {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .feature-badge {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        margin: 2rem auto;
        max-width: 900px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
        animation: pulse 2s infinite;
    }
    
    .search-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .search-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border-left: 4px solid;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateY(-3px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        border: 2px solid #e1e8f0;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        color: #667eea;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: scale(1.05);
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4); }
        50% { box-shadow: 0 15px 40px rgba(79, 172, 254, 0.6); }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# Initialize session state first
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'research_history' not in st.session_state:
    st.session_state.research_history = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "day"  # Default to day theme

# Apply theme CSS after initialization
st.markdown(get_theme_css(st.session_state.theme_mode), unsafe_allow_html=True)

def safe_api_call(func, *args, **kwargs):
    """Safely call API functions with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return {"error": str(e), "success": False}

def display_follow_up_questions(results):
    """Display follow-up questions in an interactive format"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
        <h2 style="margin: 0; font-size: 1.8rem;">❓ Follow-up Questions</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Explore deeper insights about "{results['query']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    follow_up_questions = results.get('follow_up_questions', [])
    
    if follow_up_questions:
        st.markdown("### 🤔 Suggested Questions for Further Research")
        st.markdown("Click on any question to explore it further:")
        
        # Display questions in an interactive grid with better styling
        cols = st.columns(2)
        
        for i, question in enumerate(follow_up_questions):
            with cols[i % 2]:
                # Enhanced button styling
                button_style = """
                <style>
                div.stButton > button:first-child {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 1rem;
                    font-size: 0.95rem;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    text-align: left;
                    height: auto;
                    white-space: normal;
                    margin-bottom: 0.5rem;
                }
                div.stButton > button:first-child:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
                    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
                }
                </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                
                if st.button(f"🔍 {question}", key=f"followup_{i}", use_container_width=True):
                    # When clicked, populate the search box with this question
                    st.session_state.search_query = question
                    st.success(f"Ready to research: {question}")
                    st.info("Click the 'Start Research' button above to begin exploring this question.")
                    st.rerun()  # Refresh to update the search box
        
        st.markdown("---")
        st.markdown("### 💡 Create Your Own Question")
        st.markdown("Have a specific aspect you want to explore further?")
        
        # Pre-fill with query for context
        custom_question = st.text_input("Enter your custom research question:", 
                                       placeholder=f"e.g., What are the implications of {results['query']} for...?",
                                       key="custom_followup_question")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_question_full = st.text_area("Or write a more detailed question:", 
                                               placeholder=f"Write a detailed research question about {results['query']}...",
                                               height=100,
                                               key="custom_followup_question_detailed")
        with col2:
            st.markdown(" ")
            st.markdown(" ")
            if st.button("Research Custom Question") and (custom_question or custom_question_full):
                final_question = custom_question_full if custom_question_full else custom_question
                st.session_state.search_query = final_question
                st.success(f"Ready to research: {final_question}")
                st.info("Click the 'Start Research' button above to begin your custom research.")
                st.rerun()  # Refresh to update the search box
    else:
        st.info("No follow-up questions generated for this research topic. Try a different query for more insights.")

def main():
    """Enhanced main application with modern styling and theme support"""
    
    # Theme toggle in top-right corner
    theme_icon = "🌙" if st.session_state.theme_mode == "day" else "☀️"
    theme_text = "Night" if st.session_state.theme_mode == "day" else "Day"
    
    st.markdown(f'''
    <div class="theme-toggle" onclick="parent.document.querySelector('[data-testid=\"stButton\"] button').click()">
        {theme_icon} {theme_text} Mode
    </div>
    ''', unsafe_allow_html=True)
    
    # Theme toggle button (hidden but functional)
    if st.button("🔄 Toggle Theme", key="theme_toggle", help="Switch between day and night themes"):
        st.session_state.theme_mode = "night" if st.session_state.theme_mode == "day" else "day"
        st.rerun()
    
    # Enhanced header with AI restoration notice
    try:
        config = Config()
        validation = config.validate_api_keys()
        ai_providers = validation.get('ai_providers', [])
        
        if 'OpenAI' in ai_providers:
            ai_notice = '<div style="text-align: center; color: #4ade80; font-size: 1.1rem; margin: 1rem 0;">🎉 AI Summaries Restored with OpenAI + Multi-Provider Fallbacks 🚀</div>'
        elif len(ai_providers) >= 2:
            ai_notice = '<div style="text-align: center; color: #60a5fa; font-size: 1.1rem; margin: 1rem 0;">⚡ Enhanced AI Summaries Active with Multiple Providers</div>'
        elif len(ai_providers) >= 1:
            ai_notice = '<div style="text-align: center; color: #34d399; font-size: 1.1rem; margin: 1rem 0;">✅ AI Summaries Active</div>'
        else:
            ai_notice = ''
    except:
        ai_notice = ''
    
    st.markdown(f'''
    <div class="main-header">
        <h1>🤖 AI Research Agent</h1>
        <h3>Intelligent Analysis • Quick & Advanced Search • Structured Reports</h3>
        {ai_notice}
    </div>
    ''', unsafe_allow_html=True)
    
    # Feature status badge with enhanced AI info
    feature_count = sum([CORE_MODULES_AVAILABLE, ENHANCED_FEATURES_AVAILABLE, HISTORICAL_DATA_AVAILABLE, IMAGE_PROCESSING_AVAILABLE])
    
    # Check AI provider status for enhanced messaging
    try:
        config = Config()
        validation = config.validate_api_keys()
        ai_count = len(validation.get('ai_providers', []))
        
        if ai_count >= 4:
            ai_status = "✨ Multi-AI Active (Premium Quality)"
        elif ai_count >= 2:
            ai_status = "🔥 Enhanced AI Active"
        elif ai_count >= 1:
            ai_status = "✅ AI Summaries Active"
        else:
            ai_status = "⚠️ Fallback Mode"
            
        status_text = f"⚡ {feature_count}/4 FEATURE SETS ACTIVE: {ai_status} • Lightning Quick Search (2-8s) • Advanced Search (8-20s) • Structured Analysis • Professional Export"
    except:
        status_text = f"⚡ {feature_count}/4 FEATURE SETS ACTIVE: Lightning Quick Search (2-8s) • Advanced Search (8-20s) • Structured Analysis • Professional Export"
    
    st.markdown(f'''
    <div class="feature-badge">
        {status_text}
    </div>
    ''', unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        # Enhanced sidebar with theme-aware styling
        sidebar_bg = "rgba(30, 30, 50, 0.9)" if st.session_state.theme_mode == "night" else "rgba(255, 255, 255, 0.1)"
        sidebar_color = "#e2e8f0" if st.session_state.theme_mode == "night" else "white"
        
        st.markdown(f'''
        <div style="background: {sidebar_bg}; padding: 1rem 0; text-align: center; border-radius: 15px; margin-bottom: 1rem;">
            <h2 style="color: {sidebar_color}; margin: 0;">⚙️ Configuration</h2>
        </div>
        ''', unsafe_allow_html=True)
        
        # API Status
        try:
            config = Config()
            validation = config.validate_api_keys()
            
            st.markdown(f'''
            <div style="background: {sidebar_bg}; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                <h4 style="color: {sidebar_color}; margin: 0 0 1rem 0;">📊 API Status</h4>
            </div>
            ''', unsafe_allow_html=True)
            
            # Show enhanced status with restored APIs
            ai_providers = validation.get('ai_providers', [])
            search_engines = validation.get('search_engines', [])
            working_count = validation.get('working_count', 0)
            
            # Status indicator with enhanced info
            if working_count > 8:
                status_color = "green"
                status_text = "🎉 EXCELLENT"
            elif working_count > 5:
                status_color = "blue"
                status_text = "✅ GOOD"
            elif working_count > 2:
                status_color = "orange"
                status_text = "⚠️ LIMITED"
            else:
                status_color = "red"
                status_text = "❌ CRITICAL"
            
            st.markdown(f'''
            <div style="background: {status_color}; color: white; padding: 0.8rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <strong>{status_text}</strong><br/>
                {working_count} APIs Active
            </div>
            ''', unsafe_allow_html=True)
            
            # Show AI providers with enhanced display
            if ai_providers:
                st.markdown("**🧠 AI Providers:**")
                ai_status = []
                if 'OpenAI' in ai_providers:
                    ai_status.append('🔥 OpenAI (Restored)')
                if 'Gemini' in ai_providers:
                    ai_status.append('🔮 Gemini (Free)')
                if 'Anthropic' in ai_providers:
                    ai_status.append('🧠 Claude')
                if 'Perplexity' in ai_providers:
                    ai_status.append('⚡ Perplexity')
                for provider in ai_providers:
                    if provider not in ['OpenAI', 'Gemini', 'Anthropic', 'Perplexity']:
                        ai_status.append(f'✨ {provider}')
                
                for status in ai_status:
                    st.write(f"  {status}")
            
            # Show search engines
            if search_engines:
                st.write(f"🔍 **Search:** {', '.join(search_engines)}")
            
            # Summary generation status
            if ai_providers:
                st.success("✅ AI Summaries: Active")
            else:
                st.warning("⚠️ AI Summaries: Fallback mode")
        except Exception as e:
            st.error(f"Config error: {str(e)}")
        
        # Research settings
        st.markdown(f'''
        <div style="background: {sidebar_bg}; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
            <h4 style="color: {sidebar_color}; margin: 0 0 1rem 0;">🔍 Research Settings</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        search_speed = st.radio(
            "🚀 Search Speed",
            ["⚡ Quick Search (2-8 seconds)", "🔬 Advanced Search (8-20 seconds)"],
            help="Quick: Lightning-fast results with essential information | Advanced: Comprehensive research with detailed analysis"
        )
        
        # Dynamic settings with speed optimization
        if "Quick" in search_speed:
            num_results = st.slider("Sources to analyze", 3, 5, 3)  # Reduced for speed
            search_mode = "Standard"
            include_images = st.checkbox("🖼️ Include images", value=False)
            include_trends = st.checkbox("📈 Include trends", value=False)
            summary_type = "brief"
            st.success("⚡ Quick mode: Ultra-fast results (3-8 seconds)")
        else:
            num_results = st.slider("Sources to analyze", 5, 15, 8)  # Reduced for speed
            search_mode = st.radio("Search Engine", ["Enhanced", "Standard"]) if ENHANCED_FEATURES_AVAILABLE else "Standard"
            include_images = st.checkbox("🖼️ Include images", value=False)  # Disabled by default for speed
            include_trends = st.checkbox("📈 Include trends", value=False)  # Disabled by default for speed
            summary_type = st.selectbox("Analysis depth", ["detailed", "brief", "comprehensive"])
            st.success("🔬 Advanced mode: Fast comprehensive analysis (8-20 seconds)")
        
        enable_visualizations = st.checkbox("📊 Enable charts", value=True)
        
        # Output format options
        st.markdown(f'''
        <div style="background: {sidebar_bg}; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
            <h4 style="color: {sidebar_color}; margin: 0 0 1rem 0;">📋 Output Format</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        detailed_formatting = st.checkbox("🎨 AI-powered detailed formatting", value=True)
        include_tables = st.checkbox("📊 Data tables", value=True)
        include_bullet_points = st.checkbox("• Enhanced bullets", value=True)
    
    # Enhanced search interface with theme support
    search_bg = "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)" if st.session_state.theme_mode == "night" else "linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%)"
    search_color = "#e2e8f0" if st.session_state.theme_mode == "night" else "#333"
    
    st.markdown(f'''
    <div style="background: {search_bg}; padding: 2rem; border-radius: 20px; margin: 2rem 0; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2); border: 2px solid rgba(102, 126, 234, 0.2);">
        <h2 style="color: {search_color}; margin: 0 0 1.5rem 0; text-align: center;">🔍 Research Query</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        query = st.text_input(
            "Enter your research topic:",
            placeholder="e.g., Latest AI developments, Climate change solutions, Technology trends",
            value=st.session_state.search_query,
            label_visibility="collapsed"
        )
        
        search_button = st.button("🚀 Start Research", type="primary")
    
    with col2:
        st.markdown("**💡 Quick Examples**")
        examples = [
            ("⚡ AI trends 2024", "AI trends 2024"), 
            ("🌍 Climate change", "Climate change"), 
            ("🚀 Space exploration", "Space exploration"), 
            ("⚕️ Medical research", "Medical research"), 
            ("📱 Technology news", "Technology news")
        ]
        
        for display_text, example in examples:
            if st.button(display_text, key=f"example_{example}"):
                st.session_state.search_query = example
                st.rerun()
    
    # Research execution (keeping all existing functionality)
    if search_button and query:
        st.session_state.search_query = query
        
        with st.spinner("🔍 Researching..."):
            progress = st.progress(0)
            status = st.empty()
            
            try:
                # Step 1: Search
                status.text("🔍 Searching for information...")
                progress.progress(20)
                
                if search_mode == "Enhanced" and ENHANCED_FEATURES_AVAILABLE:
                    enhanced_search = EnhancedSearchEngine()
                    search_results = safe_api_call(enhanced_search.fast_search_and_analyze, query, num_results)
                else:
                    search_engine = WebSearchEngine()
                    search_results = safe_api_call(search_engine.search, query, num_results)
                
                progress.progress(40)
                
                # Step 2: Enhanced content extraction for comprehensive summaries
                status.text("📄 Extracting comprehensive content from all sources...")
                extracted_content = []
                results_list = []  # Initialize results_list
                
                if search_results and (not isinstance(search_results, dict) or not search_results.get('error')):
                    extractor = ContentExtractor()
                    results_list = search_results if isinstance(search_results, list) else search_results.get('search_results', [])
                    
                    # Extract from ALL sources for comprehensive summaries
                    max_extraction = len(results_list)  # Get ALL content, not limited
                    
                    for i, result in enumerate(results_list[:max_extraction]):
                        status.text(f"📄 Extracting content from source {i+1}/{min(max_extraction, len(results_list))}...")
                        content = safe_api_call(extractor.extract_from_url, result.get('url', ''))
                        if content and content.get('success'):
                            # Store full content, not truncated
                            full_content = {
                                'content': content.get('content', ''),
                                'title': result.get('title', ''),
                                'url': result.get('url', ''),
                                'snippet': result.get('snippet', ''),
                                'domain': result.get('domain', ''),
                                'word_count': len(content.get('content', '').split())
                            }
                            extracted_content.append(full_content)
                        
                        # Update progress for each extraction
                        progress.progress(40 + (i * 20 // max_extraction))
                
                progress.progress(60)
                
                # Step 3: Comprehensive AI Summarization with full content
                status.text("🧠 Generating comprehensive detailed summary with keywords...")
                
                # Combine ALL extracted content for comprehensive summary
                if extracted_content:
                    # Combine full content from all sources
                    full_content_parts = []
                    for content in extracted_content:
                        content_text = content.get('content', '')
                        title = content.get('title', '')
                        url = content.get('url', '')
                        
                        # Add source context
                        source_section = f"\n\n=== SOURCE: {title} ===\nURL: {url}\nContent:\n{content_text}\n\n"
                        full_content_parts.append(source_section)
                    
                    # Also include search snippets for additional context
                    snippet_parts = []
                    for result in results_list:
                        snippet = result.get('snippet', '')
                        if snippet:
                            snippet_parts.append(f"• {snippet}")
                    
                    combined_text = "".join(full_content_parts)
                    if snippet_parts:
                        combined_text += "\n\n=== ADDITIONAL SEARCH SNIPPETS ===\n" + "\n".join(snippet_parts)
                    
                    # Limit total length but keep comprehensive
                    if len(combined_text) > 15000:  # Increased limit for comprehensive summaries
                        combined_text = combined_text[:15000] + "\n\n[Content truncated for processing efficiency]"
                else:
                    # Fallback to detailed search snippets
                    snippet_details = []
                    for result in results_list:
                        title = result.get('title', '')
                        snippet = result.get('snippet', '')
                        url = result.get('url', '')
                        snippet_details.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n---")
                    
                    combined_text = "\n\n".join(snippet_details)
                
                if combined_text:
                    try:
                        summarizer = AISummarizer()
                        
                        # Enhanced summary options for comprehensive output
                        summary_options = {
                            'detailed_formatting': True,  # Always use detailed formatting
                            'include_tables': True,
                            'include_bullet_points': True,
                            'include_keywords': True,  # New option for keywords
                            'comprehensive_mode': True,  # New option for detailed summaries
                            'search_speed': search_speed,
                            'summary_type': 'comprehensive',  # Always comprehensive
                            'source_count': len(extracted_content),
                            'total_content_length': len(combined_text)
                        }
                        
                        # Generate comprehensive summary
                        summary = summarizer.generate_comprehensive_summary(combined_text, query, summary_options)
                        
                        if not summary.get('success'):
                            summary = summarizer.generate_structured_summary(combined_text, query, summary_options)
                            
                        if not summary.get('success'):
                            summary = summarizer.summarize_content(combined_text, query)
                            
                        # Ensure summary is always successful with comprehensive content
                        if not summary.get('success'):
                            summary = {
                                "summary": summarizer._generate_comprehensive_fallback_summary(combined_text, query, len(extracted_content)),
                                "success": True,
                                "provider": "Comprehensive Fallback",
                                "timestamp": datetime.now().isoformat(),
                                "keywords": summarizer._extract_keywords(combined_text, query),
                                "content_analysis": {
                                    "sources_analyzed": len(extracted_content),
                                    "total_words": len(combined_text.split()),
                                    "comprehensive_mode": True
                                }
                            }
                    except Exception as e:
                        logger.error(f"Summarization error: {str(e)}")
                        # Always provide a summary, even if basic
                        summarizer = AISummarizer()
                        summary = {
                            "summary": summarizer._generate_enhanced_fallback_summary(combined_text, query),
                            "success": True,
                            "provider": "Enhanced Fallback",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    # Generate summary even with no content - use search results
                    summarizer = AISummarizer()
                    search_text = " ".join([result.get('snippet', '') for result in results_list[:3]])[:800] if results_list else f"Research query: {query}"
                    summary = {
                        "summary": summarizer._generate_enhanced_fallback_summary(search_text, query),
                        "success": True,
                        "provider": "Enhanced Fallback",
                        "timestamp": datetime.now().isoformat()
                    }
                
                progress.progress(80)
                
                # Enhanced features (speed-optimized)
                historical_data = None
                image_results = None
                
                # Skip heavy processing for quick mode
                if include_trends and HISTORICAL_DATA_AVAILABLE and "Advanced" in search_speed:
                    status.text("📈 Quick trend analysis...")
                    analyzer = HistoricalDataAnalyzer()
                    if "stock" in query.lower() or "market" in query.lower():
                        historical_data = safe_api_call(analyzer.get_stock_trends, 'AAPL', '6m')  # Shorter timeframe
                    else:
                        historical_data = safe_api_call(analyzer.get_market_trends, 'S&P500', '6m')
                
                if include_images and IMAGE_PROCESSING_AVAILABLE and "Advanced" in search_speed:
                    status.text("🖼️ Quick image search...")
                    processor = EnhancedImageProcessor()
                    image_results = safe_api_call(processor.search_high_quality_images, query, 3)  # Fewer images for speed
                
                progress.progress(100)
                
                # Show success message with AI provider info
                provider_used = summary.get('provider', 'Unknown')
                if provider_used != 'Enhanced Fallback':
                    success_msg = f"✅ Research completed! AI Summary by **{provider_used}**"
                else:
                    success_msg = "✅ Research completed! Summary generated"
                
                status.success(success_msg)
                
                # Store results with enhanced information
                st.session_state.research_results = {
                    'query': query,
                    'search_results': search_results,
                    'extracted_content': extracted_content,
                    'summary': summary,
                    'historical_data': historical_data,
                    'image_results': image_results,
                    'timestamp': datetime.now(),
                    'mode': search_mode,
                    'search_speed': search_speed,
                    'keywords': summary.get('keywords', []),
                    'content_analysis': summary.get('content_analysis', {}),
                    'settings': {
                        'num_results': num_results,
                        'include_images': include_images,
                        'include_trends': include_trends,
                        'summary_type': summary_type,
                        'detailed_formatting': detailed_formatting,
                        'include_tables': include_tables,
                        'include_bullet_points': include_bullet_points
                    }
                }
                
                # Generate follow-up questions
                keywords = summary.get('keywords', [])
                follow_up_questions = generate_follow_up_questions(query, summary, keywords)
                st.session_state.research_results['follow_up_questions'] = follow_up_questions
                
                time.sleep(1)
                progress.empty()
                status.empty()
                
            except Exception as e:
                st.error(f"❌ Research failed: {str(e)}")
                logger.error(f"Research error: {str(e)}")
    
    # Display results with enhanced styling
    if st.session_state.research_results:
        display_enhanced_results(st.session_state.research_results)

def generate_follow_up_questions(query: str, summary: Dict, keywords: List[str]) -> List[str]:
    """
    Generate intelligent follow-up questions based on the research summary
    """
    try:
        questions = []
        
        # Extract key themes from summary
        summary_text = summary.get('summary', '').lower()
        
        # Generate topic-specific questions with more variety
        if any(term in query.lower() for term in ['technology', 'ai', 'artificial intelligence', 'machine learning']):
            questions.extend([
                f"What are the latest breakthrough developments in {query}?",
                f"How is {query} being implemented across different industries?",
                f"What are the potential risks and benefits of {query}?",
                f"What future trends and innovations can we expect in {query}?",
                f"What are the ethical considerations surrounding {query}?",
                f"How does {query} compare to alternative approaches?",
                f"What are the technical challenges in implementing {query}?",
                f"What research is currently being conducted on {query}?"
            ])
        
        if any(term in query.lower() for term in ['market', 'business', 'economy', 'finance']):
            questions.extend([
                f"What is the current market size and growth potential for {query}?",
                f"Who are the key players and competitors in the {query} market?",
                f"What are the investment opportunities in {query}?",
                f"How is {query} affecting consumer behavior and preferences?",
                f"What are the regulatory considerations for {query}?",
                f"What are the supply chain implications of {query}?",
                f"How is {query} disrupting traditional business models?",
                f"What are the global market trends for {query}?"
            ])
        
        if any(term in query.lower() for term in ['health', 'medical', 'medicine', 'treatment']):
            questions.extend([
                f"What are the latest clinical trial results for {query}?",
                f"How does {query} compare to existing treatments and therapies?",
                f"What are the side effects or limitations of {query}?",
                f"When will {query} be widely available to patients?",
                f"What are the regulatory approval processes for {query}?",
                f"How effective is {query} across different patient populations?",
                f"What are the cost implications of {query}?",
                f"What research is being conducted to improve {query}?"
            ])
        
        if any(term in query.lower() for term in ['climate', 'environment', 'sustainability', 'green']):
            questions.extend([
                f"What are the latest findings on {query} and its impacts?",
                f"What solutions are being developed to address {query}?",
                f"How is {query} affecting different regions of the world?",
                f"What policies are being implemented regarding {query}?",
                f"What are the economic implications of {query}?",
                f"How can individuals contribute to addressing {query}?",
                f"What technological innovations are helping with {query}?",
                f"What are the long-term projections for {query}?"
            ])
        
        # Generate keyword-based questions
        if keywords:
            for keyword in keywords[:5]:  # Use top 5 keywords
                questions.append(f"Can you explain more about {keyword.title()} in relation to {query}?")
                questions.append(f"How does {keyword.title()} impact the future of {query}?")
                questions.append(f"What are the recent developments in {keyword.title()} within {query}?")
        
        # Generate analysis-based questions
        if 'challenge' in summary_text or 'problem' in summary_text or 'issue' in summary_text:
            questions.append(f"What are the main challenges and obstacles facing {query}?")
            questions.append(f"How can these challenges be effectively overcome?")
            questions.append(f"What resources are needed to address these challenges?")
        
        if 'opportunity' in summary_text or 'potential' in summary_text or 'benefit' in summary_text:
            questions.append(f"What opportunities does {query} present for different sectors?")
            questions.append(f"How can organizations and individuals capitalize on {query}?")
            questions.append(f"What are the long-term benefits of {query}?")
        
        if 'trend' in summary_text or 'future' in summary_text or 'prediction' in summary_text:
            questions.append(f"What are the emerging trends in {query}?")
            questions.append(f"How is {query} expected to evolve in the coming years?")
            questions.append(f"What factors will influence the future of {query}?")
        
        # Generic insightful questions
        questions.extend([
            f"What are the global implications and effects of {query}?",
            f"How has {query} evolved over the past few years?",
            f"What research and studies have been conducted on {query}?",
            f"How does {query} compare internationally across different countries?",
            f"What do experts and researchers predict about {query}?",
            f"What are the different approaches to addressing {query}?",
            f"What role do different stakeholders play in {query}?",
            f"What are the key factors driving changes in {query}?"
        ])
        
        # Remove duplicates and return top 10-12 questions
        unique_questions = list(dict.fromkeys(questions))  # Preserves order while removing duplicates
        return unique_questions[:12]
        
    except Exception as e:
        logger.error(f"Follow-up question generation failed: {str(e)}")
        # Return more diverse fallback questions
        return [
            f"What are the latest developments and breakthroughs in {query}?",
            f"How does {query} impact different industries and sectors?",
            f"What are the future trends and predictions for {query}?",
            f"What are the main challenges and how can they be addressed?",
            f"What opportunities does {query} present for innovation?",
            f"How is {query} being regulated and what are the policies?",
            f"What research is currently being conducted on {query}?",
            f"How does {query} compare globally across different regions?"
        ]

def display_enhanced_results(results):
    """Display results with enhanced styling"""
    
    # Enhanced results header
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 20px; margin: 2rem 0; text-align: center; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
        <h2 style="margin: 0; font-size: 2.2rem;">📊 Research Results</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; opacity: 0.9;">"{results['query']}"</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Enhanced metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Sources", len(results.get('extracted_content', [])), "📚", "#4facfe"),
        ("Results", len(results.get('search_results', [])) if isinstance(results.get('search_results'), list) else len(results.get('search_results', {}).get('search_results', [])), "🔍", "#667eea"),
        ("Mode", "⚡ Quick" if "Quick" in results.get('search_speed', '') else "🔬 Advanced", "🎯", "#764ba2"),
        ("Engine", results.get('mode', 'Standard'), "⚙️", "#fc4a1a"),
        ("Time", results['timestamp'].strftime('%H:%M:%S'), "⏰", "#00f2fe")
    ]
    
    for col, (label, value, icon, color) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f'''
            <div class="metric-card" style="border-left-color: {color};">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {color};">{value}</div>
                <div style="color: #666; font-size: 1rem;">{label}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Enhanced tabs with follow-up questions
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Summary", 
        "🔍 Sources", 
        "🖼️ Images", 
        "📈 Trends", 
        "📄 Export",
        "❓ Follow-up Questions"
    ])
    
    with tab1:
        # Import and use existing display functions with enhanced styling
        from app_working import display_summary_section
        display_summary_section(results)
    
    with tab2:
        from app_working import display_sources_section
        display_sources_section(results)
    
    with tab3:
        from app_working import display_images_section
        display_images_section(results)
    
    with tab4:
        from app_working import display_trends_section
        display_trends_section(results)
    
    with tab5:
        from app_working import display_export_section
        display_export_section(results)
    
    with tab6:
        display_follow_up_questions(results)

if __name__ == "__main__":
    # Network access information with theme support
    network_bg = "rgba(0, 50, 0, 0.3)" if st.session_state.theme_mode == "night" else "rgba(0,255,0,0.1)"
    network_color = "#68d391" if st.session_state.theme_mode == "night" else "#00aa00"
    text_color = "#e2e8f0" if st.session_state.theme_mode == "night" else "white"
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f'''
    <div style="background: {network_bg}; padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 2px solid {network_color};">
        <h4 style="color: {network_color}; margin: 0 0 0.5rem 0;">🌐 Network Access</h4>
        <p style="margin: 0; font-size: 0.9rem; color: {text_color};">This app supports both day and night themes!<br/>Network URL: Check terminal for IP</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: {network_color};">Current: {st.session_state.theme_mode.title()} Theme 🌙 ☀️</p>
    </div>
    ''', unsafe_allow_html=True)
    
    main()