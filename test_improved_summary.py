#!/usr/bin/env python3
"""
Test the improved summary generation functionality
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from modules.ai_summarizer import AISummarizer
    
    print("🚀 Testing IMPROVED Summary Generation...")
    print("=" * 60)
    
    # Test with completely new content to avoid cache
    test_content = """
    Renewable energy technologies are experiencing unprecedented growth and innovation worldwide. 
    Solar panel efficiency has improved dramatically, with new perovskite tandem cells achieving 
    over 30% efficiency in laboratory settings. Wind energy capacity has doubled in the past 
    five years, with offshore wind farms becoming increasingly cost-competitive. Energy storage 
    solutions, particularly lithium-ion batteries, have seen costs plummet by 85% since 2010. 
    Smart grid technologies are enabling better integration of renewable sources, reducing waste 
    and improving reliability. Governments globally are investing trillions in clean energy 
    infrastructure as part of climate change mitigation efforts. The renewable energy sector 
    now employs over 13 million people worldwide and is becoming the fastest-growing job sector. 
    However, challenges remain including intermittency issues, grid modernization needs, and 
    the requirement for massive mineral extraction for battery production. Despite these 
    challenges, the transition to renewable energy is accelerating rapidly with fossil fuel 
    companies increasingly investing in clean energy portfolios.
    """
    
    test_query = "renewable energy technologies and innovations 2024"
    
    print("📝 Testing with content about renewable energy...")
    summarizer = AISummarizer()
    
    print(f"Available AI providers: {list(summarizer.ai_providers.keys())}")
    print(f"Content length: {len(test_content)} characters")
    print(f"Query: '{test_query}'")
    print()
    
    # Clear any potential cache by using different content
    result = summarizer.summarize_content(test_content, test_query)
    
    print("📊 RESULTS:")
    print(f"✅ Success: {result.get('success')}")
    print(f"🤖 Provider: {result.get('provider')}")
    print(f"⏰ Timestamp: {result.get('timestamp')}")
    
    if result.get('error'):
        print(f"❌ Error: {result.get('error')}")
    
    summary = result.get('summary', '')
    print(f"\n📝 Generated Summary ({len(summary)} chars):")
    print("=" * 60)
    print(summary)
    print("=" * 60)
    
    # Analyze summary quality
    if len(summary) > 500:
        print("✅ EXCELLENT: Comprehensive summary generated!")
    elif len(summary) > 200:
        print("✅ GOOD: Detailed summary generated!")
    else:
        print("⚠️  BASIC: Short summary generated")
    
    # Check for key elements
    summary_lower = summary.lower()
    quality_indicators = []
    
    if "executive summary" in summary_lower:
        quality_indicators.append("Executive Summary")
    if "key findings" in summary_lower:
        quality_indicators.append("Key Findings")  
    if "technical analysis" in summary_lower:
        quality_indicators.append("Technical Analysis")
    if "methodology" in summary_lower:
        quality_indicators.append("Methodology")
    
    if quality_indicators:
        print(f"📈 Quality Features: {', '.join(quality_indicators)}")
    
    print("\n" + "=" * 60)
    print("🎯 Improved Summary Test Complete!")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()