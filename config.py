"""
Configuration settings for AI Research Agent
Enhanced for historical data, trends, and image analysis
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # ⚡ PRIMARY AI PROVIDERS ⚡
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # ✅ ACTIVE
    PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')  # ✅ ACTIVE
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')  # ✅ ACTIVE
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # 🆓 AVAILABLE
    
    # 🆕 ADDITIONAL FREE AI PROVIDERS 🆕
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')  # 🆓 FREE
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')  # 🆓 FREE
    TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')  # 🆓 FREE
    OLLAMA_ENABLED = os.getenv('OLLAMA_ENABLED', 'true')  # 🆓 LOCAL
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')  # 🆓 LOCAL
    
    # 🌐 SEARCH ENGINES 🌐
    GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')  # DISABLED - invalid
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')  # ✅ WORKING
    BING_SEARCH_API_KEY = os.getenv('BING_SEARCH_API_KEY')
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')  # DISABLED - invalid
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')  # ✅ WORKING
    YOU_API_KEY = os.getenv('YOU_API_KEY')
    EXA_API_KEY = os.getenv('EXA_API_KEY')  # ✅ WORKING
    SEARCHAPI_KEY = os.getenv('SEARCHAPI_KEY')  # ✅ WORKING
    SCALESERP_API_KEY = os.getenv('SCALESERP_API_KEY')
    
    # 📊 HISTORICAL DATA & TRENDS APIS 📊
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
    FRED_API_KEY = os.getenv('FRED_API_KEY')
    WORLD_BANK_API_ENABLED = os.getenv('WORLD_BANK_API_ENABLED', 'true')
    QUANDL_API_KEY = os.getenv('QUANDL_API_KEY')
    YFINANCE_ENABLED = os.getenv('YFINANCE_ENABLED', 'true')
    FMP_API_KEY = os.getenv('FMP_API_KEY', 'demo')
    
    # 🖼️ IMAGE SEARCH & ANALYSIS APIS 🖼️
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
    
    # 📊 VISUALIZATION & CHARTING 📊
    CHARTJS_ENABLED = os.getenv('CHARTJS_ENABLED', 'true')
    PLOTLY_ENABLED = os.getenv('PLOTLY_ENABLED', 'true')
    GOOGLE_CHARTS_ENABLED = os.getenv('GOOGLE_CHARTS_ENABLED', 'true')
    
    # 📱 SOCIAL MEDIA TRENDS 📱
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'AIResearchAgent/1.0')
    
    # API Key Validation
    @classmethod
    def validate_api_keys(cls):
        """Comprehensive API key validation for all services"""
        valid_keys = {
            'ai_providers': [],
            'search_engines': [],
            'historical_data': [],
            'image_services': [],
            'social_media': [],
            'issues': [],
            'working_count': 0,
            'total_available': 0
        }
        
        # Check AI providers - enhanced validation
        if cls.OPENAI_API_KEY and cls.OPENAI_API_KEY.startswith('sk-'):
            valid_keys['ai_providers'].append('OpenAI')
            
        if cls.PERPLEXITY_API_KEY and cls.PERPLEXITY_API_KEY.startswith('pplx-'):
            valid_keys['ai_providers'].append('Perplexity')
            
        if cls.ANTHROPIC_API_KEY and cls.ANTHROPIC_API_KEY.startswith('sk-ant-'):
            valid_keys['ai_providers'].append('Anthropic')
        
        if cls.GEMINI_API_KEY and cls.GEMINI_API_KEY.startswith('AIza'):  # More specific validation
            valid_keys['ai_providers'].append('Gemini')
        
        # Check additional free AI providers
        if cls.HUGGINGFACE_API_KEY and cls.HUGGINGFACE_API_KEY.startswith('hf_'):
            valid_keys['ai_providers'].append('Hugging Face')
            
        if cls.COHERE_API_KEY and cls.COHERE_API_KEY.startswith('co-'):
            valid_keys['ai_providers'].append('Cohere')
            
        if cls.TOGETHER_API_KEY and cls.TOGETHER_API_KEY.startswith('together_'):
            valid_keys['ai_providers'].append('Together AI')
            
        if cls.OLLAMA_ENABLED == 'true':
            valid_keys['ai_providers'].append('Ollama (Local)')
        
        # Check search engines
        if cls.SERPAPI_API_KEY and len(cls.SERPAPI_API_KEY) > 20:
            valid_keys['search_engines'].append('SerpAPI')
            
        if cls.TAVILY_API_KEY and cls.TAVILY_API_KEY.startswith('tvly-'):
            valid_keys['search_engines'].append('Tavily')
            
        if cls.EXA_API_KEY and len(cls.EXA_API_KEY) > 20:
            valid_keys['search_engines'].append('Exa')
            
        if cls.SEARCHAPI_KEY and len(cls.SEARCHAPI_KEY) > 10:
            valid_keys['search_engines'].append('SearchAPI')
        
        # Check historical data sources
        if cls.YFINANCE_ENABLED == 'true':
            valid_keys['historical_data'].append('Yahoo Finance')
            
        if cls.WORLD_BANK_API_ENABLED == 'true':
            valid_keys['historical_data'].append('World Bank')
            
        if cls.ALPHA_VANTAGE_API_KEY and cls.ALPHA_VANTAGE_API_KEY != 'demo':
            valid_keys['historical_data'].append('Alpha Vantage')
        elif cls.ALPHA_VANTAGE_API_KEY == 'demo':
            valid_keys['historical_data'].append('Alpha Vantage (Demo)')
            
        if cls.FRED_API_KEY and not cls.FRED_API_KEY.endswith('_here'):
            valid_keys['historical_data'].append('FRED')
        
        # Check image services
        if cls.UNSPLASH_ACCESS_KEY and not cls.UNSPLASH_ACCESS_KEY.endswith('_here'):
            valid_keys['image_services'].append('Unsplash')
            
        if cls.PIXABAY_API_KEY and not cls.PIXABAY_API_KEY.endswith('_here'):
            valid_keys['image_services'].append('Pixabay')
        
        # Check social media APIs
        if cls.TWITTER_BEARER_TOKEN and not cls.TWITTER_BEARER_TOKEN.endswith('_here'):
            valid_keys['social_media'].append('Twitter')
            
        if cls.REDDIT_CLIENT_ID and not cls.REDDIT_CLIENT_ID.endswith('_here'):
            valid_keys['social_media'].append('Reddit')
        
        # Calculate totals
        for category in ['ai_providers', 'search_engines', 'historical_data', 'image_services', 'social_media']:
            valid_keys['working_count'] += len(valid_keys[category])
        
        valid_keys['total_available'] = valid_keys['working_count']
        
        return valid_keys
    
    @classmethod
    def get_working_ai_provider(cls):
        """Get the best working AI provider in priority order"""
        validation = cls.validate_api_keys()
        ai_providers = validation['ai_providers']
        
        # Priority: Gemini (free) → Perplexity (real-time) → Anthropic (quality) → OpenAI (fallback)
        if 'Gemini' in ai_providers:
            return 'gemini'
        elif 'Perplexity' in ai_providers:
            return 'perplexity'
        elif 'Anthropic' in ai_providers:
            return 'anthropic' 
        elif 'OpenAI' in ai_providers:
            return 'openai'
        else:
            return None
    
    @classmethod
    def get_working_search_engines(cls):
        """Get list of working search engines in priority order"""
        validation = cls.validate_api_keys()
        return validation['search_engines']
    
    @classmethod
    def get_historical_data_sources(cls):
        """Get available historical data sources"""
        validation = cls.validate_api_keys()
        return validation['historical_data']
    
    @classmethod
    def get_image_services(cls):
        """Get available image services"""
        validation = cls.validate_api_keys()
        return validation['image_services']
    
    @classmethod
    def has_trend_analysis_capability(cls):
        """Check if trend analysis is possible with current APIs"""
        validation = cls.validate_api_keys()
        return (
            len(validation['ai_providers']) > 0 and 
            len(validation['search_engines']) > 0 and 
            len(validation['historical_data']) > 0
        )
    
    @classmethod
    def get_comprehensive_status(cls):
        """Get comprehensive status of all API configurations"""
        validation = cls.validate_api_keys()
        
        status = {
            'overall_health': 'Excellent' if validation['working_count'] > 8 else 
                            'Good' if validation['working_count'] > 5 else 
                            'Limited' if validation['working_count'] > 2 else 'Critical',
            'capabilities': {
                'ai_analysis': len(validation['ai_providers']) > 0,
                'web_search': len(validation['search_engines']) > 0,
                'historical_trends': len(validation['historical_data']) > 0,
                'image_analysis': len(validation['image_services']) > 0,
                'social_trends': len(validation['social_media']) > 0,
                'comprehensive_research': validation['working_count'] > 5
            },
            'working_apis': validation['working_count'],
            'total_configured': validation['total_available'],
            'ready_for_production': validation['working_count'] > 3
        }
        
        return status
    
    # 🔧 TECHNICAL CONFIGURATION 🔧
    
    # AI Model Settings
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    PERPLEXITY_MODEL = os.getenv('PERPLEXITY_MODEL', 'sonar-small-chat')
    ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonar-20240620')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.1))
    MAX_TOKENS = 2000
    
    # Search Settings
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', 10))
    SEARCH_TIMEOUT = int(os.getenv('SEARCH_TIMEOUT', 30))
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_EXPIRY_HOURS = int(os.getenv('CACHE_EXPIRY_HOURS', 24))
    MAX_CONTENT_LENGTH = 5000
    
    # Image Processing Settings
    IMAGE_ANALYSIS_ENABLED = os.getenv('IMAGE_ANALYSIS_ENABLED', 'true').lower() == 'true'
    OCR_ENABLED = os.getenv('OCR_ENABLED', 'true').lower() == 'true'
    MAX_IMAGE_SIZE_MB = int(os.getenv('MAX_IMAGE_SIZE_MB', 10))
    
    # Data Visualization Settings
    MAX_DATA_POINTS = int(os.getenv('MAX_DATA_POINTS', 1000))
    CHART_DEFAULT_WIDTH = int(os.getenv('CHART_DEFAULT_WIDTH', 800))
    CHART_DEFAULT_HEIGHT = int(os.getenv('CHART_DEFAULT_HEIGHT', 600))
    HISTORICAL_DATA_YEARS = int(os.getenv('HISTORICAL_DATA_YEARS', 5))
    
    PARALLEL_REQUESTS = os.getenv('PARALLEL_REQUESTS', 'true').lower() == 'true'
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 5))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', 3))
    REQUEST_DELAY_MS = int(os.getenv('REQUEST_DELAY_MS', 100))
    
    # Enhanced Features
    ENABLE_REAL_TIME_SEARCH = True
    PARALLEL_AI_PROCESSING = True
    FAST_MODE = True
    ENABLE_TREND_ANALYSIS = True
    TREND_WINDOW_DAYS = 365  # Full year for historical analysis
    MIN_TREND_SOURCES = 3
    
    # Content Extraction Settings
    MIN_ARTICLE_LENGTH = 200
    MAX_ARTICLE_LENGTH = 10000
    
    # Export Settings
    PDF_TITLE = "AI Research Report with Historical Analysis"
    MARKDOWN_TITLE = "# AI Research Report with Historical Trends"
    
    # 🎯 FEATURE FLAGS 🎯
    ENABLE_ENHANCED_MODE = True
    ENABLE_HISTORICAL_ANALYSIS = True
    ENABLE_IMAGE_TRENDS = True
    ENABLE_SOCIAL_SENTIMENT = True
    ENABLE_REAL_TIME_DATA = True
    ENABLE_PARALLEL_PROCESSING = True
    PARALLEL_REQUESTS = os.getenv('PARALLEL_REQUESTS', 'true').lower() == 'true'
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 5))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', 3))
    REQUEST_DELAY_MS = int(os.getenv('REQUEST_DELAY_MS', 100))
    
    # Enhanced Features
    ENABLE_REAL_TIME_SEARCH = True
    PARALLEL_AI_PROCESSING = True
    FAST_MODE = True
    ENABLE_TREND_ANALYSIS = True
    TREND_WINDOW_DAYS = 365  # Full year for historical analysis
    MIN_TREND_SOURCES = 3
    
    # Content Extraction Settings
    MIN_ARTICLE_LENGTH = 200
    MAX_ARTICLE_LENGTH = 10000
    
    # Export Settings
    PDF_TITLE = "AI Research Report with Historical Analysis"
    MARKDOWN_TITLE = "# AI Research Report with Historical Trends"
