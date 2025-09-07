#!/usr/bin/env python3
"""
Comprehensive test of multiple AI API providers for summary generation
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from modules.ai_summarizer import AISummarizer
    
    print("🧪 Testing Multiple AI Summary Providers")
    print("=" * 80)
    
    # Test with comprehensive content to ensure good summaries
    test_content = """
    Climate change represents one of the most pressing challenges facing humanity in the 21st century. 
    Recent scientific research has demonstrated that global temperatures have risen by approximately 1.1 
    degrees Celsius since pre-industrial times, with the rate of warming accelerating in recent decades. 
    
    The primary driver of this warming is the increased concentration of greenhouse gases in the atmosphere, 
    particularly carbon dioxide from fossil fuel combustion. Current atmospheric CO2 levels have reached 
    over 420 parts per million, the highest in over 3 million years. This has led to observable changes 
    including rising sea levels, melting polar ice caps, more frequent extreme weather events, and shifts 
    in precipitation patterns globally.
    
    The impacts of climate change are not equally distributed. Developing nations, despite contributing 
    least to historical emissions, face the greatest vulnerabilities. Island nations confront existential 
    threats from sea level rise, while sub-Saharan Africa experiences increased drought and desertification. 
    Arctic communities witness dramatic changes to their traditional ways of life as ice patterns shift.
    
    International efforts to address climate change have evolved through multiple frameworks. The 2015 
    Paris Agreement established a goal of limiting global warming to well below 2°C above pre-industrial 
    levels, with efforts to limit it to 1.5°C. However, current national commitments fall short of these 
    targets, with projected warming of 2.7-3.1°C by 2100 under current policies.
    
    Technological solutions offer pathways for mitigation and adaptation. Renewable energy costs have 
    plummeted, with solar and wind becoming the cheapest sources of electricity in many regions. Energy 
    storage technologies, electric vehicles, and green hydrogen are scaling rapidly. Carbon capture and 
    storage technologies, while promising, remain expensive and limited in deployment.
    
    The transition to a low-carbon economy presents both challenges and opportunities. Fossil fuel 
    dependent regions face economic disruption, while new industries create employment in clean energy, 
    sustainable agriculture, and environmental restoration. Financial markets are increasingly pricing 
    climate risks, with sustainable investing reaching record levels.
    """
    
    test_query = "climate change impacts and solutions"
    
    print("🤖 Testing AI-powered summarization with comprehensive content...")
    summarizer = AISummarizer()
    
    print(f"Available AI providers: {list(summarizer.ai_providers.keys())}")
    print(f"Content length: {len(test_content)} characters")
    print(f"Query: '{test_query}'")
    print()
    
    # Test summarize_content method
    result = summarizer.summarize_content(test_content, test_query)
    
    print("📊 SUMMARY GENERATION RESULTS:")
    print("=" * 80)
    print(f"✅ Success: {result.get('success')}")
    print(f"🤖 Provider: {result.get('provider')}")
    print(f"⏰ Timestamp: {result.get('timestamp')}")
    
    if result.get('error'):
        print(f"❌ Error: {result.get('error')}")
    
    summary = result.get('summary', '')
    print(f"\n📝 Generated Summary ({len(summary)} chars):")
    print("=" * 80)
    print(summary)
    print("=" * 80)
    
    # Analyze summary quality
    quality_score = 0
    if len(summary) > 500:
        quality_score += 30
        print("✅ EXCELLENT: Comprehensive summary generated!")
    elif len(summary) > 200:
        quality_score += 20
        print("✅ GOOD: Detailed summary generated!")
    else:
        quality_score += 10
        print("⚠️  BASIC: Short summary generated")
    
    # Check for quality indicators
    summary_lower = summary.lower()
    quality_indicators = []
    
    if any(term in summary_lower for term in ['climate change', 'greenhouse', 'global warming']):
        quality_indicators.append("Topic Coverage")
        quality_score += 20
    
    if any(term in summary_lower for term in ['research', 'study', 'data', 'evidence']):
        quality_indicators.append("Evidence-Based")
        quality_score += 15
    
    if any(term in summary_lower for term in ['impact', 'effect', 'consequence']):
        quality_indicators.append("Impact Analysis")
        quality_score += 10
    
    if any(term in summary_lower for term in ['solution', 'technology', 'renewable']):
        quality_indicators.append("Solutions Focus")
        quality_score += 15
    
    if len(summary.split('.')) >= 3:
        quality_indicators.append("Structured Content")
        quality_score += 10
    
    print(f"\n📈 QUALITY ANALYSIS:")
    print(f"Overall Score: {quality_score}/100")
    if quality_indicators:
        print(f"Quality Features: {', '.join(quality_indicators)}")
    
    # Provider-specific feedback
    provider = result.get('provider', 'Unknown')
    if provider == 'Gemini':
        print("🎉 SUCCESS: Using Google Gemini (Free AI)")
    elif provider == 'Hugging Face':
        print("🎉 SUCCESS: Using Hugging Face (Free AI)")
    elif provider == 'Cohere':
        print("🎉 SUCCESS: Using Cohere (Free AI)")
    elif provider == 'Together AI':
        print("🎉 SUCCESS: Using Together AI (Free AI)")
    elif provider == 'Ollama (Local)':
        print("🎉 SUCCESS: Using Local Ollama AI")
    elif provider in ['Perplexity', 'Anthropic', 'OpenAI']:
        print(f"🎉 SUCCESS: Using {provider} AI")
    elif provider == 'Enhanced Fallback':
        print("⚡ FALLBACK: Using Enhanced Text Analysis (No AI API needed)")
    else:
        print(f"❓ UNKNOWN: Using {provider}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if quality_score >= 80:
        print("🌟 Excellent summary quality! Your AI setup is working perfectly.")
    elif quality_score >= 60:
        print("👍 Good summary quality! Consider adding more API keys for backup.")
    elif quality_score >= 40:
        print("⚠️  Fair quality. Configure additional AI API keys for better results.")
    else:
        print("🔧 Limited quality. Please set up AI API keys for enhanced summaries.")
    
    print("\n" + "=" * 80)
    print("🎯 Multiple AI Provider Test Complete!")
    print("\n📋 NEXT STEPS:")
    if provider == 'Enhanced Fallback':
        print("1. Set up FREE API keys using: python setup_multiple_apis.py")
        print("2. Get Google Gemini key: https://makersuite.google.com/app/apikey")
        print("3. Get Hugging Face key: https://huggingface.co/settings/tokens")
    else:
        print("1. ✅ Your AI summarization is working!")
        print("2. Consider adding backup API keys for reliability")
        print("3. Monitor API usage and quotas")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()