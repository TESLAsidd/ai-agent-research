"""
Simple test version of the AI Research Agent to identify issues
"""

import streamlit as st
import sys
import os

# Test basic imports
try:
    from config import Config
    st.success("✅ Config imported successfully")
except Exception as e:
    st.error(f"❌ Config import failed: {str(e)}")
    st.stop()

try:
    from modules.web_search import WebSearchEngine
    st.success("✅ Web search module imported successfully")
except Exception as e:
    st.error(f"❌ Web search import failed: {str(e)}")

try:
    from modules.ai_summarizer import AISummarizer
    st.success("✅ AI summarizer module imported successfully")
except Exception as e:
    st.error(f"❌ AI summarizer import failed: {str(e)}")

try:
    from modules.content_extractor import ContentExtractor
    st.success("✅ Content extractor module imported successfully")
except Exception as e:
    st.error(f"❌ Content extractor import failed: {str(e)}")

# Test enhanced imports
try:
    from modules.enhanced_search import EnhancedSearchEngine
    st.success("✅ Enhanced search module imported successfully")
except Exception as e:
    st.warning(f"⚠️ Enhanced search import failed: {str(e)}")

try:
    from modules.historical_data import HistoricalDataAnalyzer
    st.success("✅ Historical data module imported successfully")
except Exception as e:
    st.warning(f"⚠️ Historical data import failed: {str(e)}")

try:
    from modules.enhanced_images import EnhancedImageProcessor
    st.success("✅ Enhanced images module imported successfully")
except Exception as e:
    st.warning(f"⚠️ Enhanced images import failed: {str(e)}")

# Test configuration
st.header("🔧 Configuration Test")

config = Config()
validation = config.validate_api_keys()

st.write(f"**Working APIs:** {validation['working_count']}")
st.write(f"**AI Providers:** {validation['ai_providers']}")
st.write(f"**Search Engines:** {validation['search_engines']}")
st.write(f"**Historical Data:** {validation['historical_data']}")
st.write(f"**Image Services:** {validation['image_services']}")

# Simple functionality test
st.header("🧪 Basic Functionality Test")

if st.button("Test Basic Search"):
    try:
        search_engine = WebSearchEngine()
        st.success("✅ Web search engine initialized")
        
        # Test a simple search
        results = search_engine.search("Python programming", 3)
        st.success(f"✅ Search completed - found {len(results)} results")
        
    except Exception as e:
        st.error(f"❌ Search test failed: {str(e)}")

if st.button("Test Enhanced Features"):
    try:
        from modules.enhanced_search import EnhancedSearchEngine
        enhanced_search = EnhancedSearchEngine()
        st.success("✅ Enhanced search engine initialized")
        
        # Test enhanced search
        results = enhanced_search.fast_search_and_analyze("AI trends", 3)
        st.success("✅ Enhanced search completed")
        st.json(results)
        
    except Exception as e:
        st.error(f"❌ Enhanced search test failed: {str(e)}")

# Show environment info
st.header("📋 Environment Information")
st.write(f"**Python Version:** {sys.version}")
st.write(f"**Working Directory:** {os.getcwd()}")
st.write(f"**Python Path:** {sys.executable}")

# Show file structure
st.header("📁 File Structure Check")
required_files = [
    'config.py',
    'modules/web_search.py',
    'modules/ai_summarizer.py',
    'modules/content_extractor.py',
    'modules/enhanced_search.py',
    'modules/historical_data.py',
    'modules/enhanced_images.py',
    '.env'
]

for file_path in required_files:
    if os.path.exists(file_path):
        st.success(f"✅ {file_path}")
    else:
        st.error(f"❌ {file_path} missing")