"""
Optional Dependencies Installer for AI Research Agent
Installs optional dependencies for enhanced features like image analysis and OCR
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def main():
    print("🚀 Installing optional dependencies for AI Research Agent...")
    print("=" * 60)
    
    # Core packages that might be missing
    core_packages = [
        "pytesseract==0.3.10",
        "opencv-python==4.8.1.78", 
        "Pillow==10.1.0",
        "scikit-learn==1.3.2",
        "numpy==1.24.3"
    ]
    
    success_count = 0
    total_packages = len(core_packages)
    
    for package in core_packages:
        print(f"\n📦 Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Installation complete: {success_count}/{total_packages} packages installed successfully")
    
    if success_count == total_packages:
        print("🎉 All optional dependencies installed! You can now use:")
        print("   - Image search and analysis")
        print("   - OCR text extraction from images")
        print("   - Advanced visualizations")
        print("   - Intelligent caching")
    else:
        print("⚠️  Some packages failed to install. The app will work with reduced functionality.")
        print("   You can still use:")
        print("   - Web search")
        print("   - Content extraction")
        print("   - AI summarization")
        print("   - Basic visualizations")
    
    print("\n🚀 You can now run the app with: streamlit run app.py")

if __name__ == "__main__":
    main()