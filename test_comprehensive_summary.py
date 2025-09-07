"""
Test script for comprehensive summary generation and display
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_comprehensive_summary():
    """Test comprehensive summary generation"""
    try:
        from modules.ai_summarizer import AISummarizer
        
        # Create a sample content for testing
        sample_content = """
        Artificial intelligence (AI) has become one of the most transformative technologies of the 21st century. 
        The field encompasses machine learning, deep learning, natural language processing, and computer vision. 
        Major tech companies like Google, Microsoft, and Amazon are investing heavily in AI research and development. 
        However, there are significant ethical concerns about AI, including bias in algorithms, job displacement, and privacy issues. 
        On the other hand, AI offers tremendous benefits such as improved healthcare diagnostics, enhanced productivity, and scientific breakthroughs. 
        The technology is being applied across various sectors including finance, transportation, education, and entertainment. 
        Researchers are working on developing more robust and explainable AI systems. 
        Despite challenges, the future of AI looks promising with continued advancements in quantum computing and neural networks.
        """
        
        summarizer = AISummarizer()
        
        # Test comprehensive summary generation
        summary_result = summarizer._generate_comprehensive_fallback_summary(
            sample_content, 
            "artificial intelligence", 
            3  # source count
        )
        
        print("=== COMPREHENSIVE SUMMARY TEST ===")
        print("Generated summary:")
        print("-" * 50)
        print(summary_result)
        print("-" * 50)
        
        # Check if it contains expected sections
        expected_sections = [
            "Comprehensive Research Summary",
            "Executive Summary",
            "Key Terms & Concepts",
            "Key Findings",
            "Content Analysis"
        ]
        
        missing_sections = []
        for section in expected_sections:
            if section not in summary_result:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing sections: {missing_sections}")
            return False
        else:
            print("✅ All expected sections present")
            return True
            
    except Exception as e:
        print(f"❌ Error testing comprehensive summary: {e}")
        return False

def test_keyword_extraction():
    """Test keyword extraction"""
    try:
        from modules.ai_summarizer import AISummarizer
        
        sample_content = """
        Artificial intelligence (AI) has become one of the most transformative technologies of the 21st century. 
        The field encompasses machine learning, deep learning, natural language processing, and computer vision. 
        Major tech companies like Google, Microsoft, and Amazon are investing heavily in AI research and development. 
        However, there are significant ethical concerns about AI, including bias in algorithms, job displacement, and privacy issues. 
        """
        
        summarizer = AISummarizer()
        keywords = summarizer._extract_keywords(sample_content, "artificial intelligence")
        
        print("\n=== KEYWORD EXTRACTION TEST ===")
        print(f"Extracted keywords: {keywords}")
        
        # Check if we have a reasonable number of keywords
        if len(keywords) >= 5:
            print("✅ Keyword extraction successful")
            return True
        else:
            print("❌ Insufficient keywords extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error testing keyword extraction: {e}")
        return False

if __name__ == "__main__":
    print("Testing comprehensive summary functionality...\n")
    
    summary_test = test_comprehensive_summary()
    keyword_test = test_keyword_extraction()
    
    if summary_test and keyword_test:
        print("\n✅ All tests passed! Comprehensive summary functionality is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")