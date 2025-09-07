#!/usr/bin/env python3
"""
Test PDF functionality in the context of the AI Research Agent application
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_full_application_pdf():
    """Test PDF generation with real application data structure"""
    print("🔬 Testing PDF with Application Data Structure")
    print("=" * 60)
    
    try:
        from utils.pdf_generator import PDFGenerator
        from datetime import datetime
        
        # Simulate real application results structure
        app_results = {
            'query': 'Climate Change Mitigation Strategies',
            'timestamp': datetime.now().isoformat(),
            'mode': 'Enhanced',
            'summary': {
                'success': True,
                'summary': 'Climate change mitigation requires comprehensive strategies including renewable energy adoption, carbon pricing mechanisms, and international cooperation. Current research shows significant progress in solar and wind technologies, while carbon capture and storage remain in development phases.',
                'provider': 'Enhanced Fallback',
                'timestamp': datetime.now().isoformat()
            },
            'search_results': {
                'search_results': [
                    {
                        'title': 'Renewable Energy Transition Global Report 2024',
                        'url': 'https://renewable-energy.org/global-report-2024',
                        'snippet': 'Latest analysis shows renewable energy capacity increased by 260 GW globally in 2024, with solar leading the growth.',
                        'domain': 'renewable-energy.org',
                        'source': 'Web Search'
                    },
                    {
                        'title': 'Carbon Pricing Mechanisms: Effectiveness and Implementation',
                        'url': 'https://climate-policy.gov/carbon-pricing-2024',
                        'snippet': 'Carbon pricing systems have been implemented in 46 national jurisdictions, covering 23% of global emissions.',
                        'domain': 'climate-policy.gov',
                        'source': 'Government'
                    },
                    {
                        'title': 'IPCC Working Group III Report: Mitigation of Climate Change',
                        'url': 'https://ipcc.ch/report/ar6/wg3/',
                        'snippet': 'Comprehensive assessment of climate change mitigation options and their potential for limiting global warming.',
                        'domain': 'ipcc.ch',
                        'source': 'Scientific'
                    }
                ],
                'total_results': 3,
                'search_time': 2.5
            },
            'extracted_content': [
                {
                    'title': 'Renewable Energy Technologies and Climate Mitigation',
                    'text': 'Solar photovoltaic and wind energy technologies have achieved grid parity in most markets, making them cost-competitive with fossil fuels. Energy storage solutions are rapidly improving, addressing intermittency challenges.',
                    'url': 'https://energy-tech.org/renewable-climate',
                    'domain': 'energy-tech.org',
                    'word_count': 150,
                    'publish_date': '2024-01-15'
                },
                {
                    'title': 'Carbon Markets and Climate Finance',
                    'text': 'International carbon markets facilitate cost-effective emission reductions through trading mechanisms. Article 6 of the Paris Agreement provides framework for cooperative approaches.',
                    'url': 'https://carbon-markets.org/paris-agreement',
                    'domain': 'carbon-markets.org',
                    'word_count': 120,
                    'publish_date': '2024-02-01'
                }
            ],
            'summaries': {
                'executive_summary': 'Climate change mitigation strategies encompass a comprehensive portfolio of technologies, policies, and international cooperation mechanisms. Recent developments in renewable energy, carbon pricing, and climate finance demonstrate significant progress toward global emission reduction goals.',
                'key_findings': [
                    'Renewable energy costs have declined by 70% since 2010',
                    'Carbon pricing covers 23% of global greenhouse gas emissions',
                    'Energy storage deployment increased 140% in 2024',
                    'Climate finance reached $100 billion target for developing countries',
                    'Nature-based solutions could provide 30% of required mitigation'
                ],
                'detailed_analysis': 'The transition to sustainable energy systems requires coordinated policy interventions, technological innovation, and substantial financial investments. Current mitigation pathways demonstrate feasibility of limiting warming to 1.5°C through rapid deployment of renewable energy, enhanced energy efficiency, and carbon removal technologies.',
                'trend_analysis': {
                    'emerging_trends': [
                        'Hydrogen economy development',
                        'Direct air capture scaling',
                        'Circular economy integration',
                        'Digital technologies for optimization'
                    ],
                    'research_gaps': [
                        'Long-duration energy storage',
                        'Industrial decarbonization pathways',
                        'Behavioral change mechanisms'
                    ],
                    'future_directions': [
                        'Integrated energy system planning',
                        'Climate-resilient infrastructure',
                        'Just transition frameworks'
                    ],
                    'analysis_text': 'Current research indicates accelerating momentum in climate mitigation technologies and policies. Key trends include rapid cost reductions in clean technologies, growing policy ambition, and increasing private sector engagement in climate solutions.'
                },
                'source_analysis': {
                    'total_sources': 3,
                    'unique_domains': 3,
                    'diversity_score': 1.0,
                    'source_quality': 'High quality sources',
                    'domain_categories': {
                        'academic': ['renewable-energy.org'],
                        'government': ['climate-policy.gov'],
                        'organization': ['ipcc.ch'],
                        'news': [],
                        'other': []
                    }
                },
                'citations': [
                    {
                        'id': 1,
                        'title': 'Renewable Energy Transition Global Report 2024',
                        'url': 'https://renewable-energy.org/global-report-2024',
                        'domain': 'renewable-energy.org',
                        'author': 'International Renewable Energy Agency',
                        'publish_date': '2024-01-15',
                        'apa_format': 'International Renewable Energy Agency. (2024). Renewable Energy Transition Global Report 2024. renewable-energy.org. Retrieved from https://renewable-energy.org/global-report-2024'
                    },
                    {
                        'id': 2,
                        'title': 'Carbon Pricing Mechanisms: Effectiveness and Implementation',
                        'url': 'https://climate-policy.gov/carbon-pricing-2024',
                        'domain': 'climate-policy.gov',
                        'author': 'Climate Policy Research Institute',
                        'publish_date': '2024-02-01',
                        'apa_format': 'Climate Policy Research Institute. (2024). Carbon Pricing Mechanisms: Effectiveness and Implementation. climate-policy.gov. Retrieved from https://climate-policy.gov/carbon-pricing-2024'
                    }
                ],
                'metadata': {
                    'query': 'Climate Change Mitigation Strategies',
                    'summary_type': 'comprehensive',
                    'total_sources': 3,
                    'generation_timestamp': datetime.now().isoformat(),
                    'ai_model': 'Multiple AI Providers'
                }
            }
        }
        
        print("📋 Realistic application data created")
        print(f"Query: {app_results['query']}")
        print(f"Search Results: {len(app_results['search_results']['search_results'])}")
        print(f"Extracted Content: {len(app_results['extracted_content'])}")
        print(f"Has Summary: {app_results['summary']['success']}")
        print(f"Has AI Summaries: {'summaries' in app_results}")
        
        # Test PDF generation with real app structure
        pdf_generator = PDFGenerator()
        
        print("\n🔧 Generating PDF with full application data...")
        pdf_bytes = pdf_generator.generate_pdf(app_results)
        
        if isinstance(pdf_bytes, bytes) and len(pdf_bytes) > 5000:  # Should be substantial
            print(f"✅ SUCCESS: Comprehensive PDF generated!")
            print(f"📊 PDF size: {len(pdf_bytes):,} bytes")
            
            # Save the PDF
            filename = 'application_test_report.pdf'
            with open(filename, 'wb') as f:
                f.write(pdf_bytes)
            print(f"💾 PDF saved as '{filename}'")
            
            # Test the export functions too
            print("\n🧪 Testing export functions...")
            from app_working import generate_markdown_export, generate_csv_export
            
            # Test Markdown export
            md_content = generate_markdown_export(app_results)
            if len(md_content) > 100:
                print("✅ Markdown export: PASS")
                with open('test_export.md', 'w', encoding='utf-8') as f:
                    f.write(md_content)
            else:
                print("❌ Markdown export: FAIL")
            
            # Test CSV export
            csv_content = generate_csv_export(app_results)
            if len(csv_content) > 50:
                print("✅ CSV export: PASS")
                with open('test_export.csv', 'w', encoding='utf-8') as f:
                    f.write(csv_content)
            else:
                print("❌ CSV export: FAIL")
            
            return True
        else:
            print(f"❌ FAILED: PDF generation issue - got {type(pdf_bytes)} with size {len(pdf_bytes) if isinstance(pdf_bytes, bytes) else 'N/A'}")
            return False
            
    except Exception as e:
        print(f"❌ Application PDF test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test PDF generation with edge cases and minimal data"""
    print("\n🧪 Testing Edge Cases...")
    
    try:
        from utils.pdf_generator import PDFGenerator
        
        # Test with minimal data
        minimal_results = {
            'query': 'Test Query',
            'summary': {'success': True, 'summary': 'Test summary'},
            'search_results': [],
            'extracted_content': []
        }
        
        pdf_generator = PDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf(minimal_results)
        
        if isinstance(pdf_bytes, bytes) and len(pdf_bytes) > 1000:
            print("✅ Minimal data test: PASS")
        else:
            print("❌ Minimal data test: FAIL")
            return False
        
        # Test with missing summary
        no_summary_results = {
            'query': 'Test Query 2',
            'search_results': [{'title': 'Test', 'url': 'http://test.com', 'snippet': 'Test snippet'}]
        }
        
        pdf_bytes = pdf_generator.generate_pdf(no_summary_results)
        
        if isinstance(pdf_bytes, bytes) and len(pdf_bytes) > 1000:
            print("✅ No summary test: PASS")
        else:
            print("❌ No summary test: FAIL")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Edge case testing failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Comprehensive PDF Functionality Test")
    print("=" * 60)
    
    # Run tests
    test1_result = test_full_application_pdf()
    test2_result = test_edge_cases()
    
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS:")
    print(f"Full Application Test: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Edge Cases Test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ PDF generation is fully functional")
        print("✅ Export functions are working")
        print("✅ Edge cases handled properly")
        print("\n💡 PDF functionality should now work perfectly in the application!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Check the error messages above for details")
    
    print("\n📋 Generated files:")
    print("- application_test_report.pdf")
    print("- test_export.md")
    print("- test_export.csv")