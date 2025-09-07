#!/usr/bin/env python3
"""
Debug script to test summary generation functionality
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from modules.ai_summarizer import AISummarizer
    from config import Config
    
    print("🔍 Testing Summary Generation...")
    print("=" * 50)
    
    # Test 1: Basic functionality
    print("1. Testing AISummarizer initialization...")
    summarizer = AISummarizer()
    print("✅ AISummarizer initialized successfully")
    
    # Test 2: Config check
    print("\n2. Checking API configuration...")
    config = Config()
    print(f"OpenAI API Key configured: {'Yes' if config.OPENAI_API_KEY else 'No'}")
    print(f"Perplexity API Key configured: {'Yes' if config.PERPLEXITY_API_KEY else 'No'}")
    print(f"Anthropic API Key configured: {'Yes' if config.ANTHROPIC_API_KEY else 'No'}")
    
    # Test 3: Test summarize_content method
    print("\n3. Testing summarize_content method...")
    test_content = """
    Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century. 
    Recent breakthroughs in machine learning, particularly in deep learning and neural networks, have enabled 
    AI systems to achieve remarkable performance in various domains including natural language processing, 
    computer vision, and robotics. Companies like OpenAI, Google, and Microsoft are leading the charge in 
    developing large language models that can understand and generate human-like text. The applications of 
    AI are vast, ranging from healthcare diagnosis and drug discovery to autonomous vehicles and financial 
    trading. However, the rapid advancement of AI also raises important questions about ethics, job displacement, 
    and the need for proper regulation to ensure AI systems are safe and beneficial for humanity.
    """
    
    test_query = "artificial intelligence breakthroughs 2024"
    
    print(f"Content length: {len(test_content)} characters")
    print(f"Query: '{test_query}'")
    
    try:
        result = summarizer.summarize_content(test_content, test_query)
        print("\n✅ summarize_content method executed successfully!")
        print(f"Result type: {type(result)}")
        print(f"Success: {result.get('success', 'unknown')}")
        print(f"Provider: {result.get('provider', 'unknown')}")
        
        if result.get('success'):
            summary = result.get('summary', '')
            print(f"\n📋 Generated Summary ({len(summary)} chars):")
            print("-" * 40)
            print(summary[:300] + "..." if len(summary) > 300 else summary)
            print("-" * 40)
        else:
            print(f"❌ Summary generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error calling summarize_content: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Test with empty content
    print("\n4. Testing with empty content...")
    try:
        empty_result = summarizer.summarize_content("", test_query)
        print(f"Empty content result: {empty_result}")
    except Exception as e:
        print(f"Error with empty content: {str(e)}")
    
    # Test 5: Test summarize_research method
    print("\n5. Testing summarize_research method...")
    test_content_list = [
        {
            "title": "AI Research Paper 2024",
            "text": test_content,
            "url": "https://example.com/ai-research",
            "domain": "example.com",
            "word_count": len(test_content.split())
        }
    ]
    
    try:
        research_result = summarizer.summarize_research(test_content_list, test_query)
        print(f"✅ summarize_research method executed successfully!")
        print(f"Result keys: {list(research_result.keys())}")
        
        if research_result.get('executive_summary'):
            print(f"Executive summary length: {len(research_result['executive_summary'])}")
        
    except Exception as e:
        print(f"❌ Error calling summarize_research: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 Summary Generation Test Complete!")
    
except ImportError as e:
    print(f"❌ Import error: {str(e)}")
    print("Please check if all required modules are available.")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
    import traceback
    traceback.print_exc()