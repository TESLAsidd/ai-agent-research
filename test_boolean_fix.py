#!/usr/bin/env python3
"""
Test the historical data fix for boolean parsing
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from modules.historical_data import HistoricalDataAnalyzer
    from config import Config
    
    print("🧪 Testing Historical Data Boolean Fix...")
    print("=" * 50)
    
    # Test 1: Initialize HistoricalDataAnalyzer
    print("1. Testing HistoricalDataAnalyzer initialization...")
    analyzer = HistoricalDataAnalyzer()
    print("✅ HistoricalDataAnalyzer initialized successfully")
    
    # Test 2: Check data sources
    print(f"\n2. Data sources configuration:")
    for source, enabled in analyzer.data_sources.items():
        print(f"   {source}: {enabled} ({type(enabled).__name__})")
    
    # Test 3: Test a simple operation
    print(f"\n3. Testing stock trends functionality...")
    try:
        result = analyzer.get_stock_trends('AAPL', '1m')
        if result.get('success'):
            print("✅ Stock trends test successful")
            print(f"   Company: {result.get('company_name', 'N/A')}")
            print(f"   Current price: ${result.get('current_price', 'N/A')}")
        else:
            print(f"⚠️  Stock trends test returned error: {result.get('error', 'Unknown')}")
    except Exception as e:
        print(f"❌ Stock trends test failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Boolean Fix Test Complete!")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()