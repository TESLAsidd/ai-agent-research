#!/usr/bin/env python3
"""
Test the complete research pipeline to identify the exact issues
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_complete_pipeline():
    """Test the complete research pipeline"""
    print("🔬 Testing Complete Research Pipeline...")
    print("=" * 60)
    
    try:
        # Import modules
        from modules.web_search import WebSearchEngine
        from modules.content_extractor import ContentExtractor
        from modules.ai_summarizer import AISummarizer
        from utils.pdf_generator import PDFGenerator
        
        print("✅ All modules imported successfully")
        
        # Test 1: Web Search
        print("\n1. Testing Web Search...")
        search_engine = WebSearchEngine()
        search_results = search_engine.search("artificial intelligence healthcare", 5)
        
        if search_results and len(search_results) > 0:
            print(f"✅ Search successful: {len(search_results)} results found")
            print(f"First result: {search_results[0].get('title', 'No title')[:50]}...")
        else:
            print("❌ Search failed or returned no results")
            return False
        
        # Test 2: Content Extraction (try first 2 URLs)
        print("\n2. Testing Content Extraction...")
        extractor = ContentExtractor()
        extracted_content = []
        
        for i, result in enumerate(search_results[:2]):
            try:
                content = extractor.extract_from_url(result.get('url', ''))
                if content and content.get('success'):
                    extracted_content.append(content)
                    print(f"✅ Extracted content from URL {i+1}: {len(content.get('content', ''))} chars")
                else:
                    print(f"⚠️ Failed to extract content from URL {i+1}")
            except Exception as e:
                print(f"❌ Error extracting from URL {i+1}: {str(e)}")
        
        print(f"📊 Total extracted content sources: {len(extracted_content)}")
        
        # Test 3: AI Summarization
        print("\n3. Testing AI Summarization...")
        summarizer = AISummarizer()
        
        # Combine content for summarization
        combined_text = " ".join([content.get('content', '')[:1000] for content in extracted_content])[:3000]
        
        if combined_text:
            summary = summarizer.summarize_content(combined_text, "artificial intelligence healthcare")
            
            if summary and summary.get('success'):
                print(f"✅ Summary generated successfully by {summary.get('provider', 'Unknown')}")
                print(f"📝 Summary length: {len(summary.get('summary', ''))} characters")
                print(f"📋 Summary preview: {summary.get('summary', '')[:100]}...")
            else:
                print(f"❌ Summary generation failed: {summary.get('error', 'Unknown error')}")
                return False
        else:
            # Try with search snippets
            search_text = " ".join([result.get('snippet', '') for result in search_results[:5]])[:2000]
            if search_text:
                summary = summarizer.summarize_content(search_text, "artificial intelligence healthcare")
                if summary and summary.get('success'):
                    print(f"✅ Summary generated from search snippets by {summary.get('provider', 'Unknown')}")
                else:
                    print("❌ Summary generation failed even with search snippets")
                    return False
            else:
                print("❌ No content available for summarization")
                return False
        
        # Test 4: Simulate app data structure
        print("\n4. Testing App Data Structure...")
        app_results = {
            'query': 'artificial intelligence healthcare',
            'search_results': search_results,
            'extracted_content': extracted_content,
            'summary': summary,
            'timestamp': '2025-01-07T20:12:00.000000',
            'mode': 'Standard'
        }
        
        print(f"✅ App data structure created with {len(app_results)} keys")
        
        # Test 5: PDF Generation with app data
        print("\n5. Testing PDF Generation with App Data...")
        pdf_gen = PDFGenerator()
        
        try:
            pdf_content = pdf_gen.generate_pdf(app_results)
            
            if isinstance(pdf_content, bytes) and len(pdf_content) > 1000:
                print(f"✅ PDF generated successfully: {len(pdf_content):,} bytes")
                
                # Save test PDF
                with open('test_complete_pipeline.pdf', 'wb') as f:
                    f.write(pdf_content)
                print("💾 Test PDF saved as 'test_complete_pipeline.pdf'")
                
                return True
            else:
                print(f"❌ PDF generation failed: {type(pdf_content)} - {len(pdf_content) if hasattr(pdf_content, '__len__') else 'No length'}")
                return False
                
        except Exception as e:
            print(f"❌ PDF generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test edge cases that might cause issues in the app"""
    print("\n" + "=" * 60)
    print("🧪 Testing Edge Cases...")
    
    from utils.pdf_generator import PDFGenerator
    
    # Test with minimal data (like what might happen in the app)
    minimal_results = {
        'query': 'test query',
        'search_results': [],
        'extracted_content': [],
        'summary': {'success': False, 'error': 'No content'},
        'timestamp': '2025-01-07T20:12:00.000000'
    }
    
    print("Testing PDF with minimal data...")
    pdf_gen = PDFGenerator()
    
    try:
        pdf_content = pdf_gen.generate_pdf(minimal_results)
        if isinstance(pdf_content, bytes) and len(pdf_content) > 0:
            print(f"✅ PDF generated with minimal data: {len(pdf_content):,} bytes")
        else:
            print("❌ PDF failed with minimal data")
    except Exception as e:
        print(f"❌ PDF error with minimal data: {str(e)}")
    
    # Test with search results but no summary
    search_only_results = {
        'query': 'test query',
        'search_results': [
            {'title': 'Test Article', 'url': 'https://example.com', 'snippet': 'Test snippet content here'},
            {'title': 'Another Article', 'url': 'https://example2.com', 'snippet': 'More test content'}
        ],
        'extracted_content': [],
        'summary': {'success': False},
        'timestamp': '2025-01-07T20:12:00.000000'
    }
    
    print("Testing PDF with search results but no summary...")
    try:
        pdf_content = pdf_gen.generate_pdf(search_only_results)
        if isinstance(pdf_content, bytes) and len(pdf_content) > 0:
            print(f"✅ PDF generated with search-only data: {len(pdf_content):,} bytes")
        else:
            print("❌ PDF failed with search-only data")
    except Exception as e:
        print(f"❌ PDF error with search-only data: {str(e)}")

if __name__ == "__main__":
    print("🚀 Complete Pipeline Test")
    print("=" * 60)
    
    # Run main pipeline test
    main_result = test_complete_pipeline()
    
    # Run edge case tests
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"Complete Pipeline: {'✅ PASS' if main_result else '❌ FAIL'}")
    
    if main_result:
        print("\n🎉 ALL TESTS PASSED!")
        print("The pipeline is working correctly. Issues might be:")
        print("1. User interaction flow in the Streamlit app")
        print("2. Session state management")
        print("3. Data format differences between test and live app")
        print("\n💡 Check the live app for specific error messages")
    else:
        print("\n⚠️ PIPELINE ISSUES DETECTED")
        print("Check the error messages above for specific problems")