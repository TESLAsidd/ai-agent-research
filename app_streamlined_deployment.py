"""
AI Research Agent - Optimized Streamlined Version for Live Deployment
Optimized for performance, minimal dependencies, and Streamlit Cloud deployment
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import time
import os
import logging
from typing import Dict, List

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

# Page configuration for deployment
st.set_page_config(
    page_title="AI Research Agent - Live Demo",
    page_icon="🤖📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/TESLAsidd/ai-agent-research',
        'Report a bug': 'https://github.com/TESLAsidd/ai-agent-research/issues',
        'About': "# 🤖 AI Research Agent - Live Demo\n\n**Intelligent Research Automation**\n\n- ⚡ Quick Search (2-8 seconds)\n- 🔬 Advanced Search (8-20 seconds)\n- 🤖 Multi-AI Integration\n- 📄 Professional Reports\n- 🎨 Day/Night Themes"
    }
)

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'research_history' not in st.session_state:
    st.session_state.research_history = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "day"

def safe_api_call(func, *args, **kwargs):
    """Safely call API functions with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return {"error": str(e), "success": False}

def generate_follow_up_questions(query: str, summary: Dict, keywords: List[str]) -> List[str]:
    """
    Generate intelligent follow-up questions based on the research summary
    """
    try:
        questions = []
        
        # Generate topic-specific questions with more variety
        if any(term in query.lower() for term in ['technology', 'ai', 'artificial intelligence', 'machine learning']):
            questions.extend([
                f"What are the latest breakthrough developments in {query}?",
                f"How is {query} being implemented across different industries?",
                f"What are the potential risks and benefits of {query}?",
                f"What future trends and innovations can we expect in {query}?"
            ])
        
        if any(term in query.lower() for term in ['market', 'business', 'economy', 'finance']):
            questions.extend([
                f"What is the current market size and growth potential for {query}?",
                f"Who are the key players and competitors in the {query} market?",
                f"What are the investment opportunities in {query}?",
                f"How is {query} affecting consumer behavior and preferences?"
            ])
        
        if any(term in query.lower() for term in ['health', 'medical', 'medicine', 'treatment']):
            questions.extend([
                f"What are the latest clinical trial results for {query}?",
                f"How does {query} compare to existing treatments and therapies?",
                f"What are the side effects or limitations of {query}?",
                f"When will {query} be widely available to patients?"
            ])
        
        if any(term in query.lower() for term in ['climate', 'environment', 'sustainability', 'green']):
            questions.extend([
                f"What are the latest findings on {query} and its impacts?",
                f"What solutions are being developed to address {query}?",
                f"How is {query} affecting different regions of the world?",
                f"What policies are being implemented regarding {query}?"
            ])
        
        # Generate keyword-based questions
        if keywords:
            for keyword in keywords[:3]:  # Use top 3 keywords
                questions.append(f"Can you explain more about {keyword.title()} in relation to {query}?")
                questions.append(f"How does {keyword.title()} impact the future of {query}?")
        
        # Generic insightful questions
        questions.extend([
            f"What are the global implications and effects of {query}?",
            f"How has {query} evolved over the past few years?",
            f"What research is currently being conducted on {query}?",
            f"What do experts predict about {query}?"
        ])
        
        # Remove duplicates and return top 8 questions
        unique_questions = list(dict.fromkeys(questions))  # Preserves order while removing duplicates
        return unique_questions[:8]
        
    except Exception as e:
        logger.error(f"Follow-up question generation failed: {str(e)}")
        return [
            f"What are the latest developments in {query}?",
            f"How does {query} impact different industries?",
            f"What are the future trends for {query}?",
            f"What are the main challenges with {query}?"
        ]

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
        
        # Display questions in an interactive grid
        cols = st.columns(2)
        
        for i, question in enumerate(follow_up_questions):
            with cols[i % 2]:
                if st.button(question, key=f"followup_{i}", use_container_width=True):
                    # When clicked, populate the search box with this question
                    st.session_state.search_query = question
                    st.success(f"Ready to research: {question}")
                    st.info("Click the 'Start Research' button above to begin exploring this question.")
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Create Your Own Question")
        st.markdown("Have a specific aspect you want to explore further?")
        
        custom_question = st.text_input("Enter your custom research question:", 
                                       placeholder=f"e.g., What are the implications of {results['query']} for...")
        
        if st.button("Research Custom Question") and custom_question:
            st.session_state.search_query = custom_question
            st.success(f"Ready to research: {custom_question}")
            st.info("Click the 'Start Research' button above to begin your custom research.")
    else:
        st.info("No follow-up questions generated for this research topic. Try a different query for more insights.")

