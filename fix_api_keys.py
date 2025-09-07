#!/usr/bin/env python3
"""
Interactive API Key Fixer for AI Research Agent
Helps you update non-working API keys step by step
"""

import os
import webbrowser
from dotenv import load_dotenv

def main():
    print("🔧 API Key Fix Assistant")
    print("=" * 50)
    print("Let's fix your API keys step by step!\n")
    
    # Load current .env
    load_dotenv()
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print("❌ .env file not found!")
        return
    
    print("📊 Issues found:")
    print("❌ OpenAI: Quota exceeded (no credits)")
    print("❌ Google Search: Invalid/forbidden") 
    print("❌ NewsAPI: Invalid key")
    print("❌ All enhanced APIs: Using placeholders\n")
    
    # Priority fixes
    priority_apis = [
        {
            "name": "🔥 Perplexity AI",
            "env_var": "PERPLEXITY_API_KEY",
            "website": "https://www.perplexity.ai/",
            "instructions": [
                "1. Click 'Sign Up' (free account)",
                "2. Go to Settings → API",
                "3. Click 'Generate API Key'",
                "4. Copy key starting with 'pplx-'"
            ],
            "benefit": "Real-time AI responses (replaces OpenAI)",
            "free_tier": "5 requests/hour FREE"
        },
        {
            "name": "🧠 Anthropic Claude",
            "env_var": "ANTHROPIC_API_KEY", 
            "website": "https://console.anthropic.com/",
            "instructions": [
                "1. Sign up for free account",
                "2. Verify email address",
                "3. Go to API Keys section",
                "4. Create new key starting with 'sk-ant-'"
            ],
            "benefit": "Superior AI analysis (backup for OpenAI)",
            "free_tier": "$5 FREE credits"
        },
        {
            "name": "🌐 Tavily Search",
            "env_var": "TAVILY_API_KEY",
            "website": "https://tavily.com/",
            "instructions": [
                "1. Sign up for free account",
                "2. Verify email",
                "3. Go to Dashboard → API Keys",
                "4. Copy key starting with 'tvly-'"
            ],
            "benefit": "Real-time web search (replaces Google)",
            "free_tier": "1000 searches/month FREE"
        }
    ]
    
    for api in priority_apis:
        print("=" * 50)
        print(f"\n{api['name']} - {api['benefit']}")
        print(f"Free Tier: {api['free_tier']}")
        print(f"Website: {api['website']}")
        
        # Check current value
        current_value = os.getenv(api['env_var'])
        if current_value and not current_value.endswith('-here'):
            print(f"✅ Already configured!")
            continue
        
        print("\n📋 Setup Steps:")
        for instruction in api['instructions']:
            print(f"   {instruction}")
        
        # Offer to open website
        try:
            choice = input(f"\n🌐 Open {api['website']} now? (y/n): ").lower().strip()
            if choice == 'y':
                webbrowser.open(api['website'])
                print("✅ Website opened in browser!")
                
                # Ask for the API key
                new_key = input(f"\n🔑 Paste your new {api['name']} API key: ").strip()
                if new_key and len(new_key) > 10:
                    # Update .env file
                    update_env_file(api['env_var'], new_key)
                    print(f"✅ {api['name']} key saved!")
                else:
                    print("⚠️ Invalid key - you can update manually later")
                    
        except KeyboardInterrupt:
            print("\n⏸️ Skipping this API...")
            continue
        except:
            print(f"💻 Manually visit: {api['website']}")
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. 💾 All changes saved to .env file")
    print("2. 🔄 Restart your Streamlit app:")
    print("   python -m streamlit run app.py")
    print("3. ✅ Test with: python test_api_keys.py")
    print("4. 🚀 Enjoy faster, better responses!")
    
    print(f"\n📁 .env file location: {os.path.abspath(env_path)}")

def update_env_file(var_name, new_value):
    """Update a specific variable in the .env file"""
    env_path = ".env"
    
    # Read current content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update the specific line
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{var_name}="):
            lines[i] = f"{var_name}={new_value}\n"
            updated = True
            break
    
    # If not found, add it
    if not updated:
        lines.append(f"{var_name}={new_value}\n")
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)

if __name__ == "__main__":
    main()