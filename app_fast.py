"""
AI Research Agent - Fast & Fixed Version
Optimized for speed and reliability with proper error handling
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import time
import logging
from typing import Dict, List
import numpy as np

# Set up logging
logging.basicConfig(level=logging.WARNING)  # Reduce log noise
logger = logging.getLogger(__name__)

# Fast imports with caching
@st.cache_resource
def load_core_modules():
    """Load core modules with caching for speed"""
    try:
        from modules.web_search import WebSearchEngine
        from modules.content_extractor import ContentExtractor  
        from modules.ai_summarizer import AISummarizer
        from utils.pdf_generator import PDFGenerator
        from config import Config
        return WebSearchEngine, ContentExtractor, AISummarizer, PDFGenerator, Config, True
    except ImportError as e:
        st.error(f"❌ Core modules missing: {e}")
        return None, None, None, None, None, False

@st.cache_resource
def load_enhanced_modules():
    """Load enhanced modules with caching"""
    modules = {}
    try:
        from modules.enhanced_search import EnhancedSearchEngine
        modules['enhanced_search'] = EnhancedSearchEngine
    except ImportError:
        modules['enhanced_search'] = None
    
    try:
        from modules.historical_data import HistoricalDataAnalyzer
        modules['historical_data'] = HistoricalDataAnalyzer
    except ImportError:
        modules['historical_data'] = None
    
    try:
        from modules.enhanced_images import EnhancedImageProcessor
        modules['enhanced_images'] = EnhancedImageProcessor
    except ImportError:
        modules['enhanced_images'] = None
    
    return modules

# Load modules once
WebSearchEngine, ContentExtractor, AISummarizer, PDFGenerator, Config, CORE_AVAILABLE = load_core_modules()
enhanced_modules = load_enhanced_modules()

if not CORE_AVAILABLE:
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

def safe_api_call(func, *args, **kwargs):
    """Fast API call with minimal error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return {"error": str(e), "success": False}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def cached_search(query: str, num_results: int, search_mode: str):
    """Cached search for faster repeated queries"""
    try:
        if search_mode == "Enhanced" and enhanced_modules['enhanced_search']:
            search_engine = enhanced_modules['enhanced_search']()
            return safe_api_call(search_engine.fast_search_and_analyze, query, num_results)
        else:
            search_engine = WebSearchEngine()
            return safe_api_call(search_engine.search, query, num_results)
    except Exception as e:
        return {"error": str(e), "success": False}

@st.cache_data(ttl=300)
def cached_content_extraction(urls: List[str]):
    """Cached content extraction for faster processing"""
    try:
        extractor = ContentExtractor()
        extracted_content = []
        
        # Limit to 3 URLs for speed
        for url in urls[:3]:
            try:
                content = safe_api_call(extractor.extract_from_url, url)  # Fixed method name
                if content and content.get('success') is not False:
                    extracted_content.append(content)
            except Exception as e:
                logger.warning(f"Content extraction failed for {url}: {e}")
                continue
        
        return extracted_content
    except Exception as e:
        return []

@st.cache_data(ttl=300)
def cached_ai_summary(text: str, query: str):
    """Cached AI summarization for faster results"""
    try:
        summarizer = AISummarizer()
        return safe_api_call(summarizer.summarize_content, text, query)
    except Exception as e:
        return {"error": str(e), "success": False}