def main():
    """Main application function - streamlined for deployment"""
    
    # Header
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;"><h1>🤖 AI Research Agent</h1><h3>Intelligent Research Automation</h3></div>', unsafe_allow_html=True)
    
    # Show feature status
    feature_count = sum([CORE_MODULES_AVAILABLE, ENHANCED_FEATURES_AVAILABLE, HISTORICAL_DATA_AVAILABLE, IMAGE_PROCESSING_AVAILABLE])
    status_text = f"⚡ {feature_count}/4 FEATURE SETS ACTIVE"
    st.markdown(f'<div style="text-align: center; margin-bottom: 2rem;"><div style="background: #4facfe; color: white; padding: 0.5rem; border-radius: 20px; display: inline-block;">{status_text}: ⚡ Quick Search • 🔬 Advanced Search • 📊 Analysis • 📄 Export</div></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status
        try:
            config = Config()
            validation = config.validate_api_keys()
            st.subheader("📊 API Status")
            st.write(f"**Working APIs:** {validation.get('working_count', 0)}")
            if validation.get('ai_providers'):
                st.write(f"🧠 **AI:** {', '.join(validation['ai_providers'])}")
            if validation.get('search_engines'):
                st.write(f"🔍 **Search:** {', '.join(validation['search_engines'])}")
        except Exception as e:
            st.error(f"Config error: {str(e)}")
        
        # Research settings
        st.subheader("🔍 Research Settings")
        search_speed = st.radio("🚀 Search Speed", ["⚡ Quick Search", "🔬 Advanced Search"])
        
        # Dynamic settings based on search speed
        if "Quick" in search_speed:
            num_results = st.slider("Sources to analyze", 3, 5, 3)
            search_mode = "Standard"
            include_images = st.checkbox("Include images", value=False)
            include_trends = st.checkbox("Include trends", value=False)
            summary_type = "brief"
            st.info("⚡ Quick mode: Ultra-fast results")
        else:
            num_results = st.slider("Sources to analyze", 5, 15, 8)
            search_mode = st.radio("Search Engine", ["Enhanced", "Standard"]) if ENHANCED_FEATURES_AVAILABLE else "Standard"
            include_images = st.checkbox("Include images", value=False)
            include_trends = st.checkbox("Include trends", value=False)
            summary_type = st.selectbox("Analysis depth", ["detailed", "brief", "comprehensive"])
            st.info("🔬 Advanced mode: Comprehensive analysis")
        
        enable_visualizations = st.checkbox("Enable charts", value=True)
        
        # Output format options
        st.subheader("📋 Output Format")
        detailed_formatting = st.checkbox("🎨 Detailed formatting", value=True)
        include_tables = st.checkbox("📊 Data tables", value=True)
        include_bullet_points = st.checkbox("• Bullet points", value=True)
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🔍 Research Query")
        query = st.text_input(
            "Enter your research topic:",
            placeholder="e.g., AI developments, Climate solutions, Technology trends",
            value=st.session_state.search_query
        )
        search_button = st.button("🚀 Start Research", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("💪 Quick Examples")
        examples = [
            ("⚡ AI trends 2024", "AI trends 2024"), 
            ("🌍 Climate change", "Climate change"), 
            ("🚀 Space exploration", "Space exploration")
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
        display_results(st.session_state.research_results)

def display_results(results):
    """Display results with streamlined styling"""
    
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
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 15px; text-align: center; border-left: 4px solid {color};">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: {color};">{value}</div>
                <div style="color: #ccc; font-size: 0.9rem;">{label}</div>
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
        display_summary_section(results)
    
    with tab2:
        display_sources_section(results)
    
    with tab3:
        display_images_section(results)
    
    with tab4:
        display_trends_section(results)
    
    with tab5:
        display_export_section(results)
    
    with tab6:
        display_follow_up_questions(results)

def display_summary_section(results):
    """Display enhanced AI summary"""
    summary = results.get('summary', {})
    
    if summary and summary.get('success'):
        st.subheader("📝 AI-Generated Research Analysis")
        
        # Enhanced provider info
        provider = summary.get('provider', 'Unknown')
        col1, col2 = st.columns(2)
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
            if summary.get('keywords'):
                st.markdown("**🔑 Keywords:** " + ", ".join(summary['keywords'][:10]))
        
        st.divider()
        
        # Display the enhanced structured summary
        summary_text = summary.get('summary', 'No summary content available')
        st.markdown(summary_text)
    
    else:
        st.warning("❌ Summary generation encountered issues")
        if summary and summary.get('error'):
            st.error(f"Error: {summary['error']}")

def display_sources_section(results):
    """Display enhanced sources information"""
    search_results = results.get('search_results', [])
    extracted_content = results.get('extracted_content', [])
    
    # Handle different result formats
    if isinstance(search_results, dict):
        sources_list = search_results.get('search_results', [])
    else:
        sources_list = search_results
    
    # Enhanced overview
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
        # Enhanced sources display
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

def display_images_section(results):
    """Display images"""
    image_results = results.get('image_results', [])
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
    """Display trend analysis"""
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
    else:
        st.info("📈 Trend analysis not available. Enable trends in settings for financial or market research.")

def display_export_section(results):
    """Display export options"""
    st.subheader("📥 Export Research Results")
    
    # Show export readiness status
    summary_available = results.get('summary', {}).get('success', False)
    sources_available = len(results.get('search_results', [])) > 0
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
                    else:
                        st.error("❌ PDF generation failed - Invalid content")
            except Exception as e:
                st.error(f"PDF export error: {str(e)}")
        
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