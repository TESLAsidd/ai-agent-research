#!/usr/bin/env python3
"""
API Key Validator for AI Research Agent
Tests all API keys to identify which ones are working and which need fixes
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.startswith('sk-proj-') == False:
        return {"status": "❌ INVALID", "error": "Invalid or missing API key format"}
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return {"status": "✅ WORKING", "model": "gpt-3.5-turbo"}
        
    except Exception as e:
        error_msg = str(e)
        if "invalid api key" in error_msg.lower():
            return {"status": "❌ INVALID", "error": "Invalid API key"}
        elif "quota" in error_msg.lower():
            return {"status": "⚠️ QUOTA_EXCEEDED", "error": "Quota exceeded - key valid but no credits"}
        else:
            return {"status": "❌ ERROR", "error": error_msg[:100]}

def test_google_search_api():
    """Test Google Custom Search API"""
    api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    if not api_key or not engine_id:
        return {"status": "❌ MISSING", "error": "API key or engine ID missing"}
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': engine_id,
            'q': 'test',
            'num': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return {"status": "✅ WORKING", "results": len(response.json().get('items', []))}
        elif response.status_code == 403:
            return {"status": "❌ FORBIDDEN", "error": "API key invalid or quota exceeded"}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def test_serpapi():
    """Test SerpAPI key"""
    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key:
        return {"status": "❌ MISSING", "error": "API key missing"}
    
    try:
        url = "https://serpapi.com/search"
        params = {
            'api_key': api_key,
            'engine': 'google',
            'q': 'test',
            'num': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                return {"status": "❌ INVALID", "error": data['error']}
            return {"status": "✅ WORKING", "results": len(data.get('organic_results', []))}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def test_newsapi():
    """Test NewsAPI key"""
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        return {"status": "❌ MISSING", "error": "API key missing"}
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        headers = {'X-API-Key': api_key}
        params = {'country': 'us', 'pageSize': 1}
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {"status": "✅ WORKING", "articles": data.get('totalResults', 0)}
        elif response.status_code == 401:
            return {"status": "❌ INVALID", "error": "Invalid API key"}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def test_perplexity_api():
    """Test Perplexity AI API"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key or api_key.endswith('-here'):
        return {"status": "❌ PLACEHOLDER", "error": "Using placeholder value - get real key from perplexity.ai"}
    
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 5
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return {"status": "✅ WORKING", "model": "llama-3.1-sonar-small-128k-online"}
        elif response.status_code == 401:
            return {"status": "❌ INVALID", "error": "Invalid API key"}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def test_anthropic_api():
    """Test Anthropic API"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key.endswith('-here'):
        return {"status": "❌ PLACEHOLDER", "error": "Using placeholder value - get real key from console.anthropic.com"}
    
    try:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 5,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return {"status": "✅ WORKING", "model": "claude-3-haiku-20240307"}
        elif response.status_code == 401:
            return {"status": "❌ INVALID", "error": "Invalid API key"}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def test_tavily_api():
    """Test Tavily API"""
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key or api_key.endswith('-here'):
        return {"status": "❌ PLACEHOLDER", "error": "Using placeholder value - get real key from tavily.com"}
    
    try:
        url = "https://api.tavily.com/search"
        data = {
            "api_key": api_key,
            "query": "test",
            "max_results": 1
        }
        
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return {"status": "✅ WORKING", "results": len(result.get('results', []))}
        elif response.status_code == 401:
            return {"status": "❌ INVALID", "error": "Invalid API key"}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def test_you_api():
    """Test You.com API"""
    api_key = os.getenv('YOU_API_KEY')
    if not api_key or api_key.endswith('-here'):
        return {"status": "❌ PLACEHOLDER", "error": "Using placeholder value - get real key from api.you.com"}
    
    # You.com API testing would go here
    return {"status": "⚠️ UNTESTED", "error": "API endpoint not publicly documented"}

def test_exa_api():
    """Test Exa API"""
    api_key = os.getenv('EXA_API_KEY')
    if not api_key or api_key.endswith('-here'):
        return {"status": "❌ PLACEHOLDER", "error": "Using placeholder value - get real key from exa.ai"}
    
    try:
        url = "https://api.exa.ai/search"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "query": "test",
            "numResults": 1
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return {"status": "✅ WORKING", "results": len(result.get('results', []))}
        elif response.status_code == 401:
            return {"status": "❌ INVALID", "error": "Invalid API key"}
        else:
            return {"status": "❌ ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)[:100]}

def main():
    print("🔍 AI Research Agent - API Key Validator")
    print("=" * 60)
    print(f"Testing API keys at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Core APIs
    print("\n🔧 CORE APIs (Required for basic functionality):")
    print("-" * 50)
    
    tests = [
        ("OpenAI (GPT)", test_openai_api),
        ("Google Search", test_google_search_api),
        ("SerpAPI", test_serpapi),
        ("NewsAPI", test_newsapi),
    ]
    
    working_core = 0
    total_core = len(tests)
    
    for name, test_func in tests:
        try:
            result = test_func()
            status = result["status"]
            error = result.get("error", "")
            
            print(f"{name:15} {status}")
            if error and not status.startswith("✅"):
                print(f"                → {error}")
            
            if status.startswith("✅"):
                working_core += 1
                
        except Exception as e:
            print(f"{name:15} ❌ EXCEPTION → {str(e)[:50]}")
    
    # Enhanced APIs
    print(f"\n⚡ ENHANCED APIs (For faster, better responses):")
    print("-" * 50)
    
    enhanced_tests = [
        ("Perplexity AI", test_perplexity_api),
        ("Anthropic Claude", test_anthropic_api), 
        ("Tavily Search", test_tavily_api),
        ("You.com Search", test_you_api),
        ("Exa Search", test_exa_api),
    ]
    
    working_enhanced = 0
    placeholder_count = 0
    total_enhanced = len(enhanced_tests)
    
    for name, test_func in enhanced_tests:
        try:
            result = test_func()
            status = result["status"]
            error = result.get("error", "")
            
            print(f"{name:15} {status}")
            if error and not status.startswith("✅"):
                print(f"                → {error}")
            
            if status.startswith("✅"):
                working_enhanced += 1
            elif "PLACEHOLDER" in status:
                placeholder_count += 1
                
        except Exception as e:
            print(f"{name:15} ❌ EXCEPTION → {str(e)[:50]}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    print(f"Core APIs:     {working_core}/{total_core} working")
    print(f"Enhanced APIs: {working_enhanced}/{total_enhanced} working")
    print(f"Placeholders:  {placeholder_count} APIs need real keys")
    
    if working_core >= 2:
        print("\n✅ BASIC FUNCTIONALITY: Available")
        print("   → App will work with standard search and AI")
    else:
        print("\n❌ BASIC FUNCTIONALITY: Limited")
        print("   → Need at least 2 core APIs working")
    
    if working_enhanced >= 2:
        print("✅ ENHANCED MODE: Active")
        print("   → Faster, more accurate responses available")
    elif working_enhanced >= 1:
        print("⚠️ ENHANCED MODE: Partial")
        print("   → Some enhanced features available")
    else:
        print("❌ ENHANCED MODE: Disabled")
        print("   → Add enhanced API keys for better performance")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("🔧 IMMEDIATE ACTIONS NEEDED")
    print("=" * 60)
    
    if placeholder_count > 0:
        print("1. 🔑 GET REAL API KEYS for placeholders:")
        print("   • Visit the URLs in your .env file comments")
        print("   • Sign up for free accounts")
        print("   • Replace placeholder values with real keys")
    
    if working_core < 2:
        print("2. 🆘 FIX CORE APIs (critical):")
        print("   • Check OpenAI billing/quota")
        print("   • Verify Google Search API setup")
        print("   • Test SerpAPI key validity")
    
    if working_enhanced == 0:
        print("3. ⚡ PRIORITY ENHANCED APIs (high impact):")
        print("   • Perplexity AI (real-time responses)")
        print("   • Anthropic Claude (better quality)")
        print("   • Tavily (real-time search)")
    
    print(f"\n💡 Run this test again after updating your .env file!")
    print(f"📁 .env location: {os.path.abspath('.env')}")

if __name__ == "__main__":
    main()