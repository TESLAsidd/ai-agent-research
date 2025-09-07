"""
AI Research Agent - Fixed Version with Better Error Handling
A comprehensive research assistant that searches, extracts, and summarizes information
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import os
import base64
import io
import logging
from typing import Dict, List
import numpy as np
from PIL import Image
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import core modules with error handling
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

# Enhanced modules (optional)
ENHANCED_FEATURES_AVAILABLE = False
HISTORICAL_DATA_AVAILABLE = False
IMAGE_PROCESSING_AVAILABLE = False

try:
    from modules.enhanced_search import EnhancedSearchEngine
    from modules.enhanced_ai import EnhancedSummarizer, MultiAIProvider
    ENHANCED_FEATURES_AVAILABLE = True
    logger.info("✅ Enhanced search and AI modules loaded")
except ImportError as e:
    logger.warning(f"Enhanced search/AI not available: {e}")

try:
    from modules.historical_data import HistoricalDataAnalyzer
    HISTORICAL_DATA_AVAILABLE = True
    logger.info("✅ Historical data module loaded")
except ImportError as e:
    logger.warning(f"Historical data not available: {e}")

try:
    from modules.enhanced_images import EnhancedImageProcessor
    IMAGE_PROCESSING_AVAILABLE = True
    logger.info("✅ Enhanced images module loaded")
except ImportError as e:
    logger.warning(f"Enhanced images not available: {e}")

# Optional modules
try:
    from modules.cache_manager import cache_manager
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False
    cache_manager = None

try:
    from modules.image_analyzer import ImageAnalyzer
    IMAGE_ANALYSIS_AVAILABLE = True
except ImportError:
    IMAGE_ANALYSIS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
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
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Research Agent</h1>', unsafe_allow_html=True)
    
    # Feature status
    feature_count = sum([
        CORE_MODULES_AVAILABLE,
        ENHANCED_FEATURES_AVAILABLE, 
        HISTORICAL_DATA_AVAILABLE,
        IMAGE_PROCESSING_AVAILABLE
    ])
    
    if feature_count >= 3:
        status_color = "green"
        status_text = "FULL FEATURES ACTIVE"
    elif feature_count >= 2:
        status_color = "blue" 
        status_text = "ENHANCED MODE"
    else:
        status_color = "orange"
        status_text = "BASIC MODE"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="background: {status_color}; color: white; padding: 0.5rem; border-radius: 20px; margin: 1rem auto; max-width: 600px;">
            ⚡ {status_text}: {feature_count}/4 Feature Sets Available
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Show available features
        st.subheader("📋 Available Features")
        st.write(f"✅ Core Research" if CORE_MODULES_AVAILABLE else "❌ Core Research")
        st.write(f"✅ Enhanced Search" if ENHANCED_FEATURES_AVAILABLE else "❌ Enhanced Search")  
        st.write(f"✅ Historical Data" if HISTORICAL_DATA_AVAILABLE else "❌ Historical Data")
        st.write(f"✅ Image Processing" if IMAGE_PROCESSING_AVAILABLE else "❌ Image Processing")
        st.write(f"✅ Caching" if CACHE_AVAILABLE else "❌ Caching")
        
        # API Status
        try:
            config = Config()
            validation = config.validate_api_keys()
            
            st.subheader("📊 API Status")
            st.write(f"**Working APIs:** {validation.get('working_count', 0)}")
            
            if validation.get('search_engines'):
                st.write("🔍 **Search:**", ", ".join(validation['search_engines']))
            if validation.get('ai_providers'):
                st.write("🧠 **AI:**", ", ".join(validation['ai_providers']))
                
        except Exception as e:
            st.error(f"Configuration error: {str(e)}")
        
        # Research settings
        st.subheader("🔍 Research Settings")
        num_results = st.slider("Number of results", 3, 15, 8)
        
        if ENHANCED_FEATURES_AVAILABLE:
            search_mode = st.radio("Search Mode", ["Enhanced", "Standard"])
        else:
            search_mode = "Standard"
            st.info("Enhanced mode requires additional modules")
            
        if HISTORICAL_DATA_AVAILABLE:
            include_trends = st.checkbox("Include trend analysis", value=True)
        else:
            include_trends = False
            
        if IMAGE_PROCESSING_AVAILABLE:
            include_images = st.checkbox("Include images", value=True)
        else:
            include_images = False
    
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
        st.subheader("💡 Quick Examples")
        examples = [
            "AI trends 2024",
            "Renewable energy",
            "Space exploration", 
            "Medical breakthroughs",
            "Tech innovations"
        ]
        
        for example in examples:
            if st.button(f"📌 {example}", use_container_width=True):
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
                progress.progress(25)
                
                if search_mode == "Enhanced" and ENHANCED_FEATURES_AVAILABLE:
                    try:
                        enhanced_search = EnhancedSearchEngine()
                        search_results = safe_api_call(
                            enhanced_search.fast_search_and_analyze, 
                            query, 
                            num_results
                        )
                    except Exception as e:
                        st.warning(f"Enhanced search failed, using standard: {str(e)}")
                        search_engine = WebSearchEngine()
                        search_results = safe_api_call(search_engine.search, query, num_results)
                else:
                    search_engine = WebSearchEngine()
                    search_results = safe_api_call(search_engine.search, query, num_results)
                
                progress.progress(50)
                
                # Step 2: Content extraction
                status.text("📄 Extracting content...")
                extracted_content = []
                
                if isinstance(search_results, list) and search_results:
                    extractor = ContentExtractor()
                    for result in search_results[:5]:  # Limit to prevent timeouts
                        try:
                            content = safe_api_call(extractor.extract_content, result.get('url', ''))
                            if content and content.get('success'):
                                extracted_content.append(content)
                        except Exception as e:
                            logger.warning(f"Content extraction failed for {result.get('url', '')}: {e}")
                            continue
                
                progress.progress(75)
                
                # Step 3: AI Summarization
                status.text("🧠 Generating summary...")
                
                # Combine content for summarization
                combined_text = " ".join([
                    content.get('content', '')[:1000] 
                    for content in extracted_content
                ])[:3000]  # Limit text length
                
                if combined_text:
                    summarizer = AISummarizer()
                    summary = safe_api_call(
                        summarizer.summarize_content,
                        combined_text,
                        query
                    )
                else:
                    summary = {"summary": "No content could be extracted for summarization.", "success": False}
                
                progress.progress(100)
                status.text("✅ Research completed!")
                
                # Store results
                st.session_state.research_results = {
                    'query': query,
                    'search_results': search_results,
                    'extracted_content': extracted_content,
                    'summary': summary,
                    'timestamp': datetime.now(),
                    'mode': search_mode
                }
                
                time.sleep(1)
                progress.empty()
                status.empty()
                
            except Exception as e:
                st.error(f"❌ Research failed: {str(e)}")
                logger.error(f"Research error: {str(e)}")
    
    # Display results
    if st.session_state.research_results:
        results = st.session_state.research_results
        
        st.divider()
        st.header("📋 Research Results")
        
        # Summary section
        if results.get('summary') and results['summary'].get('success'):
            st.subheader("📝 AI Summary")
            st.markdown(results['summary'].get('summary', 'No summary available'))
        
        # Search results section
        if results.get('search_results'):
            st.subheader(f"🔍 Search Results ({len(results['search_results'])} found)")
            
            if isinstance(results['search_results'], dict) and results['search_results'].get('search_results'):
                # Enhanced search format
                search_data = results['search_results']['search_results']
            elif isinstance(results['search_results'], list):
                # Standard search format
                search_data = results['search_results']
            else:
                search_data = []
            
            for i, result in enumerate(search_data[:10], 1):
                with st.expander(f"{i}. {result.get('title', 'Untitled')[:80]}..."):
                    st.write(f"**URL:** {result.get('url', 'N/A')}")
                    st.write(f"**Snippet:** {result.get('snippet', 'No description available')[:300]}...")
                    if result.get('source'):
                        st.write(f"**Source:** {result['source']}")
        
        # Export options
        st.subheader("📥 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                try:
                    pdf_gen = PDFGenerator()
                    pdf_content = pdf_gen.generate_pdf(results)
                    st.download_button(
                        "Download PDF",
                        pdf_content,
                        file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"PDF export failed: {str(e)}")
        
        with col2:
            if st.button("📝 Export Markdown", use_container_width=True):
                try:
                    md_content = f"# Research: {results['query']}\\n\\n"
                    md_content += f"**Generated:** {results['timestamp']}\\n\\n"
                    if results.get('summary') and results['summary'].get('summary'):
                        md_content += f"## Summary\\n{results['summary']['summary']}\\n\\n"
                    
                    st.download_button(
                        "Download Markdown",
                        md_content,
                        file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Markdown export failed: {str(e)}")
        
        with col3:
            if st.button("📊 Export JSON", use_container_width=True):
                try:
                    json_data = json.dumps(results, default=str, indent=2)
                    st.download_button(
                        "Download JSON",
                        json_data,
                        file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"JSON export failed: {str(e)}")
    
    # Test functions section
    st.divider()
    st.subheader("🧪 Test Enhanced Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Test Search", use_container_width=True):
            try:
                search_engine = WebSearchEngine()
                test_results = safe_api_call(search_engine.search, "Python programming", 3)
                if test_results and not test_results.get('error'):
                    st.success(f"✅ Search working! Found {len(test_results)} results")
                else:
                    st.error(f"❌ Search failed: {test_results.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Search test error: {str(e)}")
    
    with col2:
        if HISTORICAL_DATA_AVAILABLE and st.button("📈 Test Market Data", use_container_width=True):
            try:
                analyzer = HistoricalDataAnalyzer()
                result = safe_api_call(analyzer.get_stock_trends, 'AAPL', '1y')
                if result and result.get('success'):
                    st.success("✅ Market data working!")
                    st.metric("AAPL Price", f"${result.get('current_price', 0):.2f}")
                else:
                    st.error(f"❌ Market data failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Market test error: {str(e)}")
        elif not HISTORICAL_DATA_AVAILABLE:
            st.button("📈 Market Data (Unavailable)", disabled=True, use_container_width=True)
    
    with col3:
        if IMAGE_PROCESSING_AVAILABLE and st.button("🖼️ Test Images", use_container_width=True):
            try:
                processor = EnhancedImageProcessor()
                result = safe_api_call(processor.search_high_quality_images, 'technology', 3)
                if result and result.get('success'):
                    st.success(f"✅ Image search working! Found {result.get('total_found', 0)} images")
                else:
                    st.error(f"❌ Image search failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Image test error: {str(e)}")
        elif not IMAGE_PROCESSING_AVAILABLE:
            st.button("🖼️ Images (Unavailable)", disabled=True, use_container_width=True)

if __name__ == "__main__":
    main()