#!/usr/bin/env python3
"""
Setup guide and tester for Google Gemini API
"""

import os
import sys
from dotenv import load_dotenv

print("🔮 Google Gemini API Setup Guide")
print("=" * 50)

print("""
📋 HOW TO GET FREE GEMINI API KEY:

1. 🌐 Go to: https://makersuite.google.com/app/apikey
2. 🔑 Sign in with your Google account
3. ➕ Click "Create API key"
4. 📋 Copy the generated API key
5. ✏️  Replace 'your_gemini_api_key_here' in .env file

💰 BENEFITS:
• ✅ FREE tier with generous quota
• ⚡ Fast response times
• 🧠 Excellent summarization quality
• 🔄 No credit card required
""")

# Check current status
load_dotenv()
current_key = os.getenv('GEMINI_API_KEY')

if current_key and not current_key.endswith('_here'):
    print(f"✅ GEMINI API KEY CONFIGURED: {current_key[:20]}...")
    
    # Test the API
    print("\n🧪 Testing Gemini API...")
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from modules.ai_summarizer import AISummarizer
        
        summarizer = AISummarizer()
        test_content = "Artificial intelligence is transforming how we work and live. AI technologies like machine learning and neural networks are being used in healthcare, finance, and transportation."
        
        result = summarizer.summarize_content(test_content, "AI transformation")
        
        if result.get('success') and result.get('provider') == 'Gemini':
            print("🎉 SUCCESS: Gemini API is working!")
            print(f"📝 Test summary: {result.get('summary', '')[:100]}...")
        else:
            print(f"⚠️ Gemini test failed, using: {result.get('provider', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        
else:
    print("❌ GEMINI API KEY NOT CONFIGURED")
    print("\n📝 To add your API key:")
    print("1. Open .env file in this directory")
    print("2. Find: GEMINI_API_KEY=your_gemini_api_key_here")
    print("3. Replace with: GEMINI_API_KEY=your_actual_api_key")
    print("4. Save the file and restart the application")

print("\n" + "=" * 50)
print("🎯 Once configured, Gemini will provide FREE AI summaries!")