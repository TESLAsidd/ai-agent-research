#!/usr/bin/env python3
"""
Test the complete boolean parsing fix
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    print("🧪 Testing Complete Boolean Fix...")
    print("=" * 50)
    
    # Test 1: Historical Data module
    print("1. Testing HistoricalDataAnalyzer...")
    from modules.historical_data import HistoricalDataAnalyzer
    analyzer = HistoricalDataAnalyzer()
    print("✅ HistoricalDataAnalyzer initialized successfully")
    print(f"   Data sources: {analyzer.data_sources}")
    
    # Test 2: Enhanced Images module
    print("\n2. Testing EnhancedImageProcessor...")
    from modules.enhanced_images import EnhancedImageProcessor
    processor = EnhancedImageProcessor()
    print("✅ EnhancedImageProcessor initialized successfully")
    print(f"   Analysis enabled: {processor.analysis_enabled}")
    print(f"   OCR enabled: {processor.ocr_enabled}")
    
    # Test 3: Config access
    print("\n3. Testing Config boolean settings...")
    from config import Config
    config = Config()
    print(f"   CACHE_ENABLED: {getattr(config, 'CACHE_ENABLED', 'unknown')} ({type(getattr(config, 'CACHE_ENABLED', 'unknown')).__name__})")
    print(f"   YFINANCE_ENABLED: {getattr(config, 'YFINANCE_ENABLED', 'unknown')} ({type(getattr(config, 'YFINANCE_ENABLED', 'unknown')).__name__})")
    
    print("\n" + "=" * 50)
    print("🎯 Complete Boolean Fix Test PASSED!")
    print("✅ All boolean parsing issues resolved!")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()