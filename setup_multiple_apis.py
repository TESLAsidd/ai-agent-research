#!/usr/bin/env python3
"""
Setup guide for multiple FREE AI API providers
"""

import os
import sys
from dotenv import load_dotenv

print("🚀 Multiple AI API Setup Guide")
print("=" * 60)

print("""
🎯 MULTIPLE FREE AI PROVIDERS FOR RELIABLE SUMMARIES

We've added 5 FREE API providers to ensure summary generation always works:

1. 🔮 GOOGLE GEMINI (FREE - Generous quota)
   📋 Steps:
   • Go to: https://makersuite.google.com/app/apikey
   • Sign in with Google account
   • Click "Create API key"
   • Copy key to .env file: GEMINI_API_KEY=your_key

2. 🤗 HUGGING FACE (FREE - 1000 requests/month)
   📋 Steps:
   • Go to: https://huggingface.co/settings/tokens
   • Create account and verify email
   • Click "New token" → "Read" access
   • Copy key to .env file: HUGGINGFACE_API_KEY=your_key

3. 🧠 COHERE (FREE - 100 calls/month)
   📋 Steps:
   • Go to: https://dashboard.cohere.ai/api-keys
   • Sign up with email/Google
   • Go to API Keys section
   • Copy key to .env file: COHERE_API_KEY=your_key

4. 🚀 TOGETHER AI (FREE - $25 credit)
   📋 Steps:
   • Go to: https://api.together.xyz/settings/api-keys
   • Create account and verify
   • Create new API key
   • Copy key to .env file: TOGETHER_API_KEY=your_key

5. 🤖 OLLAMA (100% FREE - Local AI)
   📋 Steps:
   • Download: https://ollama.ai/
   • Install and run: ollama pull llama2
   • Already configured in .env: OLLAMA_ENABLED=true
""")

# Check current status
load_dotenv()

print("\n📊 CURRENT API STATUS:")
print("=" * 40)

apis = [
    ('GEMINI_API_KEY', 'Google Gemini'),
    ('HUGGINGFACE_API_KEY', 'Hugging Face'),
    ('COHERE_API_KEY', 'Cohere'),
    ('TOGETHER_API_KEY', 'Together AI'),
    ('OLLAMA_ENABLED', 'Ollama (Local)')
]

working_count = 0
for key, name in apis:
    value = os.getenv(key)
    if value and not value.endswith('_here') and value != 'your_key':
        if key == 'OLLAMA_ENABLED' and value == 'true':
            print(f"✅ {name}: Enabled (Local)")
            working_count += 1
        else:
            print(f"✅ {name}: Configured ({value[:20]}...)")
            working_count += 1
    else:
        print(f"❌ {name}: Not configured")

print(f"\n🎯 WORKING APIs: {working_count}/5")

if working_count == 0:
    print("\n⚠️  NO APIs CONFIGURED")
    print("Please set up at least 1 API key above for reliable summaries!")
elif working_count < 3:
    print("\n⚠️  LIMITED COVERAGE")
    print("Consider adding more APIs for better reliability!")
else:
    print("\n🎉 EXCELLENT COVERAGE!")
    print("You have multiple fallback options for reliable summaries!")

print("\n" + "=" * 60)
print("🔧 TESTING SUMMARY GENERATION...")

# Test the system
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    from modules.ai_summarizer import AISummarizer
    
    summarizer = AISummarizer()
    test_content = "Machine learning algorithms are revolutionizing data analysis across industries. Neural networks can now process complex patterns and make predictions with remarkable accuracy."
    
    result = summarizer.summarize_content(test_content, "machine learning advances")
    
    if result.get('success'):
        provider = result.get('provider', 'Unknown')
        summary = result.get('summary', '')[:100]
        print(f"🎉 SUCCESS: Summary generated using {provider}")
        print(f"📝 Preview: {summary}...")
    else:
        error = result.get('error', 'Unknown error')
        print(f"❌ FAILED: {error}")
        
except Exception as e:
    print(f"❌ Test error: {str(e)}")

print("\n" + "=" * 60)
print("🎯 Setup complete! Your summary generation now has multiple fallbacks!")