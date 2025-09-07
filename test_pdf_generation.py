#!/usr/bin/env python3
"""
Test PDF generation functionality
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_pdf_generation():
    """Test PDF generation with sample data"""
    print("🧪 Testing PDF Generation...")
    print("=" * 50)
    
    try:
        from utils.pdf_generator import PDFGenerator
        
        # Create sample research results
        sample_results = {
            'query': 'Artificial Intelligence in Healthcare',
            'timestamp': '2025-01-07T19:46:24.015486',
            'mode': 'Enhanced',
            'summary': {
                'success': True,
                'summary': 'Artificial intelligence is revolutionizing healthcare through advanced diagnostic tools, personalized treatment plans, and improved patient outcomes. Recent developments show significant progress in medical imaging, drug discovery, and clinical decision support systems.',
                'provider': 'Enhanced Fallback'
            },
            'search_results': [
                {
                    'title': 'AI Transforming Medical Diagnostics',
                    'url': 'https://example.com/ai-diagnostics',
                    'snippet': 'Latest advancements in AI-powered medical diagnostic tools are improving accuracy and speed of disease detection.',
                    'domain': 'example.com',
                    'source': 'Web Search'
                },
                {
                    'title': 'Machine Learning in Drug Discovery',
                    'url': 'https://research.com/ml-drugs',
                    'snippet': 'Machine learning algorithms are accelerating drug discovery processes, reducing time and costs significantly.',
                    'domain': 'research.com',
                    'source': 'Academic'
                }
            ],
            'extracted_content': [
                {
                    'title': 'AI in Healthcare: Current Applications',
                    'text': 'Artificial intelligence has found numerous applications in healthcare, from diagnostic imaging to treatment planning.',
                    'url': 'https://medical.com/ai-healthcare',
                    'domain': 'medical.com',
                    'word_count': 250
                }
            ],
            'summaries': {
                'executive_summary': 'AI technologies are transforming healthcare delivery through enhanced diagnostics, personalized medicine, and improved operational efficiency. Current applications span medical imaging, drug discovery, and clinical decision support.',
                'key_findings': [
                    'AI diagnostic tools achieve 95% accuracy in medical imaging',
                    'Machine learning reduces drug discovery time by 40%',
                    'Clinical decision support systems improve patient outcomes by 25%',
                    'AI-powered telemedicine platforms increase access to care'
                ],
                'detailed_analysis': 'The integration of artificial intelligence in healthcare represents a paradigm shift in medical practice. Advanced algorithms are enhancing diagnostic capabilities, enabling personalized treatment approaches, and streamlining clinical workflows.',
                'trend_analysis': {
                    'emerging_trends': [
                        'Generative AI for medical documentation',
                        'Federated learning for patient privacy',
                        'AI-powered robotic surgery'
                    ],
                    'research_gaps': [
                        'AI bias in diverse populations',
                        'Integration with existing healthcare systems'
                    ],
                    'future_directions': [
                        'Personalized AI therapy recommendations',
                        'Real-time health monitoring systems'
                    ]
                },
                'source_analysis': {
                    'total_sources': 2,
                    'unique_domains': 2,
                    'diversity_score': 1.0,
                    'source_quality': 'High quality sources'
                },
                'citations': [
                    {
                        'id': 1,
                        'apa_format': 'Medical Research Institute. (2024). AI in Healthcare Applications. Medical.com. Retrieved from https://medical.com/ai-healthcare'
                    }
                ]
            }
        }
        
        print("📋 Sample data created")
        print(f"Query: {sample_results['query']}")
        print(f"Sources: {len(sample_results['search_results'])}")
        
        # Test PDF generation
        pdf_generator = PDFGenerator()
        
        print("\n🔧 Testing generate_pdf method...")
        pdf_bytes = pdf_generator.generate_pdf(sample_results)
        
        if pdf_bytes and len(pdf_bytes) > 1000:  # PDF should be at least 1KB
            print(f"✅ SUCCESS: PDF generated successfully!")
            print(f"📊 PDF size: {len(pdf_bytes):,} bytes")
            
            # Save test PDF
            with open('test_research_report.pdf', 'wb') as f:
                f.write(pdf_bytes)
            print("💾 Test PDF saved as 'test_research_report.pdf'")
            
            return True
        else:
            print("❌ FAILED: PDF generation returned invalid data")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_integration():
    """Test how PDF generation works with Streamlit download button"""
    print("\n🌐 Testing Streamlit Integration...")
    
    try:
        # Simulate what happens in the app
        from utils.pdf_generator import PDFGenerator
        
        sample_results = {
            'query': 'Test Query',
            'summary': {
                'success': True,
                'summary': 'Test summary content.',
                'provider': 'Test'
            },
            'search_results': []
        }
        
        pdf_gen = PDFGenerator()
        pdf_content = pdf_gen.generate_pdf(sample_results)
        
        if isinstance(pdf_content, bytes) and len(pdf_content) > 0:
            print("✅ SUCCESS: PDF ready for Streamlit download button")
            print(f"📊 Content type: {type(pdf_content).__name__}")
            print(f"📊 Content size: {len(pdf_content):,} bytes")
            return True
        else:
            print(f"❌ FAILED: Invalid PDF content type: {type(pdf_content)}")
            return False
            
    except Exception as e:
        print(f"❌ Streamlit integration test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PDF Generation Test Suite")
    print("=" * 50)
    
    # Run tests
    test1_result = test_pdf_generation()
    test2_result = test_streamlit_integration()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"PDF Generation: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Streamlit Integration: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 ALL TESTS PASSED - PDF generation is working!")
    else:
        print("\n⚠️  SOME TESTS FAILED - Check errors above")
    
    print("\n💡 TIP: If tests pass but PDF still doesn't work in the app,")
    print("check the safe_api_call function in app_working.py")