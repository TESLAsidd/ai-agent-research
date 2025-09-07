"""
Enhanced Search Module with Perplexity and Real-time APIs
Provides faster, more accurate, and real-time search capabilities
"""

import requests
import json
import time
import asyncio
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexitySearchEngine:
    """Perplexity AI search engine for real-time responses"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.config.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def search_and_summarize(self, query: str, num_results: int = 5) -> Dict:
        """Search and get AI-powered summary in one call"""
        if not self.config.PERPLEXITY_API_KEY:
            return {"error": "Perplexity API key not configured", "success": False}
        
        # Updated prompt with better structure
        prompt = f"""
        Research the topic: "{query}"
        
        Please provide a comprehensive response with:
        1. A detailed summary of current information about this topic
        2. Key findings and recent developments (2024-2025)
        3. Multiple credible sources with URLs
        4. Statistical data or facts if available
        5. Different perspectives on the topic
        
        Format your response clearly with sections and include source citations at the end.
        """
        
        # Updated payload with correct model name and parameters
        payload = {
            "model": self.config.PERPLEXITY_MODEL,  # This should be a valid model
            "messages": [
                {
                    "role": "system",
                    "content": "You are a research assistant that provides comprehensive, accurate, and up-to-date information with proper citations. Focus on recent developments from 2024-2025."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
            "top_p": 0.9,
            "return_citations": True,
            "return_images": False
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            citations = data.get("citations", [])
            
            return {
                "summary": content,
                "citations": citations,
                "source": "Perplexity AI",
                "timestamp": datetime.now().isoformat(),
                "model": self.config.PERPLEXITY_MODEL,
                "success": True
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"Perplexity API HTTP error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}
        except Exception as e:
            error_msg = f"Perplexity search failed: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}

class TavilySearchEngine:
    """Tavily API for real-time web search"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.tavily.com/search"
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Perform real-time web search with Tavily"""
        if not self.config.TAVILY_API_KEY:
            return []
        
        payload = {
            "api_key": self.config.TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "include_answer": True,
            "include_images": True,
            "include_raw_content": True,
            "max_results": num_results
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("results", []):
                result = {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("content", ""),
                    "score": item.get("score", 0),
                    "domain": self._extract_domain(item.get("url", "")),
                    "source": "Tavily Search",
                    "timestamp": datetime.now().isoformat(),
                    "raw_content": item.get("raw_content", "")
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Tavily search failed: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ""

class ExaSearchEngine:
    """Exa API for semantic search"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.exa.ai/search"
        self.headers = {
            "Authorization": f"Bearer {self.config.EXA_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Perform semantic search with Exa"""
        if not self.config.EXA_API_KEY:
            return []
        
        payload = {
            "query": query,
            "type": "neural",
            "useAutoprompt": True,
            "numResults": num_results,
            "contents": {
                "text": True,
                "highlights": True,
                "summary": True
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=10  # Reduced timeout to prevent hanging
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("results", []):
                result = {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("summary", ""),
                    "highlights": item.get("highlights", []),
                    "score": item.get("score", 0),
                    "domain": self._extract_domain(item.get("url", "")),
                    "source": "Exa Search",
                    "timestamp": datetime.now().isoformat(),
                    "text": item.get("text", "")
                }
                results.append(result)
            
            return results
            
        except requests.exceptions.Timeout:
            logger.warning("Exa search timed out, returning empty results")
            return []
        except Exception as e:
            logger.error(f"Exa search failed: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ""

class YouSearchEngine:
    """You.com API for fast search results"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.yousearch.io/search"
        self.headers = {
            "X-API-Key": self.config.YOU_API_KEY
        }
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search with You.com API"""
        if not self.config.YOU_API_KEY:
            return []
        
        params = {
            "query": query,
            "num_web_results": num_results,
            "safesearch": "moderate"
        }
        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("web_results", []):
                result = {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "domain": self._extract_domain(item.get("url", "")),
                    "source": "You.com Search",
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"You.com search failed: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ""

class EnhancedSearchEngine:
    """Enhanced search engine combining multiple fast APIs"""
    
    def __init__(self):
        self.config = Config()
        self.engines = []
        
        # Initialize available search engines
        if self.config.PERPLEXITY_API_KEY:
            self.perplexity = PerplexitySearchEngine()
        
        if self.config.TAVILY_API_KEY:
            self.engines.append(TavilySearchEngine())
        
        if self.config.EXA_API_KEY:
            self.engines.append(ExaSearchEngine())
            
        if self.config.YOU_API_KEY:
            self.engines.append(YouSearchEngine())
    
    def fast_search_and_analyze(self, query: str, num_results: int = 10) -> Dict:
        """
        Perform ultra-fast search and analysis using multiple APIs
        Returns comprehensive results in minimal time
        """
        start_time = time.time()
        
        # Use Perplexity for instant AI-powered summary if available
        perplexity_result = None
        if hasattr(self, 'perplexity'):
            try:
                perplexity_result = self.perplexity.search_and_summarize(query)
                if not perplexity_result.get('success', False):
                    logger.warning(f"Perplexity search failed: {perplexity_result.get('error', 'Unknown error')}")
                    perplexity_result = None
            except Exception as e:
                logger.error(f"Perplexity search failed: {str(e)}")
                perplexity_result = None
        
        # Parallel search across other engines
        search_results = []
        if self.engines:
            with ThreadPoolExecutor(max_workers=len(self.engines)) as executor:
                # Submit all search tasks
                future_to_engine = {
                    executor.submit(engine.search, query, num_results // len(self.engines)): engine
                    for engine in self.engines
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_engine):
                    try:
                        results = future.result(timeout=10)
                        search_results.extend(results)
                    except Exception as e:
                        logger.error(f"Search engine failed: {str(e)}")
        else:
            logger.warning("No enhanced search engines available, falling back to standard search")
        
        # Combine and rank results
        combined_results = self._combine_and_rank_results(search_results, query)
        
        end_time = time.time()
        
        return {
            "query": query,
            "perplexity_summary": perplexity_result,
            "search_results": combined_results[:num_results],
            "total_sources": len(search_results),
            "search_time": round(end_time - start_time, 2),
            "engines_used": [engine.__class__.__name__ for engine in self.engines],
            "timestamp": datetime.now().isoformat(),
            "has_perplexity": perplexity_result is not None
        }
    
    def _combine_and_rank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Combine and rank results by relevance and quality"""
        if not results:
            return []
        
        # Remove duplicates
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        # Score and rank results
        query_words = set(query.lower().split())
        
        def calculate_score(result):
            score = 0
            
            # Title relevance
            title = result.get("title", "").lower()
            title_words = set(title.split())
            score += len(query_words.intersection(title_words)) * 3
            
            # Snippet relevance
            snippet = result.get("snippet", "").lower()
            snippet_words = set(snippet.split())
            score += len(query_words.intersection(snippet_words)) * 2
            
            # Source quality bonus
            source = result.get("source", "")
            if "Exa" in source:  # Semantic search gets bonus
                score += 2
            elif "Tavily" in source:  # Real-time search gets bonus
                score += 1.5
            
            # Domain authority bonus
            domain = result.get("domain", "")
            if any(auth in domain for auth in ["edu", "gov", "org"]):
                score += 2
            
            # Existing score from API
            api_score = result.get("score", 0)
            score += api_score if isinstance(api_score, (int, float)) else 0
            
            return score
        
        # Sort by calculated score
        unique_results.sort(key=calculate_score, reverse=True)
        return unique_results
    
    def get_available_engines(self) -> List[str]:
        """Get list of available search engines"""
        available = []
        
        if hasattr(self, 'perplexity'):
            available.append("Perplexity AI")
        
        available.extend([engine.__class__.__name__ for engine in self.engines])
        
        return available

# Example usage and testing
if __name__ == "__main__":
    enhanced_search = EnhancedSearchEngine()
    
    print("Available search engines:", enhanced_search.get_available_engines())
    
    # Test search
    results = enhanced_search.fast_search_and_analyze("artificial intelligence trends 2024", 5)
    
    print(f"Search completed in {results['search_time']} seconds")
    print(f"Found {results['total_sources']} total sources")
    
    if results.get('perplexity_summary'):
        print("Perplexity Summary Available: Yes")
    
    print(f"Top {len(results['search_results'])} results:")
    for i, result in enumerate(results['search_results'], 1):
        print(f"{i}. {result['title']} ({result['source']})")