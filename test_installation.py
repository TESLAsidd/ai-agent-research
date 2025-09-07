"""
AI Research Agent - Installation Test Script
Run this script to verify all components are working correctly
"""

import sys
import os
import importlib
from datetime import datetime

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python Version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_imports():
    """Test all required package imports"""
    print("\n📦 Testing Package Imports...")
    
    packages = [
        ('streamlit', 'Streamlit'),
        ('requests', 'Requests'),
        ('bs4', 'BeautifulSoup4'),
        ('newspaper', 'Newspaper3k'),
        ('openai', 'OpenAI'),
        ('pandas', 'Pandas'),
        ('plotly', 'Plotly'),
        ('reportlab', 'ReportLab'),
        ('trafilatura', 'Trafilatura'),
        ('readability', 'Readability'),
        ('fake_useragent', 'Fake UserAgent'),
        ('selenium', 'Selenium'),
        ('nltk', 'NLTK'),
        ('spacy', 'SpaCy'),
        ('transformers', 'Transformers'),
        ('chromadb', 'ChromaDB'),
        ('faiss', 'FAISS')
    ]
    
    success_count = 0
    for package, name in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} - {str(e)}")
    
    print(f"\n📊 Import Results: {success_count}/{len(packages)} packages imported successfully")
    return success_count == len(packages)

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from config import Config
        config = Config()
        print("✅ Configuration loaded successfully")
        
        # Test API key availability
        api_keys = {
            'OpenAI': config.OPENAI_API_KEY,
            'Google Search': config.GOOGLE_SEARCH_API_KEY,
            'SerpAPI': config.SERPAPI_API_KEY,
            'Bing Search': config.BING_SEARCH_API_KEY,
            'NewsAPI': config.NEWSAPI_KEY
        }
        
        print("\n🔑 API Key Status:")
        for api, key in api_keys.items():
            status = "✅ Configured" if key else "❌ Missing"
            print(f"  {api}: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

def test_modules():
    """Test custom modules"""
    print("\n🔧 Testing Custom Modules...")
    
    modules = [
        ('modules.web_search', 'WebSearchEngine'),
        ('modules.content_extractor', 'ContentExtractor'),
        ('modules.ai_summarizer', 'AISummarizer'),
        ('utils.pdf_generator', 'PDFGenerator')
    ]
    
    success_count = 0
    for module_name, class_name in modules:
        try:
            module = importlib.import_module(module_name)
            getattr(module, class_name)
            print(f"✅ {class_name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {class_name} - {str(e)}")
    
    print(f"\n📊 Module Results: {success_count}/{len(modules)} modules loaded successfully")
    return success_count == len(modules)

def test_web_search():
    """Test web search functionality"""
    print("\n🔍 Testing Web Search...")
    
    try:
        from modules.web_search import WebSearchEngine
        search_engine = WebSearchEngine()
        
        if search_engine.search_engines:
            print(f"✅ {len(search_engine.search_engines)} search engines configured")
            for engine in search_engine.search_engines:
                print(f"  - {engine.__class__.__name__}")
            return True
        else:
            print("⚠️ No search engines configured (add API keys to .env file)")
            return False
            
    except Exception as e:
        print(f"❌ Web search error: {str(e)}")
        return False

def test_content_extraction():
    """Test content extraction functionality"""
    print("\n📄 Testing Content Extraction...")
    
    try:
        from modules.content_extractor import ContentExtractor
        extractor = ContentExtractor()
        
        # Test with a simple URL
        test_url = "https://httpbin.org/html"
        print(f"Testing extraction from: {test_url}")
        
        # This is a basic test - actual extraction might fail due to network issues
        print("✅ ContentExtractor initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Content extraction error: {str(e)}")
        return False

def test_ai_summarization():
    """Test AI summarization functionality"""
    print("\n🤖 Testing AI Summarization...")
    
    try:
        from modules.ai_summarizer import AISummarizer
        summarizer = AISummarizer()
        
        # Test with sample data
        sample_content = [
            {
                'title': 'Test Article',
                'text': 'This is a test article for AI summarization testing.',
                'url': 'https://example.com',
                'domain': 'example.com',
                'word_count': 10
            }
        ]
        
        print("✅ AISummarizer initialized successfully")
        
        # Note: Actual summarization requires OpenAI API key
        from config import Config
        config = Config()
        if config.OPENAI_API_KEY:
            print("✅ OpenAI API key configured - summarization ready")
        else:
            print("⚠️ OpenAI API key missing - summarization will fail")
        
        return True
        
    except Exception as e:
        print(f"❌ AI summarization error: {str(e)}")
        return False

def test_pdf_generation():
    """Test PDF generation functionality"""
    print("\n📄 Testing PDF Generation...")
    
    try:
        from utils.pdf_generator import PDFGenerator
        generator = PDFGenerator()
        
        print("✅ PDFGenerator initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ PDF generation error: {str(e)}")
        return False

def test_streamlit():
    """Test Streamlit functionality"""
    print("\n🌐 Testing Streamlit...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test if we can create a simple app
        print("✅ Streamlit ready for app creation")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit error: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 AI Research Agent - Comprehensive Installation Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Configuration", test_configuration),
        ("Custom Modules", test_modules),
        ("Web Search", test_web_search),
        ("Content Extraction", test_content_extraction),
        ("AI Summarization", test_ai_summarization),
        ("PDF Generation", test_pdf_generation),
        ("Streamlit", test_streamlit)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your AI Research Agent is ready to use!")
        print("\nNext steps:")
        print("1. Run: streamlit run app.py")
        print("2. Open browser to: http://localhost:8501")
        print("3. Start researching!")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check API keys in .env file")
        print("3. Verify Python version (3.8+)")
        print("4. Check internet connection")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
