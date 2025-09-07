"""
AI Research Agent - Main Streamlit Application
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
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import requests

# Import our custom modules
from modules.web_search import WebSearchEngine
from modules.content_extractor import ContentExtractor
from modules.ai_summarizer import AISummarizer
from utils.pdf_generator import PDFGenerator
from config import Config

# Enhanced modules for faster responses
try:
    from modules.enhanced_search import EnhancedSearchEngine
    from modules.enhanced_ai import EnhancedSummarizer, MultiAIProvider
    from modules.historical_data import HistoricalDataAnalyzer
    from modules.enhanced_images import EnhancedImageProcessor
    ENHANCED_FEATURES_AVAILABLE = True
    HISTORICAL_DATA_AVAILABLE = True
    IMAGE_PROCESSING_AVAILABLE = True
    
    # Set up logging for enhanced modules
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
except ImportError as e:
    print(f"Warning: Enhanced features not available - {e}")
    ENHANCED_FEATURES_AVAILABLE = False
    HISTORICAL_DATA_AVAILABLE = False
    IMAGE_PROCESSING_AVAILABLE = False
    EnhancedSearchEngine = None
    EnhancedSummarizer = None
    MultiAIProvider = None
    HistoricalDataAnalyzer = None
    EnhancedImageProcessor = None
    logger = logging.getLogger(__name__)

# Optional imports
try:
    from modules.cache_manager import cache_manager
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False
    cache_manager = None

# Optional image analyzer import
try:
    from modules.image_analyzer import ImageAnalyzer
    IMAGE_ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Image analysis not available - {e}")
    IMAGE_ANALYSIS_AVAILABLE = False
    ImageAnalyzer = None

# Page configuration
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
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
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .trend-analysis {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
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

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Research Agent</h1>', unsafe_allow_html=True)
    
    # Enhanced features indicator
    header_message = """
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Your intelligent research assistant with enhanced multi-API capabilities
        </p>
    """
    
    if ENHANCED_FEATURES_AVAILABLE:
        header_message += """
        <div style="background: linear-gradient(90deg, #4CAF50, #2196F3); color: white; padding: 0.5rem; border-radius: 20px; margin: 1rem auto; max-width: 800px;">
            ⚡ COMPREHENSIVE MODE ACTIVE: AI Analysis • Real-time Search • Historical Trends • Image Processing • Data Visualization
        </div>
        """
    else:
        header_message += """
        <div style="background: #ff9800; color: white; padding: 0.5rem; border-radius: 20px; margin: 1rem auto; max-width: 500px;">
            🐌 Standard Mode: Add API keys in .env for enhanced features
        </div>
        """
    
    header_message += "</div>"
    st.markdown(header_message, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Configuration Status
        config = Config()
        validation = config.validate_api_keys()
        st.subheader("📊 API Status Dashboard")
        
        # Overall health indicator
        overall_health = validation.get('working_count', 0)
        if overall_health > 8:
            health_color = "green"
            health_status = "Excellent"
        elif overall_health > 5:
            health_color = "blue"
            health_status = "Good"
        elif overall_health > 2:
            health_color = "orange"
            health_status = "Limited"
        else:
            health_color = "red"
            health_status = "Critical"
        
        st.markdown(f"""
        <div style="background-color: {health_color}; color: white; padding: 0.5rem; border-radius: 0.5rem; text-align: center; margin-bottom: 1rem;">
            System Health: {health_status} ({overall_health} APIs Active)
        </div>
        """, unsafe_allow_html=True)
        
        # Working APIs by category
        if validation.get('ai_providers'):
            st.write("🧠 **AI Providers:**")
            for provider in validation['ai_providers']:
                st.write(f"  ✅ {provider}")
        
        if validation.get('search_engines'):
            st.write("🔍 **Search Engines:**")
            for engine in validation['search_engines']:
                st.write(f"  ✅ {engine}")
        
        if validation.get('historical_data'):
            st.write("📊 **Historical Data:**")
            for source in validation['historical_data']:
                st.write(f"  ✅ {source}")
        
        if validation.get('image_services'):
            st.write("🖼️ **Image Services:**")
            for service in validation['image_services']:
                st.write(f"  ✅ {service}")
        
        if validation.get('social_media'):
            st.write("📱 **Social Media:**")
            for platform in validation['social_media']:
                st.write(f"  ✅ {platform}")
        
        # Show issues if any
        if validation.get('issues'):
            st.markdown("**⚠️ Issues:**")
            for issue in validation['issues']:
                st.write(f"  ❌ {issue}")
        
        # Feature capabilities
        st.divider()
        
        # Research mode selection
        st.subheader("🎯 Research Mode")
        
        research_mode = st.selectbox(
            "Select Research Focus:",
            [
                "Comprehensive Analysis",
                "Historical Trends", 
                "Market Analysis",
                "Technology Trends",
                "Image & Visual Analysis",
                "Social Sentiment",
                "Quick Research"
            ],
            index=0
        )
        
        # Time period for historical analysis
        if research_mode in ["Historical Trends", "Market Analysis"]:
            time_period = st.selectbox(
                "Time Period:",
                ["1 Year", "6 Months", "3 Months", "1 Month"],
                index=0
            )
        else:
            time_period = "1 Year"
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            include_images = st.checkbox("Include Image Analysis", value=True)
            include_trends = st.checkbox("Include Trend Analysis", value=True)
            include_charts = st.checkbox("Generate Charts & Graphs", value=True)
            max_sources = st.slider("Maximum Sources", 5, 25, 10)
        # Export options
        st.subheader("📋 Export Options")
        export_format = st.selectbox(
            "Export Format:",
            ["PDF Report", "Markdown", "JSON Data", "CSV Data"]
        )
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("📈 Test Market Data", use_container_width=True):
            if HISTORICAL_DATA_AVAILABLE:
                test_market_analysis()
            else:
                st.error("Historical data features not available")
        
        if st.button("🖼️ Test Image Search", use_container_width=True):
            if IMAGE_PROCESSING_AVAILABLE:
                test_image_search()
            else:
                st.error("Image processing features not available")
        
        st.divider()
        
        # Cache Management
        if CACHE_AVAILABLE:
            st.subheader("💾 Cache Management")
            
            cache_stats = cache_manager.get_cache_stats()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Cache Files", cache_stats['total_files'])
            with col2:
                st.metric("Cache Size (MB)", cache_stats['total_size_mb'])
            
            # Cache details
            with st.expander("Cache Details"):
                for cache_type, stats in cache_stats['by_type'].items():
                    st.write(f"**{cache_type.title()}**: {stats['files']} files, {stats['size_mb']} MB")
            
            # Cache controls
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Clear Cache", use_container_width=True):
                    cache_manager.clear_cache()
                    st.success("Cache cleared successfully!")
                    st.rerun()
            
            with col2:
                cache_type_to_clear = st.selectbox("Clear specific cache", ["All", "search", "content", "summaries", "images"])
                if st.button("🗑️ Clear Selected", use_container_width=True):
                    if cache_type_to_clear == "All":
                        cache_manager.clear_cache()
                    else:
                        cache_manager.clear_cache(cache_type_to_clear)
                    st.success(f"{cache_type_to_clear} cache cleared!")
                    st.rerun()
        else:
            st.info("💾 Caching unavailable (performance may be slower)")
        
        # Search Settings
        st.subheader("🔍 Search Settings")
        
        # Search mode selection
        if ENHANCED_FEATURES_AVAILABLE:
            search_mode = st.radio(
                "Search Mode",
                ["Enhanced (Faster + Real-time)", "Standard (Traditional APIs)"],
                help="Enhanced mode uses multiple fast APIs for better results"
            )
        else:
            search_mode = "Standard (Traditional APIs)"
            st.info("🐌 Enhanced mode requires additional API keys")
        
        num_results = st.slider("Number of results", 5, 20, 10)
        time_filter = st.selectbox("Time filter", ["All time", "Past day", "Past week", "Past month", "Past year"])
        
        # Summary Settings
        st.subheader("📝 Summary Settings")
        summary_type = st.selectbox("Summary type", ["comprehensive", "brief", "detailed"])
        
        # AI Provider selection
        if ENHANCED_FEATURES_AVAILABLE:
            ai_mode = st.radio(
                "AI Processing Mode",
                ["Fastest Available", "Best Quality (Parallel)", "Perplexity Real-time", "Standard OpenAI"],
                help="Choose AI processing strategy for optimal speed and quality"
            )
        else:
            ai_mode = "Standard OpenAI"
            st.info("⚡ Enhanced AI modes require additional API keys")
        
        # Advanced Options
        with st.expander("🔧 Advanced Options"):
            enable_trend_analysis = st.checkbox("Enable trend analysis", value=True)
            enable_visualizations = st.checkbox("Enable data visualizations", value=True)
            enable_images = st.checkbox("Include images in results", value=True)
            enable_wordcloud = st.checkbox("Generate word clouds", value=True)
            
            # Performance optimizations
            st.markdown("**Performance Settings:**")
            parallel_processing = st.checkbox("Parallel processing", value=True, help="Process multiple sources simultaneously")
            aggressive_caching = st.checkbox("Aggressive caching", value=True, help="Cache more aggressively for faster responses")
            
            export_format = st.selectbox("Export format", ["PDF", "Markdown", "JSON"])
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search input
        st.subheader("🔍 Research Query")
        query = st.text_input(
            "Enter your research topic or question:",
            placeholder="e.g., Recent advancements in quantum computing, Benefits of intermittent fasting, How do transformer models work?",
            value=st.session_state.search_query
        )
        
        # Search button
        col_search1, col_search2, col_search3 = st.columns([1, 1, 1])
        with col_search2:
            search_button = st.button("🚀 Start Research", type="primary", use_container_width=True)
    
    with col2:
        # Quick examples
        st.subheader("💡 Example Queries")
        examples = [
            "AI breakthroughs in 2024",
            "Climate change solutions",
            "Cryptocurrency regulations",
            "Space exploration news",
            "Medical research updates"
        ]
        
        for example in examples:
            if st.button(f"📌 {example}", use_container_width=True):
                st.session_state.search_query = example
                st.rerun()
    
    # Display research results with enhanced features
    if search_button and query:
        st.session_state.search_query = query
        
        # Initialize progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Search and content extraction
            progress_bar.progress(20)
            status_text.text("🔍 Searching for information...")
            
            if ENHANCED_FEATURES_AVAILABLE and search_mode == "Enhanced (Faster + Real-time)":
                # Use enhanced search
                enhanced_search = EnhancedSearchEngine()
                search_results = enhanced_search.fast_search_and_analyze(query, num_results)
                
                progress_bar.progress(40)
                status_text.text("⚡ Enhanced search completed!")
                
            else:
                # Use standard search
                search_engine = WebSearchEngine()
                search_results = search_engine.search(query, num_results)
                
                progress_bar.progress(40) 
                status_text.text("📊 Standard search completed")
            
            # Step 2: Historical data analysis if requested
            historical_data = None
            if research_mode in ["Historical Trends", "Market Analysis"] and HISTORICAL_DATA_AVAILABLE:
                progress_bar.progress(50)
                status_text.text("📈 Analyzing historical trends...")
                
                analyzer = HistoricalDataAnalyzer()
                
                if "stock" in query.lower() or "market" in query.lower():
                    # Try to extract stock symbol from query
                    import re
                    symbol_match = re.search(r'\b([A-Z]{1,5})\b', query.upper())
                    symbol = symbol_match.group(1) if symbol_match else 'AAPL'  # Default to Apple
                    historical_data = analyzer.get_stock_trends(symbol, time_period.lower().replace(' ', ''))
                else:
                    # General market trends
                    historical_data = analyzer.get_market_trends('S&P500', time_period.lower().replace(' ', ''))
            
            # Step 3: Image search and analysis
            image_results = None
            if include_images and IMAGE_PROCESSING_AVAILABLE:
                progress_bar.progress(60)
                status_text.text("🖼️ Searching for relevant images...")
                
                image_processor = EnhancedImageProcessor()
                
                if research_mode == "Image & Visual Analysis":
                    image_results = image_processor.search_trend_images(query, time_period.lower())
                else:
                    image_results = image_processor.search_high_quality_images(query, 5)
            
            # Step 4: AI Analysis and Summarization
            progress_bar.progress(70)
            status_text.text("🧠 Generating AI analysis...")
            
            if ENHANCED_FEATURES_AVAILABLE:
                enhanced_ai = EnhancedSummarizer()
                
                if ai_mode == "Fastest Available":
                    summary_result = enhanced_ai.fast_summarize(
                        str(search_results)[:4000], 
                        query, 
                        summary_type
                    )
                elif ai_mode == "Best Quality (Parallel)":
                    summary_result = enhanced_ai.parallel_analysis(
                        str(search_results)[:3000], 
                        query
                    )
                else:
                    # Fallback to standard
                    summarizer = AISummarizer()
                    summary_result = summarizer.summarize_content(
                        str(search_results)[:3000], 
                        query
                    )
            else:
                # Standard AI summarization
                summarizer = AISummarizer()
                summary_result = summarizer.summarize_content(
                    str(search_results)[:3000], 
                    query
                )
            
            progress_bar.progress(90)
            status_text.text("📝 Finalizing research report...")
            
            # Store results in session state
            st.session_state.research_results = {
                'query': query,
                'search_results': search_results,
                'summary': summary_result,
                'historical_data': historical_data,
                'image_results': image_results,
                'research_mode': research_mode,
                'timestamp': datetime.now()
            }
            
            # Add to research history
            st.session_state.research_history.append({
                'query': query,
                'timestamp': datetime.now(),
                'mode': research_mode
            })
            
            progress_bar.progress(100)
            status_text.text("✅ Research completed successfully!")
            
            time.sleep(1)  # Brief pause to show completion
            
        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            progress_bar.empty()
            status_text.empty()
            return
        
        # Initialize enhanced progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_elapsed = st.empty()
        
        # Performance metrics
        start_time = time.time()
        metrics_placeholder = st.empty()
        
        try:
            # Step 1: Enhanced Web Search with real-time updates
            status_text.markdown("🔍 **Performing enhanced search across multiple engines...**")
            progress_bar.progress(10)
            time_elapsed.markdown(f"*Time elapsed: 0s*")
            
            search_start = time.time()
            
            # Choose search engine based on mode
            if search_mode == "Enhanced (Faster + Real-time)" and ENHANCED_FEATURES_AVAILABLE:
                # Use enhanced search engine for faster, more accurate results
                status_text.markdown("⚡ **Using enhanced search with Perplexity, Tavily, Exa, and You.com...**")
                enhanced_search = EnhancedSearchEngine()
                
                # Get real-time search results with AI analysis
                enhanced_results = enhanced_search.fast_search_and_analyze(
                    query, 
                    num_results=num_results
                )
                
                # Convert enhanced results to standard format
                search_results = enhanced_results.get('search_results', [])
                
                # Add Perplexity AI summary if available
                perplexity_summary = enhanced_results.get('perplexity_summary')
                if perplexity_summary and perplexity_summary.get('success'):
                    st.session_state.perplexity_summary = perplexity_summary
                
                # Show enhanced metrics
                if enhanced_results.get('search_time'):
                    status_text.markdown(f"✅ **Enhanced search completed in {enhanced_results['search_time']}s using {len(enhanced_results.get('engines_used', []))} engines**")
                
            else:
                # Use standard search engine
                status_text.markdown("🔍 **Using standard search engines...**")
                search_engine = WebSearchEngine()
                search_results = search_engine.search(
                    query, 
                    num_results=num_results,
                    time_filter=time_filter.lower().replace("past ", "").replace(" ", "") if time_filter != "All time" else None,
                    include_images=enable_images
                )
            search_time = time.time() - search_start
            
            progress_bar.progress(25)
            elapsed = time.time() - start_time
            time_elapsed.markdown(f"*Time elapsed: {elapsed:.1f}s*")
            
            with metrics_placeholder.container():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🔍 Search Time", f"{search_time:.1f}s")
                with col2:
                    st.metric("📄 Results Found", len(search_results))
                with col3:
                    image_count = len([r for r in search_results if r.get('result_type') == 'image'])
                    st.metric("🖼️ Images Found", image_count)
            
            if not search_results:
                st.error("❌ No search results found. Please try a different query or check your API configuration.")
                return
            
            # Step 2: Content Extraction with real-time updates
            status_text.markdown("📄 **Extracting content from sources...**")
            progress_bar.progress(35)
            elapsed = time.time() - start_time
            time_elapsed.markdown(f"*Time elapsed: {elapsed:.1f}s*")
            
            extraction_start = time.time()
            extractor = ContentExtractor()
            
            # Filter out image results for content extraction
            text_results = [r for r in search_results if r.get('result_type') != 'image']
            urls = [result['url'] for result in text_results]
            
            # Show extraction progress
            extraction_progress = st.empty()
            extracted_content = []
            
            if parallel_processing and len(urls) > 1:
                # Parallel processing for faster extraction
                extraction_progress.markdown(f"*Extracting from {len(urls)} sources in parallel...*")
                
                import concurrent.futures
                import threading
                
                def extract_single_url(url):
                    try:
                        return extractor.extract_from_url(url)
                    except Exception as e:
                        logger.error(f"Failed to extract from {url}: {str(e)}")
                        return None
                
                # Use ThreadPoolExecutor for parallel processing
                with concurrent.futures.ThreadPoolExecutor(max_workers=min(5, len(urls))) as executor:
                    future_to_url = {executor.submit(extract_single_url, url): url for url in urls}
                    
                    for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
                        try:
                            content = future.result()
                            if content:
                                extracted_content.append(content)
                        except Exception as e:
                            logger.error(f"Parallel extraction error: {str(e)}")
                        
                        # Update progress
                        current_progress = 35 + (i + 1) / len(urls) * 20
                        progress_bar.progress(int(current_progress))
            else:
                # Sequential processing (original method)
                for i, url in enumerate(urls):
                    extraction_progress.markdown(f"*Extracting from source {i+1}/{len(urls)}: {url[:50]}...*")
                    content = extractor.extract_from_url(url)
                    if content:
                        extracted_content.append(content)
                    
                    # Update progress
                    current_progress = 35 + (i + 1) / len(urls) * 20
                    progress_bar.progress(int(current_progress))
            
            extraction_time = time.time() - extraction_start
            extraction_progress.empty()
            
            progress_bar.progress(55)
            elapsed = time.time() - start_time
            time_elapsed.markdown(f"*Time elapsed: {elapsed:.1f}s*")
            
            # Update metrics
            with metrics_placeholder.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🔍 Search Time", f"{search_time:.1f}s")
                with col2:
                    st.metric("📄 Extraction Time", f"{extraction_time:.1f}s")
                with col3:
                    st.metric("📜 Content Sources", len(extracted_content))
                with col4:
                    total_words = sum(c.get('word_count', 0) for c in extracted_content)
                    st.metric("📊 Total Words", f"{total_words:,}")
            
            if not extracted_content:
                st.error("❌ Failed to extract content from sources. Please try again.")
                return
            
            # Step 3: Enhanced AI Summarization with streaming updates
            status_text.markdown("🤖 **Generating AI-powered analysis and summaries...**")
            progress_bar.progress(65)
            elapsed = time.time() - start_time
            time_elapsed.markdown(f"*Time elapsed: {elapsed:.1f}s*")
            
            summarization_start = time.time()
            
            # Show summarization steps
            summary_progress = st.empty()
            
            # Choose AI processing mode
            if ai_mode != "Standard OpenAI" and ENHANCED_FEATURES_AVAILABLE:
                summary_progress.markdown(f"*Using {ai_mode} AI processing...*")
                enhanced_ai = EnhancedSummarizer()
                
                # Prepare content text for AI analysis
                combined_content = "\n\n".join([
                    f"Title: {content.get('title', '')}\n"
                    f"URL: {content.get('url', '')}\n"
                    f"Content: {content.get('text', '')[:1000]}\n"
                    for content in extracted_content
                ])
                
                if ai_mode == "Fastest Available":
                    # Get fastest AI response
                    fast_summary = enhanced_ai.fast_summarize(combined_content, query, summary_type)
                    if fast_summary.get('success'):
                        summaries = {
                            "executive_summary": fast_summary['summary'],
                            "ai_provider": fast_summary.get('provider', 'Unknown'),
                            "response_time": fast_summary.get('response_time', 0),
                            "enhanced_mode": True
                        }
                    else:
                        # Fallback to standard
                        summarizer = AISummarizer()
                        summaries = summarizer.summarize_research(extracted_content, query, summary_type)
                        
                elif ai_mode == "Best Quality (Parallel)":
                    # Get parallel responses from multiple AI providers
                    parallel_results = enhanced_ai.parallel_analysis(combined_content, query)
                    
                    # Combine the best results
                    best_summary = ""
                    providers_used = []
                    
                    for provider, result in parallel_results.items():
                        if result.get('success'):
                            providers_used.append(provider)
                            if len(result.get('content', '')) > len(best_summary):
                                best_summary = result['content']
                    
                    summaries = {
                        "executive_summary": best_summary,
                        "ai_providers": providers_used,
                        "parallel_results": parallel_results,
                        "enhanced_mode": True
                    }
                    
                elif ai_mode == "Perplexity Real-time":
                    # Use Perplexity for real-time AI analysis
                    if hasattr(st.session_state, 'perplexity_summary') and st.session_state.perplexity_summary:
                        perplexity_data = st.session_state.perplexity_summary
                        summaries = {
                            "executive_summary": perplexity_data.get('summary', ''),
                            "citations": perplexity_data.get('citations', []),
                            "ai_provider": "Perplexity AI",
                            "real_time": True,
                            "enhanced_mode": True
                        }
                    else:
                        # Fallback to enhanced summarizer
                        fast_summary = enhanced_ai.fast_summarize(combined_content, query, "brief")
                        summaries = fast_summary if fast_summary.get('success') else {"error": "AI analysis failed"}
                        
            else:
                # Use standard OpenAI summarization
                summary_progress.markdown("*Preparing content for AI analysis...*")
                summarizer = AISummarizer()
                summaries = summarizer.summarize_research(extracted_content, query, summary_type)
            
            if "error" in summaries:
                st.error(f"❌ Summarization failed: {summaries['error']}")
                return
            
            summarization_time = time.time() - summarization_start
            summary_progress.empty()
            
            progress_bar.progress(85)
            elapsed = time.time() - start_time
            time_elapsed.markdown(f"*Time elapsed: {elapsed:.1f}s*")
            
            # Step 4: Finalization and Results
            status_text.markdown("✅ **Research completed successfully!**")
            progress_bar.progress(100)
            total_time = time.time() - start_time
            time_elapsed.markdown(f"*Total time: {total_time:.1f}s*")
            
            # Final metrics
            with metrics_placeholder.container():
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("🔍 Search", f"{search_time:.1f}s")
                with col2:
                    st.metric("📄 Extraction", f"{extraction_time:.1f}s")
                with col3:
                    st.metric("🤖 AI Analysis", f"{summarization_time:.1f}s")
                with col4:
                    st.metric("⏱️ Total Time", f"{total_time:.1f}s")
                with col5:
                    efficiency = len(extracted_content) / total_time if total_time > 0 else 0
                    st.metric("⚡ Efficiency", f"{efficiency:.1f} sources/sec")
            
            # Store results in session state
            st.session_state.research_results = {
                'query': query,
                'search_results': search_results,
                'extracted_content': extracted_content,
                'summaries': summaries,
                'timestamp': datetime.now().isoformat(),
                'enable_wordcloud': enable_wordcloud,
                'enable_images': enable_images
            }
            
            # Add to research history
            st.session_state.research_history.append({
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'sources_count': len(extracted_content)
            })
            
            time.sleep(2)  # Show results briefly
            status_text.empty()
            progress_bar.empty()
            time_elapsed.empty()
            
            # Keep metrics visible for longer
            time.sleep(1)
            metrics_placeholder.empty()
            
        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            status_text.empty()
            progress_bar.empty()
            return
    
    # Display results
    if st.session_state.research_results:
        display_research_results(st.session_state.research_results, enable_trend_analysis, enable_visualizations)
    
    # Research history
    if st.session_state.research_history:
        display_research_history()

def display_research_results(results: Dict, enable_trend_analysis: bool, enable_visualizations: bool):
    """Display comprehensive research results"""
    
    query = results['query']
    summaries = results['summaries']
    extracted_content = results['extracted_content']
    search_results = results['search_results']
    enable_wordcloud = results.get('enable_wordcloud', False)
    enable_images = results.get('enable_images', False)
    
    st.markdown(f'<div class="sub-header">📊 Research Results: "{query}"</div>', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sources Analyzed", len(extracted_content))
    
    with col2:
        unique_domains = len(set(content.get('domain', '') for content in extracted_content))
        st.metric("Unique Domains", unique_domains)
    
    with col3:
        total_words = sum(content.get('word_count', 0) for content in extracted_content)
        st.metric("Total Words", f"{total_words:,}")
    
    with col4:
        avg_words = total_words // len(extracted_content) if extracted_content else 0
        st.metric("Avg Words/Source", f"{avg_words:,}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Summary", "🔍 Sources", "🖼️ Images", "📈 Trends", "📊 Analysis", "📄 Export"])
    
    with tab1:
        display_summary_tab(summaries)
    
    with tab2:
        display_sources_tab(extracted_content)
    
    with tab3:
        if enable_images:
            display_images_tab(search_results)
        else:
            st.info("Image search is disabled in the sidebar settings.")
    
    with tab4:
        if enable_trend_analysis:
            display_trends_tab(summaries, enable_visualizations, enable_wordcloud)
        else:
            st.info("Trend analysis is disabled in the sidebar settings.")
    
    with tab5:
        display_analysis_tab(summaries, enable_visualizations)
    
    with tab6:
        display_export_tab(results)

def display_summary_tab(summaries: Dict):
    """Display summary tab content with enhanced AI features"""
    
    # Enhanced AI Information
    if summaries.get('enhanced_mode'):
        st.success("⚡ Enhanced AI Analysis Active")
        
        # Show AI provider information
        col1, col2, col3 = st.columns(3)
        with col1:
            if summaries.get('ai_provider'):
                st.info(f"🤖 AI Provider: {summaries['ai_provider']}")
            elif summaries.get('ai_providers'):
                st.info(f"🤖 AI Providers: {', '.join(summaries['ai_providers'])}")
        
        with col2:
            if summaries.get('response_time'):
                st.metric("⚡ Response Time", f"{summaries['response_time']}s")
        
        with col3:
            if summaries.get('real_time'):
                st.success("🔴 Real-time Data")
    
    # Perplexity Real-time Summary
    if summaries.get('real_time') and summaries.get('citations'):
        st.subheader("🔍 Perplexity Real-time Analysis")
        st.markdown(summaries["executive_summary"])
        
        # Show citations from Perplexity
        if summaries.get('citations'):
            with st.expander("📚 Real-time Citations"):
                for i, citation in enumerate(summaries['citations'], 1):
                    st.markdown(f"**{i}.** {citation}")
    
    # Executive Summary
    elif "executive_summary" in summaries:
        st.subheader("📝 Executive Summary")
        st.markdown(summaries["executive_summary"])
    
    # Parallel AI Results (if available)
    if summaries.get('parallel_results'):
        with st.expander("🕰️ View Parallel AI Responses"):
            for provider, result in summaries['parallel_results'].items():
                if result.get('success'):
                    st.markdown(f"**{provider}:**")
                    st.markdown(result['content'][:300] + "..." if len(result['content']) > 300 else result['content'])
                    st.markdown("---")
    
    # Key Findings
    if "key_findings" in summaries:
        st.subheader("🎯 Key Findings")
        for i, finding in enumerate(summaries["key_findings"], 1):
            st.markdown(f"**{i}.** {finding}")
    
    # Detailed Analysis
    if "detailed_analysis" in summaries:
        st.subheader("🔬 Detailed Analysis")
        st.markdown(summaries["detailed_analysis"])

def display_sources_tab(extracted_content: List[Dict]):
    """Display sources tab content"""
    
    st.subheader("📚 Sources")
    
    for i, content in enumerate(extracted_content, 1):
        with st.expander(f"{i}. {content.get('title', 'Untitled')}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**URL:** {content.get('url', 'N/A')}")
                st.markdown(f"**Domain:** {content.get('domain', 'N/A')}")
                st.markdown(f"**Word Count:** {content.get('word_count', 0):,}")
                st.markdown(f"**Extraction Method:** {content.get('extraction_method', 'N/A')}")
                
                if content.get('authors'):
                    st.markdown(f"**Authors:** {', '.join(content['authors'])}")
                
                if content.get('publish_date'):
                    st.markdown(f"**Published:** {content['publish_date']}")
            
            with col2:
                st.markdown(f"**Content Score:** {content.get('content_score', 0)}")
                st.markdown(f"**Extracted:** {content.get('extraction_timestamp', 'N/A')}")
            
            # Content preview
            text = content.get('text', '')
            if text:
                st.markdown("**Content Preview:**")
                st.markdown(text[:500] + "..." if len(text) > 500 else text)

def display_images_tab(search_results: List[Dict]):
    """Display images tab with search results and analysis"""
    
    image_results = [r for r in search_results if r.get('result_type') == 'image']
    
    if not image_results:
        st.info("No images found for this search query.")
        return
    
    st.subheader(f"🖼️ Images Analysis ({len(image_results)} found)")
    
    # Image analysis options
    col1, col2, col3 = st.columns(3)
    with col1:
        if IMAGE_ANALYSIS_AVAILABLE:
            analyze_images = st.checkbox("🤖 Enable AI Image Analysis", value=True)
        else:
            analyze_images = False
            st.info("📋 AI Image Analysis unavailable (missing dependencies)")
    with col2:
        if IMAGE_ANALYSIS_AVAILABLE:
            extract_text = st.checkbox("🔍 Extract Text (OCR)", value=True)
        else:
            extract_text = False
            st.info("📋 OCR unavailable (missing dependencies)")
    with col3:
        quality_filter = st.selectbox("Quality Filter", ["All", "High Quality Only", "With Text Only"])
    
    if (analyze_images or extract_text) and IMAGE_ANALYSIS_AVAILABLE:
        # Initialize image analyzer
        analyzer = ImageAnalyzer()
        
        # Show analysis progress
        analysis_progress = st.progress(0)
        analysis_status = st.empty()
        
        # Process images for analysis
        for i, image in enumerate(image_results[:10]):  # Limit to first 10 images
            analysis_progress.progress((i + 1) / min(10, len(image_results)))
            analysis_status.text(f"Analyzing image {i+1}/{min(10, len(image_results))}...")
            
            try:
                analysis_result = analyzer.analyze_image(
                    image.get('image_url', ''), 
                    st.session_state.get('search_query', '')
                )
                image['analysis'] = analysis_result
            except Exception as e:
                image['analysis'] = {'error': str(e), 'success': False}
        
        analysis_progress.empty()
        analysis_status.empty()
    
    # Filter images based on quality filter
    filtered_images = image_results
    if quality_filter == "High Quality Only":
        filtered_images = [
            img for img in image_results 
            if img.get('analysis', {}).get('quality', {}).get('overall_score', 0) > 60
        ]
    elif quality_filter == "With Text Only":
        filtered_images = [
            img for img in image_results 
            if img.get('analysis', {}).get('ocr', {}).get('has_text', False)
        ]
    
    if not filtered_images:
        st.warning(f"No images match the '{quality_filter}' filter.")
        return
    
    # Display images in an enhanced grid
    cols = st.columns(2)
    
    for i, image in enumerate(filtered_images):
        col_idx = i % 2
        
        with cols[col_idx]:
            try:
                # Display thumbnail or full image
                image_url = image.get('thumbnail') or image.get('image_url')
                
                if image_url:
                    # Create a container for each image
                    with st.container():
                        st.image(image_url, caption=image.get('title', 'Untitled')[:50], use_column_width=True)
                        
                        # Enhanced image details in an expander
                        with st.expander(f"📊 Analysis Results {i+1}", expanded=False):
                            # Basic info
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown(f"**Title:** {image.get('title', 'N/A')}")
                                st.markdown(f"**Source:** {image.get('source', 'N/A')}")
                                st.markdown(f"**Domain:** {image.get('domain', 'N/A')}")
                            
                            with col_b:
                                st.markdown(f"**Dimensions:** {image.get('width', 'N/A')} x {image.get('height', 'N/A')}")
                                if image.get('context_url'):
                                    st.markdown(f"**[View Source]({image['context_url']})**")
                                if image.get('image_url'):
                                    st.markdown(f"**[Full Size]({image['image_url']})**")
                            
                            # Analysis results
                            analysis = image.get('analysis', {})
                            if analysis and analysis.get('success'):
                                st.markdown("### 🤖 AI Analysis")
                                
                                # Quality metrics
                                quality = analysis.get('quality', {})
                                if quality:
                                    col_q1, col_q2, col_q3 = st.columns(3)
                                    with col_q1:
                                        st.metric("Quality Score", f"{quality.get('overall_score', 0)}/100")
                                    with col_q2:
                                        st.metric("Blur Score", f"{quality.get('blur_score', 0):.1f}")
                                    with col_q3:
                                        st.metric("Brightness", f"{quality.get('brightness', 0):.1f}")
                                
                                # OCR results
                                ocr = analysis.get('ocr', {})
                                if ocr and ocr.get('has_text'):
                                    st.markdown("### 🔍 Extracted Text (OCR)")
                                    st.text_area(
                                        "Detected Text", 
                                        ocr.get('text', ''), 
                                        height=100, 
                                        key=f"ocr_{i}"
                                    )
                                    st.markdown(f"**Confidence:** {ocr.get('confidence', 0):.1f}%")
                                    st.markdown(f"**Word Count:** {ocr.get('word_count', 0)}")
                                
                                # AI description
                                ai_desc = analysis.get('ai_description', {})
                                if ai_desc and ai_desc.get('success'):
                                    st.markdown("### 📝 AI Description")
                                    st.markdown(ai_desc.get('description', ''))
                                    if 'relevance_score' in ai_desc:
                                        st.markdown(f"**Relevance Score:** {ai_desc['relevance_score']:.2f}")
                                
                                # Visual features
                                visual = analysis.get('visual_features', {})
                                if visual:
                                    st.markdown("### 🎨 Visual Features")
                                    
                                    if visual.get('contains_chart'):
                                        st.success("📈 Chart/Graph detected")
                                    
                                    colors = visual.get('colors', {})
                                    if colors.get('dominant_colors'):
                                        st.markdown("**Dominant Colors:**")
                                        for color in colors['dominant_colors'][:3]:
                                            st.markdown(
                                                f"<div style='display: inline-block; width: 20px; height: 20px; "
                                                f"background-color: {color['hex']}; margin-right: 10px;'></div>"
                                                f"{color['hex']} ({color['percentage']:.1f}%)", 
                                                unsafe_allow_html=True
                                            )
                            
                            elif analysis.get('error'):
                                st.error(f"Analysis failed: {analysis['error']}")
                            
                            # Download buttons
                            col_d1, col_d2 = st.columns(2)
                            with col_d1:
                                if st.button(f"📋 Download Image {i+1}", key=f"download_img_{i}"):
                                    try:
                                        response = requests.get(image_url, timeout=10)
                                        if response.status_code == 200:
                                            st.download_button(
                                                label="Download Image",
                                                data=response.content,
                                                file_name=f"image_{i+1}.jpg",
                                                mime="image/jpeg",
                                                key=f"download_btn_{i}"
                                            )
                                    except Exception as e:
                                        st.error(f"Failed to download: {str(e)}")
                            
                            with col_d2:
                                if analysis and analysis.get('success'):
                                    analysis_json = json.dumps(analysis, indent=2, default=str)
                                    st.download_button(
                                        label=f"📄 Download Analysis {i+1}",
                                        data=analysis_json,
                                        file_name=f"image_analysis_{i+1}.json",
                                        mime="application/json",
                                        key=f"download_analysis_{i}"
                                    )
                
            except Exception as e:
                st.error(f"Failed to load image {i+1}: {str(e)}")

def display_trends_tab(summaries: Dict, enable_visualizations: bool, enable_wordcloud: bool = False):
    """Display trends tab content - unique feature"""
    
    st.markdown('<div class="trend-analysis">', unsafe_allow_html=True)
    st.subheader("📈 Trend Analysis")
    st.markdown("*This is a unique feature that identifies patterns and trends in your research topic.*")
    
    trend_data = summaries.get("trend_analysis", {})
    
    if "error" in trend_data:
        st.error(f"Trend analysis unavailable: {trend_data['error']}")
        return
    
    # Emerging Trends
    if trend_data.get("emerging_trends"):
        st.subheader("🌱 Emerging Trends")
        for trend in trend_data["emerging_trends"]:
            st.markdown(f"• {trend}")
    
    # Recurring Themes
    if trend_data.get("recurring_themes"):
        st.subheader("🔄 Recurring Themes")
        for theme in trend_data["recurring_themes"]:
            st.markdown(f"• {theme}")
    
    # Research Gaps
    if trend_data.get("research_gaps"):
        st.subheader("🔍 Research Gaps")
        for gap in trend_data["research_gaps"]:
            st.markdown(f"• {gap}")
    
    # Future Directions
    if trend_data.get("future_directions"):
        st.subheader("🚀 Future Directions")
        for direction in trend_data["future_directions"]:
            st.markdown(f"• {direction}")
    
    # Full Analysis
    if trend_data.get("analysis_text"):
        st.subheader("📊 Complete Trend Analysis")
        st.markdown(trend_data["analysis_text"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualizations
    if enable_visualizations and trend_data:
        display_trend_visualizations(trend_data)
    
    # Word cloud generation
    if enable_wordcloud and trend_data:
        display_wordcloud_analysis(summaries)

def display_trend_visualizations(trend_data: Dict):
    """Display trend visualizations"""
    
    st.subheader("📊 Trend Visualizations")
    
    # Create trend categories data
    categories = []
    counts = []
    
    if trend_data.get("emerging_trends"):
        categories.append("Emerging Trends")
        counts.append(len(trend_data["emerging_trends"]))
    
    if trend_data.get("recurring_themes"):
        categories.append("Recurring Themes")
        counts.append(len(trend_data["recurring_themes"]))
    
    if trend_data.get("research_gaps"):
        categories.append("Research Gaps")
        counts.append(len(trend_data["research_gaps"]))
    
    if trend_data.get("future_directions"):
        categories.append("Future Directions")
        counts.append(len(trend_data["future_directions"]))
    
    if categories:
        # Bar chart
        fig = px.bar(
            x=categories, 
            y=counts,
            title="Trend Analysis Categories",
            labels={'x': 'Category', 'y': 'Number of Items'},
            color=counts,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def display_wordcloud_analysis(summaries: Dict):
    """Generate and display word clouds from research content"""
    
    st.subheader("☁️ Word Cloud Analysis")
    
    try:
        # Combine all text content for word cloud
        text_content = ""
        
        if summaries.get("executive_summary"):
            text_content += summaries["executive_summary"] + " "
        
        if summaries.get("detailed_analysis"):
            text_content += summaries["detailed_analysis"] + " "
        
        if summaries.get("key_findings"):
            text_content += " ".join(summaries["key_findings"]) + " "
        
        if summaries.get("trend_analysis", {}).get("analysis_text"):
            text_content += summaries["trend_analysis"]["analysis_text"] + " "
        
        if not text_content.strip():
            st.warning("No text content available for word cloud generation.")
            return
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            stopwords=set(['said', 'say', 'says', 'also', 'would', 'could', 'one', 'two', 'may', 'might', 'much', 'many'])
        ).generate(text_content)
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.title('Research Content Word Cloud', fontsize=16, fontweight='bold')
        
        # Convert to bytes for Streamlit
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
        img_buffer.seek(0)
        
        # Display in Streamlit
        st.image(img_buffer, caption='Word frequency visualization from your research content')
        
        # Close the matplotlib figure to free memory
        plt.close(fig)
        
        # Generate frequency analysis
        st.subheader("📈 Word Frequency Analysis")
        
        # Get word frequencies
        word_freq = wordcloud.words_
        
        if word_freq:
            # Create a bar chart of top words
            top_words = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15])
            
            fig_freq = px.bar(
                x=list(top_words.values()),
                y=list(top_words.keys()),
                orientation='h',
                title='Top 15 Most Frequent Words',
                labels={'x': 'Frequency', 'y': 'Words'},
                color=list(top_words.values()),
                color_continuous_scale='Blues'
            )
            fig_freq.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_freq, use_container_width=True)
            
            # Download word cloud
            img_buffer.seek(0)
            st.download_button(
                label="📋 Download Word Cloud",
                data=img_buffer.getvalue(),
                file_name=f"wordcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        
    except Exception as e:
        st.error(f"Failed to generate word cloud: {str(e)}")
        st.info("Make sure you have sufficient text content for analysis.")

def display_analysis_tab(summaries: Dict, enable_visualizations: bool):
    """Display analysis tab content"""
    
    # Source Analysis
    source_data = summaries.get("source_analysis", {})
    if source_data:
        st.subheader("📊 Source Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Sources", source_data.get('total_sources', 0))
            st.metric("Unique Domains", source_data.get('unique_domains', 0))
        
        with col2:
            st.metric("Diversity Score", f"{source_data.get('diversity_score', 0):.2f}")
            st.metric("Source Quality", source_data.get('source_quality', 'Unknown'))
        
        # Domain Categories
        domain_categories = source_data.get('domain_categories', {})
        if domain_categories:
            st.subheader("🏛️ Domain Categories")
            
            for category, domains in domain_categories.items():
                if domains:
                    st.markdown(f"**{category.title()}:** {', '.join(domains)}")
    
    # Citations
    citations = summaries.get("citations", [])
    if citations:
        st.subheader("📚 Citations")
        
        citation_format = st.selectbox("Citation Format", ["APA", "MLA"])
        
        for citation in citations:
            with st.expander(f"Citation {citation['id']}: {citation['title'][:50]}..."):
                if citation_format == "APA":
                    st.markdown(f"**APA Format:**\n{citation['apa_format']}")
                else:
                    st.markdown(f"**MLA Format:**\n{citation['mla_format']}")
                
                st.markdown(f"**URL:** {citation['url']}")
                if citation.get('author'):
                    st.markdown(f"**Author:** {citation['author']}")
                if citation.get('publish_date'):
                    st.markdown(f"**Published:** {citation['publish_date']}")

def display_export_tab(results: Dict):
    """Display export tab content with enhanced PDF generation"""
    
    st.subheader("📄 Export Research Report")
    
    # Generate report text for preview
    summarizer = AISummarizer()
    report_text = summarizer.generate_research_report(results['summaries'], results['query'])
    
    # Export statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Report Length", f"{len(report_text):,} chars")
    with col2:
        st.metric("Word Count", f"{len(report_text.split()):,} words")
    with col3:
        st.metric("Sources", len(results.get('extracted_content', [])))
    with col4:
        st.metric("Export Formats", "5 available")
    
    # Quick export buttons (optimized for speed)
    st.subheader("⚡ Quick Export")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📄 PDF Report", use_container_width=True, type="primary"):
            try:
                # Generate PDF using the PDF generator
                import tempfile
                import os
                
                # Create temporary file
                temp_dir = tempfile.mkdtemp()
                pdf_filename = f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf_path = os.path.join(temp_dir, pdf_filename)
                
                # Show progress
                with st.spinner("Generating PDF report..."):
                    pdf_generator = PDFGenerator()
                    pdf_generator.generate_research_report(results, pdf_path)
                
                # Read the PDF file
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                
                # Clean up temporary file
                os.remove(pdf_path)
                os.rmdir(temp_dir)
                
                # Provide download
                st.download_button(
                    label="📋 Download PDF Report",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="pdf_download"
                )
                
                st.success("🎉 PDF generated successfully!")
                
            except Exception as e:
                st.error(f"❌ PDF generation failed: {str(e)}")
                st.info("Trying fallback method...")
                
                # Fallback to simple text-based PDF
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.platypus import SimpleDocTemplate, Paragraph
                    from reportlab.lib.styles import getSampleStyleSheet
                    
                    temp_dir = tempfile.mkdtemp()
                    pdf_filename = f"research_report_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    pdf_path = os.path.join(temp_dir, pdf_filename)
                    
                    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
                    styles = getSampleStyleSheet()
                    story = []
                    
                    # Add title
                    story.append(Paragraph(f"Research Report: {results['query']}", styles['Title']))
                    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
                    
                    # Add content
                    for line in report_text.split('\n'):
                        if line.strip():
                            if line.startswith('#'):
                                story.append(Paragraph(line.replace('#', ''), styles['Heading1']))
                            elif line.startswith('##'):
                                story.append(Paragraph(line.replace('##', ''), styles['Heading2']))
                            else:
                                story.append(Paragraph(line, styles['Normal']))
                    
                    doc.build(story)
                    
                    with open(pdf_path, 'rb') as pdf_file:
                        pdf_data = pdf_file.read()
                    
                    os.remove(pdf_path)
                    os.rmdir(temp_dir)
                    
                    st.download_button(
                        label="📋 Download Simple PDF",
                        data=pdf_data,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        key="simple_pdf_download"
                    )
                    
                    st.success("🎉 Simple PDF generated successfully!")
                    
                except Exception as fallback_error:
                    st.error(f"❌ Both PDF methods failed: {str(fallback_error)}")
    
    with col2:
        # Fast Markdown export
        st.download_button(
            label="📄 Markdown",
            data=report_text,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col3:
        # Fast JSON export
        json_data = json.dumps(results, indent=2, default=str)
        st.download_button(
            label="📊 JSON Data",
            data=json_data,
            file_name=f"research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col4:
        # Fast CSV export
        sources_data = []
        for content in results.get('extracted_content', []):
            sources_data.append({
                'Title': content.get('title', ''),
                'URL': content.get('url', ''),
                'Domain': content.get('domain', ''),
                'Word Count': content.get('word_count', 0),
                'Authors': ', '.join(content.get('authors', [])),
                'Publish Date': content.get('publish_date', '')
            })
        
        if sources_data:
            df = pd.DataFrame(sources_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📈 Sources CSV",
                data=csv,
                file_name=f"research_sources_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("📈 No Sources", disabled=True, use_container_width=True)
    
    with col5:
        # Fast image export
        image_results = [r for r in results.get('search_results', []) if r.get('result_type') == 'image']
        if image_results:
            image_data = []
            for img in image_results:
                image_data.append({
                    'Title': img.get('title', ''),
                    'Image URL': img.get('image_url', ''),
                    'Source': img.get('source', '')
                })
            
            df_images = pd.DataFrame(image_data)
            csv_images = df_images.to_csv(index=False)
            st.download_button(
                label="🖼️ Image URLs",
                data=csv_images,
                file_name=f"research_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("🖼️ No Images", disabled=True, use_container_width=True)

def display_research_history():
    """Display research history"""
    
    with st.sidebar:
        st.subheader("📚 Research History")
        
        for i, history_item in enumerate(reversed(st.session_state.research_history[-5:]), 1):
            with st.expander(f"{i}. {history_item['query'][:30]}..."):
                st.write(f"**Query:** {history_item['query']}")
                st.write(f"**Sources:** {history_item['sources_count']}")
                st.write(f"**Date:** {history_item['timestamp'][:19]}")
                
                if st.button(f"🔍 Repeat", key=f"repeat_{i}"):
                    st.session_state.search_query = history_item['query']
                    st.rerun()

if __name__ == "__main__":
    main()

# Helper functions for testing enhanced features
def test_market_analysis():
    """Test market data analysis functionality"""
    try:
        analyzer = HistoricalDataAnalyzer()
        result = analyzer.get_stock_trends('AAPL', '1y')
        
        if result.get('success'):
            st.success(f"✅ Market data test successful!")
            st.json({
                'symbol': result['symbol'],
                'current_price': result['current_price'],
                'price_change_pct': result['price_change_pct'],
                'data_points': result['data_points']
            })
            
            # Display chart if available
            if result.get('chart_html'):
                st.components.v1.html(result['chart_html'], height=400)
                
        else:
            st.error(f"❌ Market data test failed: {result.get('error')}")
            
    except Exception as e:
        st.error(f"❌ Market data test error: {str(e)}")

def test_image_search():
    """Test image search functionality"""
    try:
        processor = EnhancedImageProcessor()
        result = processor.search_high_quality_images('artificial intelligence trends', 5)
        
        if result.get('success'):
            st.success(f"✅ Image search test successful! Found {result['total_found']} images")
            
            # Display sample images
            if result['images']:
                cols = st.columns(min(3, len(result['images'])))
                for i, img in enumerate(result['images'][:3]):
                    with cols[i]:
                        if img.get('thumbnail'):
                            try:
                                st.image(img['thumbnail'], caption=img.get('title', 'Image')[:50])
                            except:
                                st.write(f"Image: {img.get('title', 'Untitled')}")
                        st.write(f"Source: {img.get('source')}")
                        st.write(f"Quality: {img.get('quality_score', 'N/A')}")
        else:
            st.error(f"❌ Image search test failed: {result.get('error')}")
            
    except Exception as e:
        st.error(f"❌ Image search test error: {str(e)}")

def display_historical_analysis(historical_data):
    """Display historical data analysis results"""
    if not historical_data or not historical_data.get('success'):
        return
    
    st.subheader("📈 Historical Analysis")
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Value",
            value=f"${historical_data.get('current_price', 0):.2f}" if 'current_price' in historical_data else historical_data.get('current_value', 'N/A'),
            delta=f"{historical_data.get('price_change_pct', 0):+.2f}%" if 'price_change_pct' in historical_data else None
        )
    
    with col2:
        st.metric(
            label="Period",
            value=historical_data.get('period', 'N/A')
        )
    
    with col3:
        st.metric(
            label="Data Points",
            value=historical_data.get('data_points', 0)
        )
    
    with col4:
        st.metric(
            label="Trend",
            value=historical_data.get('trend', 'N/A')
        )
    
    # Display chart if available
    if historical_data.get('chart_html'):
        st.components.v1.html(historical_data['chart_html'], height=500, scrolling=True)
    
    # Display summary
    if historical_data.get('summary'):
        st.markdown("### 📊 Analysis Summary")
        st.markdown(historical_data['summary'])

def display_image_results(image_results):
    """Display image search results"""
    if not image_results or not image_results.get('success'):
        return
    
    st.subheader("🖼️ Image Analysis")
    
    images = image_results.get('images', [])
    if not images:
        st.info("No images found")
        return
    
    # Display images in grid
    cols_per_row = 3
    for i in range(0, len(images), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            img_idx = i + j
            if img_idx < len(images):
                img = images[img_idx]
                
                with col:
                    # Display image
                    if img.get('thumbnail'):
                        try:
                            st.image(img['thumbnail'], use_column_width=True)
                        except:
                            st.write("🖼️ Image unavailable")
                    
                    # Display metadata
                    st.caption(img.get('title', 'Untitled')[:100])
                    st.caption(f"Source: {img.get('source', 'Unknown')}")
                    
                    if img.get('quality_score'):
                        st.caption(f"Quality: {img['quality_score']}/10")
                    
                    # Add trend relevance if available
                    if img.get('trend_relevance'):
                        st.caption(f"Relevance: {img['trend_relevance']:.2f}")
