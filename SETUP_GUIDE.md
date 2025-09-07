# 🚀 AI Research Agent - Complete Setup Guide

This guide will walk you through setting up the AI Research Agent step by step, ensuring everything works perfectly in VS Code.

## 📋 Prerequisites

- **Python 3.8 or higher** (Check with `python --version`)
- **VS Code** with Python extension
- **Git** (optional, for version control)
- **Internet connection** for API access

## 🔧 Step 1: Environment Setup

### 1.1 Create Virtual Environment
Open VS Code terminal and run:

```bash
# Create virtual environment
python -m venv ai_research_env

# Activate virtual environment (Windows)
ai_research_env\Scripts\activate

# Activate virtual environment (Mac/Linux)
source ai_research_env/bin/activate
```

### 1.2 Verify Python Installation
```bash
python --version
pip --version
```

## 📦 Step 2: Install Dependencies

### 2.1 Install Required Packages
```bash
pip install -r requirements.txt
```

### 2.2 Verify Installation
```bash
pip list
```

You should see all packages listed including:
- streamlit
- requests
- beautifulsoup4
- newspaper3k
- openai
- pandas
- plotly
- reportlab
- And many more...

## 🔑 Step 3: API Configuration

### 3.1 Create Environment File
```bash
# Copy the example file
copy env_example.txt .env
```

### 3.2 Configure API Keys

Open `.env` file and add your API keys:

```env
# Required: OpenAI API Key (for AI summarization)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Google Custom Search API
GOOGLE_SEARCH_API_KEY=your-google-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id

# Optional: SerpAPI Key
SERPAPI_API_KEY=your-serpapi-key

# Optional: Bing Search API
BING_SEARCH_API_KEY=your-bing-api-key

# Optional: NewsAPI Key
NEWSAPI_KEY=your-newsapi-key
```

### 3.3 Get API Keys

#### OpenAI API Key (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up/Login
3. Go to API Keys section
4. Create new secret key
5. Copy and paste into `.env` file

#### Google Custom Search API (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Custom Search API
4. Create credentials (API Key)
5. Create Custom Search Engine at [Google Custom Search](https://cse.google.com/)
6. Get Search Engine ID

#### SerpAPI (Optional)
1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for free account
3. Get API key from dashboard

#### Bing Search API (Optional)
1. Go to [Azure Portal](https://portal.azure.com/)
2. Create Bing Search v7 resource
3. Get API key from resource

#### NewsAPI (Optional)
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for free account
3. Get API key from dashboard

## 🧪 Step 4: Test Installation

### 4.1 Test Individual Modules
```bash
# Test web search module
python -c "from modules.web_search import WebSearchEngine; print('Web search module OK')"

# Test content extractor
python -c "from modules.content_extractor import ContentExtractor; print('Content extractor OK')"

# Test AI summarizer
python -c "from modules.ai_summarizer import AISummarizer; print('AI summarizer OK')"
```

### 4.2 Test Configuration
```bash
python -c "from config import Config; c = Config(); print('Configuration loaded successfully')"
```

## 🚀 Step 5: Run the Application

### 5.1 Start the Streamlit App
```bash
streamlit run app.py
```

### 5.2 Access the Application
- The app will open automatically in your browser
- If not, go to: `http://localhost:8501`
- You should see the AI Research Agent interface

## 🔍 Step 6: Test Research Functionality

### 6.1 Basic Test Query
Try searching for: "artificial intelligence breakthroughs 2024"

### 6.2 Expected Workflow
1. Enter query in search box
2. Click "Start Research"
3. Watch progress indicators
4. View results in tabs:
   - Summary
   - Sources
   - Trends (unique feature)
   - Analysis
   - Export

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Issue 1: Module Import Errors
```bash
# Solution: Reinstall packages
pip install --upgrade -r requirements.txt
```

#### Issue 2: API Key Errors
- Check `.env` file exists and has correct format
- Verify API keys are valid and active
- Ensure no extra spaces in API keys

#### Issue 3: Streamlit Not Starting
```bash
# Solution: Update streamlit
pip install --upgrade streamlit

# Or try alternative port
streamlit run app.py --server.port 8502
```

#### Issue 4: Content Extraction Fails
- Check internet connection
- Some websites block automated access
- Try different search queries

#### Issue 5: OpenAI API Errors
- Verify API key is correct
- Check API usage limits
- Ensure sufficient credits

### Debug Mode
Run with debug information:
```bash
streamlit run app.py --logger.level debug
```

## 📁 Project Structure

```
ai_research_agent/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md              # Project documentation
├── SETUP_GUIDE.md         # This setup guide
├── modules/               # Core modules
│   ├── __init__.py
│   ├── web_search.py      # Web search functionality
│   ├── content_extractor.py # Content extraction
│   └── ai_summarizer.py   # AI summarization
├── utils/                 # Utility modules
│   ├── __init__.py
│   └── pdf_generator.py   # PDF report generation
├── templates/             # HTML templates (future)
├── static/               # Static assets (future)
└── ai_research_env/      # Virtual environment (created)
```

## 🎯 Next Steps

1. **Explore Features**: Try different research queries
2. **Customize Settings**: Modify `config.py` for your needs
3. **Add More APIs**: Configure additional search APIs
4. **Export Reports**: Try PDF and Markdown exports
5. **Trend Analysis**: Explore the unique trend analysis feature

## 📞 Support

If you encounter issues:

1. Check this setup guide first
2. Verify all dependencies are installed
3. Test API keys individually
4. Check VS Code Python interpreter is set to virtual environment
5. Review error messages in terminal

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ Streamlit app starts without errors
- ✅ You can enter a research query
- ✅ Search results appear
- ✅ Content extraction works
- ✅ AI summary is generated
- ✅ Trend analysis shows insights
- ✅ Export functions work

## 🔄 Updates and Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update API Keys
- Regularly check API key expiration
- Monitor usage limits
- Update keys in `.env` file as needed

### Backup Configuration
- Keep `.env` file secure
- Don't commit API keys to version control
- Backup your configuration

---

**🎊 Congratulations!** You now have a fully functional AI Research Agent running in VS Code!
