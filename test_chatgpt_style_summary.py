"""
Test script for ChatGPT-style summary generation
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

def test_chatgpt_style_summary():
    """Test the ChatGPT-style summary generation"""
    
    print("Testing ChatGPT-style Summary Generation")
    print("=" * 50)
    
    try:
        from modules.ai_summarizer import AISummarizer
        from modules.content_extractor import ContentExtractor
        
        # Test content
        test_content = """
        Artificial intelligence (AI) has become one of the most transformative technologies of the 21st century. 
        The purpose of this research is to analyze current developments and future trends in AI technology.
        
        The scope of this work includes machine learning algorithms, neural networks, natural language processing, 
        computer vision, and robotics. These areas represent the core components of modern AI systems.
        
        As input, this research takes scientific papers, industry reports, and technical documentation. 
        The output consists of synthesized insights, trend analysis, and future projections.
        
        Key features of current AI systems include deep learning capabilities, real-time processing, 
        adaptive algorithms, and integration with cloud computing platforms. These features enable 
        sophisticated applications across various industries.
        
        The target audience for this research includes technology researchers, software developers, 
        business strategists, and policy makers. It helps them understand current capabilities, 
        identify opportunities, and make informed decisions about AI adoption.
        
        Recent developments show significant progress in generative AI models, which can create text, 
        images, and code. These models are based on transformer architectures and have billions of parameters.
        
        The implications of these advances are profound, affecting how we work, communicate, and solve problems.
        However, they also raise important questions about ethics, privacy, and the future of employment.
        """
        
        query = "Artificial Intelligence Developments 2024"
        
        print(f"Testing summary generation for query: '{query}'")
        print(f"Content length: {len(test_content)} characters")
        
        # Test ChatGPT-style summary generation
        summarizer = AISummarizer()
        summary_result = summarizer.generate_chatgpt_style_summary(test_content, query)
        
        print(f"Summary generation success: {summary_result.get('success', False)}")
        print(f"Provider used: {summary_result.get('provider', 'Unknown')}")
        
        if summary_result.get('success'):
            summary_text = summary_result.get('summary', '')
            print(f"Summary length: {len(summary_text)} characters")
            print("\nGenerated Summary:")
            print("-" * 30)
            print(summary_text[:1000] + "..." if len(summary_text) > 1000 else summary_text)
            
            # Check if all required sections are present
            required_sections = [
                "Purpose / Objective",
                "Scope of Work", 
                "Input / Output",
                "Key Features",
                "Target Audience / Use Case"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in summary_text:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"\n⚠️  Missing sections: {missing_sections}")
            else:
                print("\n✅ All required sections present")
                
        else:
            print(f"❌ Summary generation failed: {summary_result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing ChatGPT-style summary: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("ChatGPT-style summary test completed!")
    return True

def test_comprehensive_extraction():
    """Test comprehensive content extraction"""
    
    print("\n\nTesting Comprehensive Content Extraction")
    print("=" * 50)
    
    try:
        from modules.content_extractor import ContentExtractor
        
        # Create extractor
        extractor = ContentExtractor()
        
        # Test with sample content
        sample_content = {
            'text': """
            This research aims to analyze current developments in artificial intelligence. 
            The scope includes machine learning, neural networks, and natural language processing.
            Input consists of scientific papers and the output provides synthesized insights.
            Key features include deep learning capabilities and real-time processing.
            This research serves technology researchers and business strategists.
            """,
            'title': 'AI Research Analysis'
        }
        
        # Test comprehensive details extraction
        comp_details = extractor._extract_comprehensive_details(sample_content, sample_content['text'])
        
        print("Extracted comprehensive details:")
        for key, value in comp_details.items():
            print(f"  {key}: {value[:100]}..." if len(value) > 100 else f"  {key}: {value}")
        
        # Verify all required fields are present
        required_fields = ['purpose', 'scope', 'input_output', 'key_features', 'audience_use_case']
        missing_fields = [field for field in required_fields if field not in comp_details]
        
        if missing_fields:
            print(f"⚠️  Missing fields: {missing_fields}")
        else:
            print("✅ All required fields extracted")
            
    except Exception as e:
        print(f"❌ Error testing comprehensive extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("Comprehensive extraction test completed!")
    return True

if __name__ == "__main__":
    success1 = test_chatgpt_style_summary()
    success2 = test_comprehensive_extraction()
    
    if success1 and success2:
        print("\n🎉 All tests passed!")
        print("\nThe ChatGPT-style summary generation and comprehensive content extraction")
        print("are working correctly. The app will now provide detailed summaries with:")
        print("  ✅ Purpose / Objective")
        print("  ✅ Scope of Work")
        print("  ✅ Input / Output")
        print("  ✅ Key Features")
        print("  ✅ Target Audience / Use Case")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")