def main():
    """Optimized main application function"""
    
    # Fast header
    st.markdown('<h1 style="text-align: center; color: #1f77b4;">🚀 AI Research Agent - Fast Mode</h1>', unsafe_allow_html=True)
    
    # Quick feature status
    feature_count = sum([
        CORE_AVAILABLE,
        bool(enhanced_modules['enhanced_search']),
        bool(enhanced_modules['historical_data']),
        bool(enhanced_modules['enhanced_images'])
    ])
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <div style="background: green; color: white; padding: 0.5rem; border-radius: 15px; margin: 0 auto; max-width: 500px;">
            ⚡ SPEED OPTIMIZED: {feature_count}/4 Features • Cached Results • Fast Processing
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simplified sidebar
    with st.sidebar:
        st.header("⚙️ Quick Settings")
        
        # API Status
        try:
            config = Config()
            validation = config.validate_api_keys()
            st.metric("Working APIs", validation.get('working_count', 0))
        except:
            st.warning("Config loading failed")
        
        # Essential settings only
        num_results = st.slider("Results", 5, 15, 8)
        search_mode = st.radio("Mode", ["Enhanced", "Standard"]) if enhanced_modules['enhanced_search'] else "Standard"
        include_summary = st.checkbox("AI Summary", value=True)
        include_extraction = st.checkbox("Content Extraction", value=True)
        
        # Performance info
        st.info("⚡ Optimizations Active:\n• Result caching\n• Fast extraction\n• Minimal logging")
    
    # Main search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🔍 Research Query")
        query = st.text_input(
            "Enter your research topic:",
            placeholder="e.g., AI trends 2024, climate change solutions",
            value=st.session_state.search_query
        )
        search_button = st.button("🚀 Fast Research", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("💡 Quick Examples")
        examples = ["AI trends 2024", "Climate change", "Tech news", "Space exploration"]
        for example in examples:
            if st.button(f"📌 {example}", use_container_width=True):
                st.session_state.search_query = example
                st.rerun()
    
    # Fast research execution
    if search_button and query:
        st.session_state.search_query = query
        
        # Streamlined progress tracking
        progress = st.progress(0)
        status = st.empty()
        start_time = time.time()
        
        try:
            # Step 1: Fast Search (cached)
            status.text("🔍 Searching...")
            progress.progress(25)
            
            search_results = cached_search(query, num_results, search_mode)
            
            progress.progress(50)
            
            # Step 2: Fast Content Extraction (optional, cached)
            extracted_content = []
            if include_extraction and search_results and not search_results.get('error'):
                status.text("📄 Extracting content...")
                
                # Get URLs from search results
                if isinstance(search_results, dict):
                    results_list = search_results.get('search_results', [])
                else:
                    results_list = search_results
                
                urls = [r.get('url') for r in results_list[:3] if r.get('url')]  # Limit to 3 for speed
                if urls:
                    extracted_content = cached_content_extraction(urls)
            
            progress.progress(75)
            
            # Step 3: Fast AI Summary (cached)
            summary = None
            if include_summary:
                status.text("🧠 Generating summary...")
                
                # Prepare text for summarization
                if extracted_content:
                    combined_text = " ".join([content.get('text', '')[:500] for content in extracted_content])[:2000]
                else:
                    # Use search results for summary
                    if isinstance(search_results, dict):
                        results_list = search_results.get('search_results', [])
                    else:
                        results_list = search_results
                    
                    combined_text = " ".join([r.get('snippet', '')[:200] for r in results_list])[:1500]
                
                if combined_text:
                    summary = cached_ai_summary(combined_text, query)
            
            progress.progress(100)
            
            total_time = time.time() - start_time
            status.text(f"✅ Completed in {total_time:.1f}s!")
            
            # Store results
            st.session_state.research_results = {
                'query': query,
                'search_results': search_results,
                'extracted_content': extracted_content,
                'summary': summary,
                'timestamp': datetime.now(),
                'mode': search_mode,
                'processing_time': total_time
            }
            
            time.sleep(1)
            progress.empty()
            status.empty()
            
        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
    
    # Fast results display
    if st.session_state.research_results:
        display_fast_results(st.session_state.research_results)

def display_fast_results(results):
    """Fast, streamlined results display"""
    
    st.divider()
    st.header(f"📊 Results: \"{results['query']}\"")
    
    # Quick metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sources", len(results.get('extracted_content', [])))
    with col2:
        search_count = len(results.get('search_results', [])) if isinstance(results.get('search_results'), list) else len(results.get('search_results', {}).get('search_results', []))
        st.metric("Results", search_count)
    with col3:
        st.metric("Mode", results.get('mode', 'Standard'))
    with col4:
        st.metric("Time", f"{results.get('processing_time', 0):.1f}s")
    
    # Streamlined tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🔍 Sources", "📊 Analysis", "📄 Export"])
    
    with tab1:
        display_fast_summary(results)
    
    with tab2:
        display_fast_sources(results)
    
    with tab3:
        display_fast_analysis(results)
    
    with tab4:
        display_fast_export(results)

def display_fast_summary(results):
    """Fast summary display"""
    summary = results.get('summary')
    
    if summary and summary.get('success'):
        st.subheader("📝 AI Summary")
        st.markdown(summary.get('summary', 'No summary available'))
        
        if summary.get('response_time'):
            st.caption(f"⚡ Generated in {summary['response_time']} seconds")
    else:
        st.info("Summary not generated or failed. Check sources below.")

def display_fast_sources(results):
    """Fast sources display"""
    search_results = results.get('search_results', [])
    extracted_content = results.get('extracted_content', [])
    
    # Handle different result formats
    if isinstance(search_results, dict):
        sources_list = search_results.get('search_results', [])
    else:
        sources_list = search_results
    
    st.subheader(f"🔍 Sources ({len(sources_list)} found)")
    
    # Quick source list
    for i, source in enumerate(sources_list[:10], 1):
        with st.expander(f"{i}. {source.get('title', 'Untitled')[:60]}..."):
            st.markdown(f"**URL:** {source.get('url', 'N/A')}")
            st.markdown(f"**Description:** {source.get('snippet', 'No description')[:250]}...")
            if source.get('source'):
                st.caption(f"Source: {source['source']}")
    
    # Extracted content (if available)
    if extracted_content:
        st.subheader(f"📄 Extracted Content ({len(extracted_content)} sources)")
        for i, content in enumerate(extracted_content, 1):
            with st.expander(f"Content {i}: {content.get('title', 'Untitled')[:50]}..."):
                if content.get('text'):
                    text = content['text'][:600]
                    st.markdown(text + "..." if len(content['text']) > 600 else text)

def display_fast_analysis(results):
    """Fast analysis display"""
    search_results = results.get('search_results', [])
    
    if isinstance(search_results, dict):
        sources = search_results.get('search_results', [])
    else:
        sources = search_results
    
    if sources:
        st.subheader("📊 Quick Analysis")
        
        # Domain analysis
        domains = [s.get('domain', 'Unknown') for s in sources if s.get('domain')]
        if domains:
            domain_counts = pd.Series(domains).value_counts().head(6)
            
            fig = px.bar(
                x=domain_counts.values,
                y=domain_counts.index,
                orientation='h',
                title='Top Source Domains'
            )
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        # Quick stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Unique Domains", len(set(domains)))
        with col2:
            avg_snippet_length = np.mean([len(s.get('snippet', '')) for s in sources])
            st.metric("Avg Description Length", f"{avg_snippet_length:.0f} chars")
    else:
        st.info("No analysis data available")

def display_fast_export(results):
    """Fast export options"""
    st.subheader("📥 Quick Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Fast JSON export
        if st.button("📊 Export JSON", use_container_width=True):
            export_data = {
                'query': results['query'],
                'timestamp': str(results['timestamp']),
                'mode': results.get('mode', 'Standard'),
                'processing_time': results.get('processing_time', 0),
                'sources_count': len(results.get('extracted_content', [])),
                'search_results_count': len(results.get('search_results', [])) if isinstance(results.get('search_results'), list) else len(results.get('search_results', {}).get('search_results', []))
            }
            
            json_string = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                "📥 Download JSON",
                json_string,
                file_name=f"research_{results['query'][:20]}_{datetime.now().strftime('%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.success("✅ JSON ready!")
    
    with col2:
        # Fast Markdown export
        if st.button("📝 Export Markdown", use_container_width=True):
            md_content = f"# Research: {results['query']}\\n\\n"
            md_content += f"**Generated:** {results['timestamp']}\\n"
            md_content += f"**Processing Time:** {results.get('processing_time', 0):.1f}s\\n\\n"
            
            # Add summary if available
            summary = results.get('summary')
            if summary and summary.get('success'):
                md_content += f"## Summary\\n{summary.get('summary', 'No summary')}\\n\\n"
            
            # Add top sources
            search_results = results.get('search_results', [])
            sources = search_results if isinstance(search_results, list) else search_results.get('search_results', [])
            
            if sources:
                md_content += "## Top Sources\\n\\n"
                for i, source in enumerate(sources[:5], 1):
                    md_content += f"{i}. **{source.get('title', 'Untitled')}**\\n"
                    md_content += f"   - {source.get('url', 'N/A')}\\n\\n"
            
            st.download_button(
                "📥 Download Markdown",
                md_content,
                file_name=f"research_{results['query'][:20]}_{datetime.now().strftime('%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
            st.success("✅ Markdown ready!")
    
    # Performance info
    st.info(f"⚡ Research completed in {results.get('processing_time', 0):.1f} seconds")

if __name__ == "__main__":
    main()