#!/usr/bin/env python3
"""
Direct test of Perplexity API to check valid models
"""

import requests
import os
import json

# Load API key from .env
from dotenv import load_dotenv
load_dotenv()

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not PERPLEXITY_API_KEY:
    print("No PERPLEXITY_API_KEY found")
    exit(1)

print("Testing Perplexity API models...")
print(f"API Key: {PERPLEXITY_API_KEY[:20]}...")

# Test different model names
models_to_test = [
    'llama-3.1-sonar-small-128k-chat',
    'llama-3.1-sonar-large-128k-chat', 
    'sonar-small-chat',
    'sonar-medium-chat'
]

for model in models_to_test:
    print(f"\nTesting model: {model}")
    
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': 'Summarize: Artificial intelligence is transforming technology.'
            }
        ],
        'max_tokens': 100,
        'temperature': 0.2
    }
    
    try:
        response = requests.post(
            'https://api.perplexity.ai/chat/completions',
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'][:100]
            print(f"SUCCESS: {content}...")
            print(f"Model '{model}' is VALID and working!")
            break
        else:
            print(f"Error {response.status_code}: {response.text[:200]}...")
            
    except Exception as e:
        print(f"Exception: {str(e)[:100]}...")

print("\nPerplexity API test complete!")