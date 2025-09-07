# Streamlit Community Cloud entry point
# This file helps with deployment on Streamlit Community Cloud

import streamlit as st
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the main app
try:
    from app_streamlined_deployment import main
    
    # Set page config for deployment
    st.set_page_config(
        page_title="AI Research Agent - Live Demo",
        page_icon="🤖📚",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/TESLAsidd/ai-agent-research',
            'Report a bug': 'https://github.com/TESLAsidd/ai-agent-research/issues',
            'About': """
            # 🤖 AI Research Agent
            
            **Intelligent Research Automation with Dual-Speed Processing**
            
            Built for hackathons and professional use!
            
            - ⚡ Quick Search (2-8 seconds)
            - 🔬 Advanced Search (8-20 seconds)  
            - 🤖 Multi-AI Integration (8 providers)
            - 📄 Professional Reports
            - 🎨 Day/Night Themes
            
            **GitHub**: https://github.com/TESLAsidd/ai-agent-research
            """
        }
    )
    
    # Initialize session state first
    if 'research_results' not in st.session_state:
        st.session_state.research_results = None
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "day"
    
    # Run the main application
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.info("Please ensure all required modules are available.")
    st.stop()
except Exception as e:
    st.error(f"❌ Application Error: {e}")
    st.info("There was an issue loading the application. Please check the logs.")
    st.stop()