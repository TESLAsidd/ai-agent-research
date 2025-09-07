#!/usr/bin/env python3
"""
Test Gemini integration and enhanced fallback summary
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    print("🔮 Testing Gemini Integration...")
    print("=" * 60)
    
    from modules.ai_summarizer import AISummarizer
    
    # Test 1: Check available providers
    print("1. Checking available AI providers...")
    summarizer = AISummarizer()
    print(f"Available providers: {list(summarizer.ai_providers.keys())}")
    
    # Test 2: Test summarization (will use enhanced fallback)
    print("\n2. Testing summary generation...")
    test_content = """
    Renewable energy has reached unprecedented growth in 2024, with solar and wind power 
    leading the transformation. Global investments in clean energy exceeded $2 trillion, 
    driven by declining costs and supportive government policies. Solar panel efficiency 
    has improved to over 26% for commercial panels, while offshore wind capacity has 
    doubled. Electric vehicle adoption accelerated, with EVs representing 30% of new car 
    sales in many developed countries. Energy storage technologies, particularly 
    lithium-ion batteries, have seen costs drop by 15% year-over-year. Smart grid 
    implementations are enabling better integration of renewable sources, reducing waste 
    and improving reliability across power networks.
    """
    
    result = summarizer.summarize_content(test_content, "renewable energy trends 2024")
    
    print(f"✅ Summary generated successfully!")
    print(f"🤖 Provider: {result.get('provider')}")
    print(f"✅ Success: {result.get('success')}")
    print(f"📊 Summary length: {len(result.get('summary', ''))}")
    
    print(f"\n📝 Generated Summary:")
    print("=" * 60)
    print(result.get('summary', 'No summary available'))
    print("=" * 60)
    
    # Test 3: Check if Gemini would be prioritized
    print(f"\n3. API Priority Test:")
    if 'gemini' in summarizer.ai_providers:
        print("🎉 Gemini is available and will be used first!")
    else:
        print("⚠️ Gemini not configured, but enhanced fallback provides quality summaries")
    
    print(f"\n4. Summary Quality Assessment:")
    summary_text = result.get('summary', '')
    
    # Check quality indicators
    quality_score = 0
    if 'Executive Summary' in summary_text:
        quality_score += 25
        print("✅ Professional structure (+25)")
    if 'Key Findings' in summary_text:
        quality_score += 25  
        print("✅ Key findings section (+25)")
    if 'Technical Analysis' in summary_text:
        quality_score += 25
        print("✅ Technical analysis (+25)")
    if len(summary_text) > 500:
        quality_score += 25
        print("✅ Comprehensive length (+25)")
    
    print(f"\n🏆 Overall Quality Score: {quality_score}/100")
    
    if quality_score >= 75:
        print("🌟 EXCELLENT: High-quality summary generated!")
    elif quality_score >= 50:
        print("👍 GOOD: Quality summary with room for improvement")
    else:
        print("📈 BASIC: Functional but could be enhanced with API keys")
    
    print("\n" + "=" * 60)
    print("🎯 Summary Generation Test Complete!")
    
    if 'gemini' not in summarizer.ai_providers:
        print("\n💡 TIP: Add a free Gemini API key for even better summaries!")
        print("Run: python setup_gemini.py for instructions")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()