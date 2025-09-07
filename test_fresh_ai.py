#!/usr/bin/env python3
"""
Fresh test of AI summarization with different content to avoid cache
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from modules.ai_summarizer import AISummarizer
    from config import Config
    
    print("🧪 Testing Enhanced AI Summary Generation...")
    print("=" * 60)
    
    # Test with completely different content to avoid cache
    test_content = """
    Quantum computing represents a revolutionary paradigm shift in computational power and capabilities. 
    Unlike classical computers that use bits (0s and 1s), quantum computers leverage quantum bits or 
    qubits that can exist in multiple states simultaneously through superposition. Major tech companies 
    including IBM, Google, and Microsoft are investing billions in quantum research. Google's quantum 
    computer achieved quantum supremacy by solving a specific problem faster than the world's most 
    powerful supercomputers. The potential applications include cryptography, drug discovery, financial 
    modeling, and climate simulation. However, quantum computers are still in early stages and face 
    challenges like quantum decoherence and error correction. The race for practical quantum advantage 
    continues with new breakthroughs emerging regularly.
    """
    
    test_query = "quantum computing breakthroughs and applications"
    
    print("🤖 Testing AI-powered summarization...")
    summarizer = AISummarizer()
    
    print(f"Available AI providers: {list(summarizer.ai_providers.keys())}")
    print(f"Content length: {len(test_content)} characters")
    print(f"Query: '{test_query}'")
    print()
    
    # Test summarize_content with fresh content
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
    
    # Check if we got a real AI summary or fallback
    if result.get('provider') in ['Perplexity', 'Anthropic', 'OpenAI']:
        print("🎉 SUCCESS: AI-powered summary generated!")
    elif result.get('provider') == 'Fallback':
        print("⚠️  FALLBACK: Using basic text analysis (AI APIs may have issues)")
    else:
        print("❓ UNKNOWN: Unexpected provider type")
    
    print("\n" + "=" * 60)
    print("🎯 Fresh AI Summary Test Complete!")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()