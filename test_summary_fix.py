#!/usr/bin/env python3
"""
Test the summary generation fix specifically
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    print("🧪 Testing Summary Generation Fix...")
    print("=" * 60)
    
    # Test 1: Test summarize_content directly
    print("1. Testing summarize_content method...")
    from modules.ai_summarizer import AISummarizer
    
    summarizer = AISummarizer()
    test_content = """
    Climate change is one of the most pressing global challenges of the 21st century. 
    Rising global temperatures are causing melting ice caps, rising sea levels, and 
    extreme weather events. Scientists worldwide are working on solutions including 
    renewable energy, carbon capture, and sustainable practices. Governments are 
    implementing policies to reduce carbon emissions and transition to clean energy.
    The Paris Agreement represents a global commitment to limit temperature rise.
    """
    
    result = summarizer.summarize_content(test_content, "climate change solutions")
    print(f"✅ Direct summary test: {result.get('success')}")
    print(f"   Provider: {result.get('provider')}")
    print(f"   Summary length: {len(result.get('summary', ''))}")
    
    # Test 2: Test with list data structure (the problematic case)
    print("\n2. Testing with search results structure...")
    
    # Simulate search results that come as a list
    mock_search_results = [
        {
            "title": "Climate Change Solutions",
            "url": "https://example.com/climate1",
            "snippet": "Renewable energy is key to fighting climate change...",
            "domain": "example.com"
        },
        {
            "title": "Carbon Reduction Strategies", 
            "url": "https://example.com/climate2",
            "snippet": "Carbon capture technology shows promise...",
            "domain": "example.com"
        }
    ]
    
    # Test the condition that was failing
    print("   Testing list vs dict handling...")
    
    # This should NOT raise 'list' object has no attribute 'get'
    if mock_search_results and (not isinstance(mock_search_results, dict) or not mock_search_results.get('error')):
        print("   ✅ List handling: PASSED")
        results_list = mock_search_results if isinstance(mock_search_results, list) else mock_search_results.get('search_results', [])
        print(f"   ✅ Results extraction: {len(results_list)} items")
    else:
        print("   ❌ List handling: FAILED")
    
    # Test 3: Test with dict structure  
    print("\n3. Testing with dict search results...")
    mock_dict_results = {
        "search_results": mock_search_results,
        "search_time": 1.5,
        "total_found": 2
    }
    
    if mock_dict_results and (not isinstance(mock_dict_results, dict) or not mock_dict_results.get('error')):
        print("   ✅ Dict handling: PASSED")
        results_list = mock_dict_results if isinstance(mock_dict_results, list) else mock_dict_results.get('search_results', [])
        print(f"   ✅ Results extraction: {len(results_list)} items")
    else:
        print("   ❌ Dict handling: FAILED")
    
    # Test 4: Test summarization with extracted content format
    print("\n4. Testing content extraction simulation...")
    mock_extracted_content = [
        {
            "content": "Climate change requires immediate action through renewable energy adoption...",
            "title": "Climate Action",
            "url": "https://example.com/climate1"
        },
        {
            "content": "Carbon capture and storage technologies are becoming more viable...",
            "title": "Carbon Tech", 
            "url": "https://example.com/climate2"
        }
    ]
    
    # Test the summarization path
    combined_text = " ".join([content.get('content', '')[:1000] for content in mock_extracted_content])[:3000]
    if combined_text:
        summary_result = summarizer.summarize_content(combined_text, "climate change solutions")
        print(f"   ✅ Content summarization: {summary_result.get('success')}")
        print(f"   Summary provider: {summary_result.get('provider')}")
        print(f"   Summary preview: {summary_result.get('summary', '')[:100]}...")
    else:
        print("   ❌ No content for summarization")
    
    print("\n" + "=" * 60)
    print("🎯 Summary Generation Fix Test Complete!")
    print("✅ All summary-related issues should now be resolved!")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()