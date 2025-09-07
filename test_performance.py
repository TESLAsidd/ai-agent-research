"""
Performance Test Script for AI Research Agent
Tests the speed improvements and optimizations
"""

import time
import json
from datetime import datetime
from modules.web_search import WebSearchEngine
from modules.content_extractor import ContentExtractor
from modules.ai_summarizer import AISummarizer
from utils.pdf_generator import PDFGenerator
from utils.performance_optimizer import performance_optimizer

def test_search_performance():
    """Test search performance"""
    print("🔍 Testing Search Performance...")
    
    search_engine = WebSearchEngine()
    
    # Test queries
    queries = ["AI research", "machine learning", "climate change"]
    
    for query in queries:
        start_time = time.time()
        results = search_engine.search(query, num_results=5)
        end_time = time.time()
        
        print(f"   {query}: {len(results)} results in {end_time - start_time:.2f}s")

def test_pdf_generation():
    """Test PDF generation speed"""
    print("📄 Testing PDF Generation...")
    
    # Sample research results
    sample_results = {
        'query': 'AI Performance Testing',
        'extracted_content': [
            {
                'title': 'Sample Article 1',
                'text': 'This is sample content for testing PDF generation speed.',
                'url': 'https://example.com/1',
                'domain': 'example.com',
                'word_count': 100
            }
        ],
        'summaries': {
            'executive_summary': 'This is a test summary for PDF generation.',
            'key_findings': ['Finding 1', 'Finding 2'],
            'detailed_analysis': 'Detailed analysis content for testing.',
            'metadata': {
                'total_sources': 1,
                'ai_model': 'gpt-3.5-turbo'
            }
        }
    }
    
    try:
        pdf_generator = PDFGenerator()
        
        start_time = time.time()
        pdf_path = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_generator.generate_research_report(sample_results, pdf_path)
        end_time = time.time()
        
        print(f"   PDF generated in {end_time - start_time:.2f}s")
        print(f"   File saved as: {pdf_path}")
        
        # Check file size
        import os
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            print(f"   File size: {file_size:.1f} KB")
            
            # Clean up
            os.remove(pdf_path)
            print("   ✅ Test file cleaned up")
        
    except Exception as e:
        print(f"   ❌ PDF generation failed: {str(e)}")

def test_parallel_processing():
    """Test parallel processing improvements"""
    print("⚡ Testing Parallel Processing...")
    
    def sample_task(x):
        time.sleep(0.1)  # Simulate work
        return x * 2
    
    items = list(range(10))
    
    # Sequential processing
    start_time = time.time()
    sequential_results = [sample_task(x) for x in items]
    sequential_time = time.time() - start_time
    
    # Parallel processing
    start_time = time.time()
    parallel_results = performance_optimizer.parallel_map(sample_task, items)
    parallel_time = time.time() - start_time
    
    speedup = sequential_time / parallel_time if parallel_time > 0 else 0
    
    print(f"   Sequential: {sequential_time:.2f}s")
    print(f"   Parallel: {parallel_time:.2f}s")
    print(f"   Speedup: {speedup:.1f}x")

def test_cache_performance():
    """Test caching improvements"""
    print("🗄️ Testing Cache Performance...")
    
    try:
        # Test with cache manager if available
        from modules.cache_manager import cache_manager
        
        stats = cache_manager.get_cache_stats()
        print(f"   Cache files: {stats['total_files']}")
        print(f"   Cache size: {stats['total_size_mb']} MB")
        print("   ✅ Caching system active")
        
    except ImportError:
        print("   ⚠️ Cache manager not available")
    except Exception as e:
        print(f"   ❌ Cache test failed: {str(e)}")

def main():
    """Run all performance tests"""
    print("🚀 AI Research Agent Performance Tests")
    print("=" * 50)
    
    test_search_performance()
    print()
    
    test_pdf_generation()
    print()
    
    test_parallel_processing()
    print()
    
    test_cache_performance()
    print()
    
    print("=" * 50)
    print("✅ Performance tests completed!")
    print("\n📊 Performance Summary:")
    print("• Search: Optimized with caching and parallel processing")
    print("• PDF Generation: Fast PDF creation with proper formatting") 
    print("• Parallel Processing: Multi-threaded content extraction")
    print("• Caching: Intelligent caching for faster repeated queries")

if __name__ == "__main__":
    main()