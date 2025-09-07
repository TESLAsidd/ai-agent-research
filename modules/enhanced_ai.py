"""
Enhanced AI Module with Multiple Providers
Provides faster, more accurate AI responses using multiple providers
"""

import json
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import concurrent.futures
import requests

from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAIProvider:
    """Manages multiple AI providers for enhanced performance"""
    
    def __init__(self):
        self.config = Config()
        self.providers = []
        
        # Initialize available providers
        if self.config.OPENAI_API_KEY:
            self.providers.append(OpenAIProvider())
        
        if self.config.PERPLEXITY_API_KEY:
            self.providers.append(PerplexityProvider())
        
        if self.config.ANTHROPIC_API_KEY:
            self.providers.append(AnthropicProvider())
    
    def get_fastest_response(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """Get response from the fastest available AI provider"""
        if not self.providers:
            return {"error": "No AI providers available"}
        
        # Use first available provider for speed
        for provider in self.providers:
            try:
                start_time = time.time()
                response = provider.generate_response(prompt, max_tokens)
                end_time = time.time()
                
                if response.get("success"):
                    response["response_time"] = round(end_time - start_time, 2)
                    response["provider"] = provider.__class__.__name__
                    return response
                    
            except Exception as e:
                logger.error(f"Provider {provider.__class__.__name__} failed: {str(e)}")
                continue
        
        return {"error": "All AI providers failed"}
    
    def get_parallel_responses(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """Get responses from multiple providers in parallel for comparison"""
        if not self.providers:
            return {"error": "No AI providers available"}
        
        responses = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            # Submit tasks to all providers
            future_to_provider = {
                executor.submit(provider.generate_response, prompt, max_tokens): provider
                for provider in self.providers
            }
            
            # Collect responses
            for future in concurrent.futures.as_completed(future_to_provider, timeout=30):
                provider = future_to_provider[future]
                try:
                    response = future.result()
                    responses[provider.__class__.__name__] = response
                except Exception as e:
                    responses[provider.__class__.__name__] = {"error": str(e)}
        
        return responses
    
    def get_best_response(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """Get the best response by comparing multiple providers"""
        parallel_responses = self.get_parallel_responses(prompt, max_tokens)
        
        # Find the best response based on success and length
        best_response = None
        best_score = 0
        
        for provider_name, response in parallel_responses.items():
            if response.get("success"):
                # Score based on content length and response time
                content_length = len(response.get("content", ""))
                response_time = response.get("response_time", 999)
                
                # Prefer longer content with faster response time
                score = content_length / (response_time + 1)
                
                if score > best_score:
                    best_score = score
                    best_response = response
                    best_response["provider"] = provider_name
                    best_response["alternatives"] = len(parallel_responses)
        
        return best_response or {"error": "No successful responses"}

class OpenAIProvider:
    """OpenAI API provider"""
    
    def __init__(self):
        self.config = Config()
        from openai import OpenAI
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """Generate response using OpenAI"""
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant that provides accurate, comprehensive, and well-structured responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=self.config.TEMPERATURE
            )
            
            end_time = time.time()
            
            return {
                "content": response.choices[0].message.content,
                "model": self.config.OPENAI_MODEL,
                "response_time": round(end_time - start_time, 2),
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "provider": "OpenAI"
            }

class PerplexityProvider:
    """Perplexity AI provider for real-time responses"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.config.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """Generate response using Perplexity AI"""
        try:
            start_time = time.time()
            
            payload = {
                "model": self.config.PERPLEXITY_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a knowledgeable research assistant with access to real-time information. Provide accurate, up-to-date, and comprehensive responses."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.1,
                "return_citations": True
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            end_time = time.time()
            data = response.json()
            
            return {
                "content": data["choices"][0]["message"]["content"],
                "model": self.config.PERPLEXITY_MODEL,
                "response_time": round(end_time - start_time, 2),
                "citations": data.get("citations", []),
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "real_time": True
            }
            
        except Exception as e:
            logger.error(f"Perplexity API error: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "provider": "Perplexity"
            }

class AnthropicProvider:
    """Anthropic Claude API provider"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.config.ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """Generate response using Anthropic Claude"""
        try:
            start_time = time.time()
            
            payload = {
                "model": self.config.ANTHROPIC_MODEL,
                "max_tokens": max_tokens,
                "temperature": self.config.TEMPERATURE,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            end_time = time.time()
            data = response.json()
            
            return {
                "content": data["content"][0]["text"],
                "model": self.config.ANTHROPIC_MODEL,
                "response_time": round(end_time - start_time, 2),
                "tokens_used": data.get("usage", {}).get("output_tokens", 0),
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "provider": "Anthropic"
            }

class EnhancedSummarizer:
    """Enhanced summarizer using multiple AI providers"""
    
    def __init__(self):
        self.ai_provider = MultiAIProvider()
    
    def fast_summarize(self, content: str, query: str, style: str = "comprehensive") -> Dict:
        """Generate fast summary using the best available AI provider"""
        
        # Create optimized prompt based on style
        if style == "brief":
            prompt = f"""Provide a brief summary (2-3 sentences) of the following content related to "{query}":

{content[:2000]}

Focus on the most important points only."""
        
        elif style == "detailed":
            prompt = f"""Provide a detailed analysis of the following content related to "{query}":

{content[:4000]}

Include:
1. Key findings and insights
2. Important statistics or data
3. Different perspectives
4. Implications and significance"""
        
        else:  # comprehensive
            prompt = f"""Analyze and summarize the following content related to "{query}":

{content[:3000]}

Provide:
1. Executive summary (2-3 sentences)
2. Key findings (3-5 bullet points)
3. Important details and context
4. Relevance to the research query"""
        
        # Get fastest response
        response = self.ai_provider.get_fastest_response(prompt, max_tokens=800)
        
        if response.get("success"):
            return {
                "summary": response["content"],
                "provider": response.get("provider", "Unknown"),
                "response_time": response.get("response_time", 0),
                "style": style,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
        else:
            return {
                "error": response.get("error", "Summarization failed"),
                "success": False
            }
    
    def parallel_analysis(self, content: str, query: str) -> Dict:
        """Get analysis from multiple AI providers for comparison"""
        
        prompt = f"""Analyze the following research content about "{query}":

{content[:3000]}

Provide:
1. Key insights and findings
2. Important trends or patterns
3. Credibility assessment
4. Relevance to the research topic"""
        
        return self.ai_provider.get_parallel_responses(prompt, max_tokens=1000)

# Example usage and testing
if __name__ == "__main__":
    enhancer = EnhancedSummarizer()
    
    sample_content = """
    Artificial intelligence has made significant advances in 2024, with breakthroughs in 
    large language models, computer vision, and robotics. Major tech companies have 
    released new AI models with improved capabilities and efficiency.
    """
    
    print("Testing enhanced AI summarization...")
    
    # Test fast summarization
    result = enhancer.fast_summarize(sample_content, "AI trends 2024", "brief")
    
    if result.get("success"):
        print(f"Summary generated in {result['response_time']} seconds")
        print(f"Provider: {result['provider']}")
        print(f"Summary: {result['summary'][:200]}...")
    else:
        print(f"Error: {result.get('error')}")