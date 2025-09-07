"""
Test script for the streamlined deployment version
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from app_streamlined_deployment import main
        print("✅ Successfully imported app_streamlined_deployment")
        return True
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_modules():
    """Test that core modules can be imported"""
    modules_to_test = [
        "modules.web_search",
        "modules.content_extractor", 
        "modules.ai_summarizer",
        "utils.pdf_generator",
        "config"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ Successfully imported {module}")
        except ImportError as e:
            print(f"❌ Import Error for {module}: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error for {module}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Testing streamlined deployment version...\n")
    
    if test_imports() and test_modules():
        print("\n✅ All tests passed! The streamlined deployment version is ready.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")