"""
AI Research Agent - Full Features Restored with Error Handling
Includes: Summary, Images, Trends, Sources, Export PDF - All working properly
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

# Page configuration
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling for modern, interactive layout
st.markdown("""
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
    
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4); }
        50% { box-shadow: 0 15px 40px rgba(79, 172, 254, 0.6); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'research_history' not in st.session_state:
    st.session_state.research_history = []

def safe_api_call(func, *args, **kwargs):
    """Safely call API functions with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return {"error": str(e), "success": False}

def main():
    """Main application function"""
    
    # Header with enhanced capabilities
    st.markdown('<h1 style="text-align: center; color: #1f77b4;">🤖 AI Research Agent - Enhanced</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666666;">ChatGPT-Style Analysis • Quick & Advanced Search • Structured Reports</h3>', unsafe_allow_html=True)
    
    # Show feature status with timing
    feature_count = sum([CORE_MODULES_AVAILABLE, ENHANCED_FEATURES_AVAILABLE, HISTORICAL_DATA_AVAILABLE, IMAGE_PROCESSING_AVAILABLE])
    
    status_color = "green" if feature_count >= 3 else "blue" if feature_count >= 2 else "orange"
    status_text = f"⚡ {feature_count}/4 FEATURE SETS ACTIVE"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="background: {status_color}; color: white; padding: 0.5rem; border-radius: 20px; margin: 1rem auto; max-width: 700px;">
            {status_text}: ⚡ Quick Search (5-15s) • 🔬 Advanced Search (30-60s) • 📊 Structured Analysis • 📄 Professional Export
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status
        try:
            config = Config()
            validation = config.validate_api_keys()
            st.subheader("📊 API Status")
            st.write(f"**Working APIs:** {validation.get('working_count', 0)}")
            if validation.get('search_engines'):
                st.write(f"🔍 **Search:** {', '.join(validation['search_engines'])}")
        except Exception as e:
            st.error(f"Config error: {str(e)}")
        
        # Research settings
        st.subheader("🔍 Research Settings")
        
        # NEW: Search Speed Options
        search_speed = st.radio(
            "🚀 Search Speed",
            ["⚡ Quick Search (5-15 seconds)", "🔬 Advanced Search (30-60 seconds)"],
            help="Quick: Fast results with basic analysis | Advanced: Comprehensive research with detailed analysis"
        )
        
        # Dynamic settings based on search speed
        if "Quick" in search_speed:
            num_results = st.slider("Number of results", 3, 8, 5)
            search_mode = "Standard"
            include_images = st.checkbox("Include images", value=False)
            include_trends = st.checkbox("Include trend analysis", value=False)
            summary_type = "brief"
            st.info("⚡ Quick mode: Optimized for speed with essential information")
        else:
            num_results = st.slider("Number of results", 10, 25, 15)
            search_mode = st.radio("Search Mode", ["Enhanced", "Standard"]) if ENHANCED_FEATURES_AVAILABLE else "Standard"
            include_images = st.checkbox("Include images", value=True)
            include_trends = st.checkbox("Include trend analysis", value=True)
            summary_type = st.selectbox("Summary type", ["comprehensive", "detailed", "brief"])
            st.info("🔬 Advanced mode: Comprehensive analysis with detailed insights")
        
        enable_visualizations = st.checkbox("Enable charts", value=True)
        
        # NEW: Output Format Options
        st.subheader("📋 Output Format")
        detailed_formatting = st.checkbox("📝 ChatGPT-style detailed formatting", value=True, help="Bullet points, headings, tables, structured analysis")
        include_tables = st.checkbox("📊 Include data tables", value=True)
        include_bullet_points = st.checkbox("• Enhanced bullet points", value=True)
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🔍 Research Query")
        query = st.text_input(
            "Enter your research topic:",
            placeholder="e.g., Latest AI developments, Climate change solutions, Technology trends",
            value=st.session_state.search_query
        )
        search_button = st.button("🚀 Start Research", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("💪 Quick Examples")
        examples = [
            ("⚡ AI trends 2024", "AI trends 2024"), 
            ("🌍 Climate change", "Climate change"), 
            ("🚀 Space exploration", "Space exploration"), 
            ("⚕️ Medical research", "Medical research"), 
            ("📱 Technology news", "Technology news")
        ]
        for display_text, example in examples:
            if st.button(display_text, use_container_width=True):
                st.session_state.search_query = example
                st.rerun()
    
    # Research execution
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
                
                # Step 2: Content extraction
                status.text("📄 Extracting content...")
                extracted_content = []
                
                if search_results and (not isinstance(search_results, dict) or not search_results.get('error')):
                    extractor = ContentExtractor()
                    results_list = search_results if isinstance(search_results, list) else search_results.get('search_results', [])
                    
                    for result in results_list[:5]:
                        content = safe_api_call(extractor.extract_from_url, result.get('url', ''))
                        if content and content.get('success'):
                            extracted_content.append(content)
                
                progress.progress(60)
                
                # Step 3: AI Summarization
                status.text("🧠 Generating AI summary...")
                
                # Prepare content based on search speed
                if "Quick" in search_speed:
                    # Quick mode: Use search snippets primarily
                    search_text = " ".join([result.get('snippet', '')[:300] for result in results_list[:5]])[:2000]
                    combined_text = search_text
                else:
                    # Advanced mode: Use full extracted content
                    combined_text = " ".join([content.get('content', '')[:1500] for content in extracted_content])[:5000]
                    if not combined_text:  # Fallback to search snippets
                        combined_text = " ".join([result.get('snippet', '')[:500] for result in results_list[:8]])[:3000]
                
                if combined_text:
                    try:
                        summarizer = AISummarizer()
                        
                        # Enhanced summarization with formatting options
                        summary_options = {
                            'detailed_formatting': detailed_formatting,
                            'include_tables': include_tables,
                            'include_bullet_points': include_bullet_points,
                            'search_speed': search_speed,
                            'summary_type': summary_type
                        }
                        
                        summary = summarizer.generate_structured_summary(combined_text, query, summary_options)
                        
                        # Ensure we have a valid summary structure
                        if not summary.get('success'):
                            # Try with basic summarization as fallback
                            summary = summarizer.summarize_content(combined_text, query)
                    except Exception as e:
                        logger.error(f"Summarization error: {str(e)}")
                        summary = {
                            "summary": f"Research completed for '{query}'. Please check the Sources tab for detailed information from {len(extracted_content)} extracted sources and {len(results_list)} search results.",
                            "success": True,
                            "provider": "Fallback",
                            "error": str(e)
                        }
                else:
                    # Fallback: summarize search results snippets
                    search_text = " ".join([result.get('snippet', '') for result in results_list[:5]])[:2000]
                    if search_text:
                        try:
                            summarizer = AISummarizer()
                            summary = summarizer.summarize_content(search_text, query)
                        except Exception as e:
                            summary = {
                                "summary": f"Search completed for '{query}' with {len(results_list)} results found. Detailed information is available in the Sources section.",
                                "success": True,
                                "provider": "Basic"
                            }
                    else:
                        summary = {
                            "summary": f"Research query '{query}' has been processed. Please check the Sources tab for available information.",
                            "success": True,
                            "provider": "Basic"
                        }
                
                progress.progress(80)
                
                # Step 4: Enhanced features
                historical_data = None
                image_results = None
                
                if include_trends and HISTORICAL_DATA_AVAILABLE:
                    status.text("📈 Analyzing trends...")
                    analyzer = HistoricalDataAnalyzer()
                    if "stock" in query.lower() or "market" in query.lower():
                        historical_data = safe_api_call(analyzer.get_stock_trends, 'AAPL', '1y')
                    else:
                        historical_data = safe_api_call(analyzer.get_market_trends, 'S&P500', '1y')
                
                if include_images and IMAGE_PROCESSING_AVAILABLE:
                    status.text("🖼️ Finding images...")
                    processor = EnhancedImageProcessor()
                    image_results = safe_api_call(processor.search_high_quality_images, query, 5)
                
                progress.progress(100)
                status.text("✅ Research completed!")
                
                # Store comprehensive results
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
                
                # Add to history
                st.session_state.research_history.append({
                    'query': query,
                    'timestamp': datetime.now(),
                    'mode': search_mode
                })
                
                time.sleep(1)
                progress.empty()
                status.empty()
                
            except Exception as e:
                st.error(f"❌ Research failed: {str(e)}")
                logger.error(f"Research error: {str(e)}")
    
    # Display comprehensive results
    if st.session_state.research_results:
        display_comprehensive_results(st.session_state.research_results)

def display_comprehensive_results(results):
    """Display comprehensive research results with all original features"""
    
    st.divider()
    st.header(f"📊 Research Results: \"{results['query']}\"")
    
    # Enhanced metrics with interactive cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Sources", len(results.get('extracted_content', [])), "📚", "#4facfe"),
        ("Results", len(results.get('search_results', [])) if isinstance(results.get('search_results'), list) else len(results.get('search_results', {}).get('search_results', [])), "🔍", "#667eea"),
        ("Mode", "⚡ Quick" if "Quick" in results.get('search_speed', '') else "🔬 Advanced", "🎯", "#764ba2"),
        ("Engine", results.get('mode', 'Standard'), "⚙️", "#fc4a1a"),
        ("Time", results['timestamp'].strftime('%H:%M:%S'), "⏰", "#00f2fe")
    ]
    
    for i, (col, (label, value, icon, color)) in enumerate(zip([col1, col2, col3, col4, col5], metrics)):
        with col:
            st.markdown(f'''
            <div class="metric-container" style="background: linear-gradient(135deg, {color}15 0%, {color}05 100%); border-left: 4px solid {color};">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: {color};">{value}</div>
                    <div style="color: #666; font-size: 0.9rem;">{label}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Main content tabs - FULL FUNCTIONALITY RESTORED
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Summary", "🔍 Sources", "🖼️ Images", "📈 Trends", "📄 Export"])
    
    with tab1:
        display_summary_section(results)
    
    with tab2:
        display_sources_section(results)
    
    with tab3:
        display_images_section(results)
    
    with tab4:
        display_trends_section(results)
    
    with tab5:
        display_export_section(results)

def display_summary_section(results):
    """Display enhanced AI summary with ChatGPT-style formatting"""
    summary = results.get('summary', {})
    settings = results.get('settings', {})
    
    if summary and summary.get('success'):
        st.subheader("📝 AI-Generated Research Analysis")
        
        # Enhanced provider info with formatting details
        provider = summary.get('provider', 'Unknown')
        format_type = summary.get('format_type', 'standard')
        is_structured = summary.get('structured', False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if provider == 'Gemini':
                st.success(f"🚀 Generated by Google Gemini (Free AI)")
            elif provider == 'Enhanced Structured Fallback':
                st.info(f"⚡ Generated by Enhanced Analysis (No API needed)")
            elif provider in ['Hugging Face', 'Cohere', 'Together AI', 'Ollama (Local)']:
                st.success(f"🤖 Generated by {provider}")
            elif provider in ['Perplexity', 'Anthropic', 'OpenAI']:
                st.success(f"🧠 Generated by {provider}")
            else:
                st.info(f"📊 Generated by: {provider}")
        
        with col2:
            if is_structured:
                st.success("📋 Structured Format (ChatGPT-style)")
            else:
                st.info("📄 Standard Format")
        
        with col3:
            if format_type == 'quick':
                st.info("⚡ Quick Analysis (Optimized)")
            elif format_type == 'advanced':
                st.success("🔬 Advanced Analysis (Comprehensive)")
            else:
                st.info("📊 Standard Analysis")
        
        st.divider()
        
        # Display the enhanced structured summary
        summary_text = summary.get('summary', 'No summary content available')
        
        # Check if it's structured content and render appropriately
        if is_structured and '##' in summary_text:
            # Enhanced rendering for structured content
            st.markdown(summary_text)
        else:
            # Standard rendering
            st.markdown(summary_text)
        
        # Show additional structured details if available
        if summary.get('key_findings'):
            st.markdown("---")
            st.subheader("🎯 Key Findings")
            for i, finding in enumerate(summary['key_findings'], 1):
                st.markdown(f"**{i}.** {finding}")
        
        if summary.get('technical_details'):
            st.markdown("---")
            st.subheader("🔧 Technical Details")
            for detail in summary['technical_details']:
                st.markdown(f"• {detail}")
        
        # Performance metrics with enhanced info
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if summary.get('timestamp'):
                st.caption(f"⏰ Generated: {summary.get('timestamp', '')[:19]}")
        with col2:
            st.caption(f"📝 Length: {len(summary_text):,} characters")
        with col3:
            if settings.get('detailed_formatting'):
                st.caption("✨ Enhanced formatting enabled")
            else:
                st.caption("📄 Standard formatting")
        with col4:
            search_speed = results.get('search_speed', '')
            if 'Quick' in search_speed:
                st.caption("⚡ Quick mode (5-15s)")
            else:
                st.caption("🔬 Advanced mode (30-60s)")
    
    else:
        st.warning("❌ Summary generation encountered issues")
        
        # Show error details if available
        if summary and summary.get('error'):
            st.error(f"Error: {summary['error']}")
        
        # Enhanced guidance based on search mode
        search_speed = results.get('search_speed', '')
        if 'Quick' in search_speed:
            st.info("💡 **Quick Search Troubleshooting:**")
            st.markdown("""
            - Try a more specific search query
            - Switch to **Advanced Search** for better AI analysis
            - Check the **Sources** tab for available information
            - Some topics may need more detailed search
            """)
        else:
            st.info("💡 **What you can do:**")
            st.markdown("""
            - Check the **Sources** tab for detailed information
            - The search found content that you can review manually
            - Try a more specific search query
            - Some AI providers may have quota limits
            """)
        
        # Show available alternatives with quick setup
        with st.expander("🔧 Enable AI Summaries (Free Setup)"):
            st.markdown("""
            **Quick Setup (2 minutes):**
            1. **Google Gemini** (Free, unlimited): 
               - Go to: https://makersuite.google.com/app/apikey
               - Create free account → Generate API key
               - Add to .env file: `GEMINI_API_KEY=your_key`
            
            2. **Hugging Face** (Free, 1000 requests/month):
               - Go to: https://huggingface.co/settings/tokens  
               - Create account → Generate token
               - Add to .env file: `HUGGINGFACE_API_KEY=your_key`
            
            3. Restart the application
            
            **Result**: Reliable AI summaries with structured formatting!
            """)

def display_sources_section(results):
    """Display enhanced sources information with tables and structured data"""
    search_results = results.get('search_results', [])
    extracted_content = results.get('extracted_content', [])
    settings = results.get('settings', {})
    
    # Handle different result formats
    if isinstance(search_results, dict):
        sources_list = search_results.get('search_results', [])
        if search_results.get('search_time'):
            st.info(f"⚡ Search completed in {search_results['search_time']} seconds")
    else:
        sources_list = search_results
    
    # Enhanced overview with data table
    st.subheader("📊 Sources Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔍 Search Results", len(sources_list))
    with col2:
        st.metric("📄 Content Extracted", len(extracted_content))
    with col3:
        domains = list(set([source.get('domain', 'Unknown') for source in sources_list]))
        st.metric("🌐 Unique Domains", len(domains))
    with col4:
        search_speed = results.get('search_speed', '')
        mode = "Quick" if "Quick" in search_speed else "Advanced"
        st.metric("🎯 Search Mode", mode)
    
    if sources_list:
        # Enhanced sources display with table option
        display_format = st.radio(
            "Display Format:", 
            ["📋 Detailed Cards", "📊 Data Table", "📝 Compact List"]
        )
        
        if display_format == "📊 Data Table" and settings.get('include_tables', True):
            # Create data table
            table_data = []
            for i, source in enumerate(sources_list[:20], 1):
                table_data.append({
                    "#": i,
                    "Title": source.get('title', 'Untitled')[:60] + ('...' if len(source.get('title', '')) > 60 else ''),
                    "Domain": source.get('domain', 'Unknown'),
                    "Relevance": f"{source.get('score', 0.8):.1f}/1.0" if source.get('score') else "High",
                    "Type": source.get('source', 'Web')
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Download table option
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download Sources Table (CSV)",
                csv,
                file_name=f"sources_{results['query'][:20]}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
            
        elif display_format == "📝 Compact List":
            # Compact list view
            for i, source in enumerate(sources_list[:15], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{i}.** [{source.get('title', 'Untitled')[:80]}]({source.get('url', '#')})")
                    st.caption(f"🌐 {source.get('domain', 'Unknown')} | {source.get('snippet', 'No description')[:100]}...")
                with col2:
                    if source.get('score'):
                        st.metric("Relevance", f"{source['score']:.2f}")
                    st.caption(f"📄 {source.get('source', 'Web')}")
        
        else:  # Detailed Cards (default)
            st.subheader(f"🔍 Search Sources ({len(sources_list)} found)")
            
            for i, source in enumerate(sources_list[:15], 1):
                with st.expander(f"{i}. {source.get('title', 'Untitled')[:80]}..."):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**🔗 URL:** [{source.get('url', 'N/A')}]({source.get('url', '#')})")
                        st.markdown(f"**📝 Description:** {source.get('snippet', 'No description available')[:400]}...")
                        if source.get('domain'):
                            st.markdown(f"**🌐 Domain:** {source['domain']}")
                    
                    with col2:
                        if source.get('score'):
                            st.metric("🎯 Relevance", f"{source['score']:.2f}/1.0")
                        if source.get('source'):
                            st.caption(f"🔍 Engine: {source['source']}")
                        if source.get('date'):
                            st.caption(f"📅 Date: {source['date']}")
    
    # Enhanced extracted content display
    if extracted_content:
        st.markdown("---")
        st.subheader(f"📄 Extracted Content ({len(extracted_content)} sources)")
        
        content_format = st.radio(
            "Content Display:",
            ["📖 Full Content", "📊 Content Summary Table"]
        )
        
        if content_format == "📊 Content Summary Table":
            content_table = []
            for i, content in enumerate(extracted_content[:10], 1):
                content_table.append({
                    "Source": i,
                    "Title": content.get('title', 'Untitled')[:50] + ('...' if len(content.get('title', '')) > 50 else ''),
                    "Domain": content.get('domain', 'Unknown'),
                    "Words": content.get('word_count', 0),
                    "Content Preview": content.get('text', '')[:100] + '...' if content.get('text') else 'No content'
                })
            
            content_df = pd.DataFrame(content_table)
            st.dataframe(content_df, use_container_width=True, hide_index=True)
        
        else:  # Full content display
            for i, content in enumerate(extracted_content[:10], 1):
                with st.expander(f"Content {i}: {content.get('title', 'Untitled')[:60]}..."):
                    if content.get('content'):
                        text = content['content'][:1200]
                        st.markdown(text + "..." if len(content['content']) > 1200 else text)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if content.get('word_count'):
                            st.caption(f"📊 Words: {content['word_count']:,}")
                    with col2:
                        if content.get('domain'):
                            st.caption(f"🌐 {content['domain']}")
                    with col3:
                        if content.get('url'):
                            st.caption(f"🔗 [Source]({content['url']})")
    
    if not sources_list and not extracted_content:
        st.warning("🚨 No sources found")
        search_speed = results.get('search_speed', '')
        if 'Quick' in search_speed:
            st.info("💡 **Quick Search Tips:**\n- Try more specific keywords\n- Switch to Advanced Search for broader coverage\n- Check your internet connection")
        else:
            st.info("💡 **Troubleshooting:**\n- Refine your search query\n- Try different keywords\n- Check your internet connection\n- Some topics may have limited online sources")

def display_images_section(results):
    """Display images with comprehensive analysis"""
    image_results = results.get('image_results')
    search_results = results.get('search_results', [])
    
    # Check for enhanced image results
    if image_results and image_results.get('success'):
        st.subheader(f"🖼️ Enhanced Images ({image_results.get('total_found', 0)} found)")
        
        images = image_results.get('images', [])
        cols_per_row = 3
        for i in range(0, len(images), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(images):
                    img = images[idx]
                    with col:
                        if img.get('thumbnail'):
                            try:
                                st.image(img['thumbnail'], caption=img.get('title', 'Image')[:50], use_column_width=True)
                            except:
                                st.write(f"🖼️ {img.get('title', 'Image')}")
                        st.caption(f"Source: {img.get('source', 'Unknown')}")
                        if img.get('quality_score'):
                            st.caption(f"Quality: {img['quality_score']}/10")
    
    # Fall back to search result images
    else:
        if isinstance(search_results, dict):
            results_list = search_results.get('search_results', [])
        else:
            results_list = search_results
        
        image_urls = [r for r in results_list if r.get('image_url') or r.get('result_type') == 'image']
        
        if image_urls:
            st.subheader(f"🖼️ Search Images ({len(image_urls)} found)")
            cols = st.columns(3)
            for i, img in enumerate(image_urls[:9]):
                with cols[i % 3]:
                    img_url = img.get('image_url') or img.get('url')
                    if img_url:
                        try:
                            st.image(img_url, caption=img.get('title', 'Image')[:40], use_column_width=True)
                        except:
                            st.write(f"🖼️ {img.get('title', 'Image')}")
        else:
            st.info("🖼️ No images found. Try enabling image search or use a more visual query.")

def display_trends_section(results):
    """Display trend analysis and historical data"""
    historical_data = results.get('historical_data')
    
    if historical_data and historical_data.get('success'):
        st.subheader("📈 Historical Trend Analysis")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Value", f"${historical_data.get('current_price', 0):.2f}")
        with col2:
            change_pct = historical_data.get('price_change_pct', 0)
            st.metric("Change %", f"{change_pct:+.2f}%", delta=f"{change_pct:+.2f}%")
        with col3:
            st.metric("Data Points", historical_data.get('data_points', 0))
        with col4:
            st.metric("Trend", historical_data.get('trend', 'N/A'))
        
        # Chart display
        if historical_data.get('chart_html'):
            st.components.v1.html(historical_data['chart_html'], height=500, scrolling=True)
        
        # Summary
        if historical_data.get('summary'):
            st.markdown("### 📊 Analysis Summary")
            st.markdown(historical_data['summary'])
    
    # Basic trend analysis from sources
    search_results = results.get('search_results', [])
    if isinstance(search_results, dict):
        sources = search_results.get('search_results', [])
    else:
        sources = search_results
    
    if sources:
        st.subheader("📊 Source Distribution")
        domains = [s.get('domain', 'Unknown') for s in sources if s.get('domain')]
        if domains:
            domain_counts = pd.Series(domains).value_counts().head(8)
            fig = px.bar(x=domain_counts.values, y=domain_counts.index, orientation='h', 
                        title='Top Source Domains', labels={'x': 'Count', 'y': 'Domain'})
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def display_export_section(results):
    """Display comprehensive export options"""
    st.subheader("📥 Export Research Results")
    
    # Show export readiness status
    summary_available = results.get('summary', {}).get('success', False)
    sources_available = len(results.get('search_results', {}).get('search_results', [])) > 0 if isinstance(results.get('search_results'), dict) else len(results.get('search_results', [])) > 0
    content_available = len(results.get('extracted_content', [])) > 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Summary", "✅ Ready" if summary_available else "⚠️ Limited")
    with col2:
        st.metric("🔍 Sources", "✅ Ready" if sources_available else "❌ None")
    with col3:
        st.metric("📄 Content", "✅ Ready" if content_available else "❌ None")
    
    if not (summary_available or sources_available or content_available):
        st.warning("⚠️ No content available for export. Please run a search first.")
        return
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 Document Formats:**")
        
        # PDF Export
        if st.button("📄 Export as PDF", use_container_width=True):
            try:
                with st.spinner("Generating comprehensive PDF report..."):
                    pdf_gen = PDFGenerator()
                    pdf_content = pdf_gen.generate_pdf(results)
                    
                    if isinstance(pdf_content, bytes) and len(pdf_content) > 0:
                        st.download_button(
                            "📥 Download PDF Report",
                            pdf_content,
                            file_name=f"research_{results['query'][:30]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF report ready for download!")
                        st.info(f"📋 Report includes: {'Summary, ' if summary_available else ''}Sources{', Content' if content_available else ''}")
                    else:
                        st.error("❌ PDF generation failed - Invalid content")
            except Exception as e:
                st.error(f"PDF export error: {str(e)}")
                st.info("💡 Tip: Try a simpler query or check your API configuration")
        
        # Markdown Export
        if st.button("📝 Export as Markdown", use_container_width=True):
            try:
                md_content = generate_markdown_export(results)
                st.download_button(
                    "📥 Download Markdown",
                    md_content,
                    file_name=f"research_{results['query'][:30]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                st.success("✅ Markdown ready for download!")
            except Exception as e:
                st.error(f"Markdown export error: {str(e)}")
    
        
    with col2:
        st.markdown("**📊 Data Formats:**")
        
        # JSON Export
        if st.button("📊 Export as JSON", use_container_width=True):
            try:
                json_data = json.dumps(results, indent=2, default=str)
                st.download_button(
                    "📥 Download JSON",
                    json_data,
                    file_name=f"research_{results['query'][:30]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                st.success("✅ JSON data ready!")
            except Exception as e:
                st.error(f"JSON export error: {str(e)}")
        
        # CSV Export
        if st.button("📈 Export Sources CSV", use_container_width=True):
            try:
                csv_content = generate_csv_export(results)
                st.download_button(
                    "📥 Download CSV",
                    csv_content,
                    file_name=f"sources_{results['query'][:30]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                st.success("✅ CSV data ready!")
            except Exception as e:
                st.error(f"CSV export error: {str(e)}")
    
    # Show export tips
    with st.expander("💡 Export Tips"):
        st.markdown("""
        - **PDF**: Best for sharing complete research reports
        - **Markdown**: Great for documentation and GitHub
        - **JSON**: Perfect for developers and data analysis
        - **CSV**: Ideal for spreadsheet analysis of sources
        """)

def generate_markdown_export(results):
    """Generate comprehensive markdown export"""
    try:
        md = f"# Research Report: {results.get('query', 'Unknown Query')}\n\n"
        md += f"**Generated:** {results.get('timestamp', datetime.now().isoformat())}\n"
        md += f"**Mode:** {results.get('mode', 'Standard')}\n\n"
        
        # Summary
        summary = results.get('summary', {})
        if summary and summary.get('success'):
            md += "## Summary\n\n"
            md += summary.get('summary', 'No summary available') + "\n\n"
            md += f"*Generated by: {summary.get('provider', 'AI System')}*\n\n"
        
        # AI Summaries (if available)
        summaries = results.get('summaries', {})
        if isinstance(summaries, dict):
            if summaries.get('executive_summary'):
                md += "## Executive Summary\n\n"
                md += summaries['executive_summary'] + "\n\n"
            
            if summaries.get('key_findings'):
                md += "## Key Findings\n\n"
                for i, finding in enumerate(summaries['key_findings'], 1):
                    md += f"{i}. {finding}\n"
                md += "\n"
        
        # Sources
        search_results = results.get('search_results', [])
        sources = search_results if isinstance(search_results, list) else search_results.get('search_results', [])
        if sources:
            md += "## Sources\n\n"
            for i, source in enumerate(sources[:10], 1):
                title = source.get('title', 'Untitled')
                url = source.get('url', 'N/A')
                snippet = source.get('snippet', 'No description')[:200]
                md += f"{i}. **{title}**\n"
                md += f"   - URL: {url}\n"
                md += f"   - Description: {snippet}...\n\n"
        
        return md
        
    except Exception as e:
        return f"# Research Report\n\nError generating markdown: {str(e)}\n"

def generate_csv_export(results):
    """Generate CSV export for sources"""
    try:
        search_results = results.get('search_results', [])
        sources = search_results if isinstance(search_results, list) else search_results.get('search_results', [])
        
        csv = "Title,URL,Description,Source,Domain\n"
        for source in sources:
            title = str(source.get('title', 'Untitled')).replace(',', ';').replace('"', "'")
            url = str(source.get('url', 'N/A')).replace(',', ';')
            desc = str(source.get('snippet', 'No description')).replace(',', ';')[:200]
            src = str(source.get('source', 'Unknown')).replace(',', ';')
            domain = str(source.get('domain', 'Unknown')).replace(',', ';')
            csv += f'"{title}","{url}","{desc}","{src}","{domain}"\n'
        
        return csv if len(sources) > 0 else "Title,URL,Description,Source,Domain\nNo sources available,,,,,\n"
        
    except Exception as e:
        return f"Title,URL,Description,Source,Domain\nError generating CSV: {str(e)},,,,\n"

if __name__ == "__main__":
    main()