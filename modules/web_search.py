"""
Web Search Module for AI Research Agent
Handles multiple search APIs and result aggregation
"""

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from config import Config

# Optional cache manager import
try:
    from .cache_manager import cache_manager
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False
    cache_manager = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearchEngine:
    """Main web search engine that aggregates results from multiple APIs"""
    
    def __init__(self):
        self.config = Config()
        self.search_engines = []
        
        # Initialize available search engines (excluding removed ones)
        # Google Search API - REMOVED (invalid/forbidden)
        # if self.config.GOOGLE_SEARCH_API_KEY and self.config.GOOGLE_SEARCH_ENGINE_ID:
        #     self.search_engines.append(GoogleSearchAPI())
        
        if self.config.SERPAPI_API_KEY:
            self.search_engines.append(SerpAPISearch())
            
        if self.config.BING_SEARCH_API_KEY:
            self.search_engines.append(BingSearchAPI())
            
        # NewsAPI - REMOVED (invalid key)
        # if self.config.NEWSAPI_KEY:
        #     self.search_engines.append(NewsAPISearch())
        
        if not self.search_engines:
            logger.warning("No search engines configured! App will have limited functionality.")
        else:
            logger.info(f"Initialized {len(self.search_engines)} search engines: {[engine.__class__.__name__ for engine in self.search_engines]}")
    
    def search(self, query: str, num_results: int = None, time_filter: str = None, include_images: bool = True) -> List[Dict]:
        """
        Perform comprehensive web search across multiple engines
        
        Args:
            query: Search query string
            num_results: Number of results to return (default from config)
            time_filter: Time filter ('day', 'week', 'month', 'year')
            include_images: Whether to include image search results
            
        Returns:
            List of search results with metadata
        """
        if num_results is None:
            num_results = self.config.MAX_SEARCH_RESULTS
        
        # Check cache first
        cache_params = {
            'num_results': num_results,
            'time_filter': time_filter,
            'include_images': include_images
        }
        
        if CACHE_AVAILABLE:
            cached_results = cache_manager.get_search_cache(query, cache_params)
            if cached_results:
                logger.info(f"Using cached search results for: {query[:50]}...")
                return cached_results
        
        all_results = []
        
        for engine in self.search_engines:
            try:
                logger.info(f"Searching with {engine.__class__.__name__}")
                results = engine.search(query, num_results, time_filter)
                all_results.extend(results)
                
                # Search for images if enabled and supported
                if include_images and hasattr(engine, 'search_images'):
                    try:
                        image_results = engine.search_images(query, min(5, num_results//2))
                        all_results.extend(image_results)
                    except Exception as img_e:
                        logger.warning(f"Image search failed for {engine.__class__.__name__}: {str(img_e)}")
                
                # Add small delay to respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error with {engine.__class__.__name__}: {str(e)}")
                continue
        
        # Remove duplicates and rank by relevance
        unique_results = self._deduplicate_results(all_results)
        ranked_results = self._rank_results(unique_results, query)
        
        # Separate images and text results for better organization
        text_results = [r for r in ranked_results if r.get('result_type') != 'image']
        image_results = [r for r in ranked_results if r.get('result_type') == 'image']
        
        # Combine results with images interspersed
        final_results = []
        max_results = min(num_results, len(text_results) + len(image_results))
        
        text_idx = 0
        image_idx = 0
        
        for i in range(max_results):
            # Add 3 text results, then 1 image result pattern
            if i % 4 != 3 and text_idx < len(text_results):
                final_results.append(text_results[text_idx])
                text_idx += 1
            elif image_idx < len(image_results):
                final_results.append(image_results[image_idx])
                image_idx += 1
            elif text_idx < len(text_results):
                final_results.append(text_results[text_idx])
                text_idx += 1
        
        
        # Cache the results before returning
        if CACHE_AVAILABLE:
            cache_manager.set_search_cache(query, cache_params, final_results[:num_results])
        
        return final_results[:num_results]
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate URLs and keep the best result for each URL"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def _rank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Rank results by relevance and quality"""
        # Simple ranking based on title relevance and domain authority
        query_words = set(query.lower().split())
        
        def score_result(result):
            score = 0
            
            # Title relevance
            title = result.get('title', '').lower()
            title_words = set(title.split())
            score += len(query_words.intersection(title_words)) * 2
            
            # Snippet relevance
            snippet = result.get('snippet', '').lower()
            snippet_words = set(snippet.split())
            score += len(query_words.intersection(snippet_words))
            
            # Domain authority (simple heuristic)
            domain = result.get('domain', '')
            if any(auth_domain in domain for auth_domain in ['edu', 'gov', 'org', 'nature.com', 'science.org']):
                score += 3
            
            return score
        
        # Sort by score (descending)
        results.sort(key=score_result, reverse=True)
        return results


class GoogleSearchAPI:
    """Google Custom Search API implementation"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    def search(self, query: str, num_results: int, time_filter: str = None) -> List[Dict]:
        """Search using Google Custom Search API"""
        params = {
            'key': self.config.GOOGLE_SEARCH_API_KEY,
            'cx': self.config.GOOGLE_SEARCH_ENGINE_ID,
            'q': query,
            'num': min(num_results, 10)  # Google API limit
        }
        
        if time_filter:
            # Convert time filter to Google's date format
            date_filter = self._get_date_filter(time_filter)
            if date_filter:
                params['dateRestrict'] = date_filter
        
        try:
            response = requests.get(self.base_url, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'domain': self._extract_domain(item.get('link', '')),
                    'source': 'Google Search',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Google Search API error: {str(e)}")
            return []
    
    def _get_date_filter(self, time_filter: str) -> Optional[str]:
        """Convert time filter to Google's dateRestrict format"""
        mapping = {
            'day': 'd1',
            'week': 'w1',
            'month': 'm1',
            'year': 'y1'
        }
        return mapping.get(time_filter)
    
    def search_images(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search for images using Google Custom Search API"""
        params = {
            'key': self.config.GOOGLE_SEARCH_API_KEY,
            'cx': self.config.GOOGLE_SEARCH_ENGINE_ID,
            'q': query,
            'searchType': 'image',
            'num': min(num_results, 10),
            'safe': 'active',
            'fileType': 'jpg,png,gif,webp'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'thumbnail': item.get('image', {}).get('thumbnailLink', ''),
                    'image_url': item.get('link', ''),
                    'context_url': item.get('image', {}).get('contextLink', ''),
                    'width': item.get('image', {}).get('width', 0),
                    'height': item.get('image', {}).get('height', 0),
                    'snippet': item.get('snippet', ''),
                    'domain': self._extract_domain(item.get('image', {}).get('contextLink', '')),
                    'source': 'Google Images',
                    'result_type': 'image',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Google Image Search API error: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ''


class SerpAPISearch:
    """SerpAPI implementation for web search"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, num_results: int, time_filter: str = None) -> List[Dict]:
        """Search using SerpAPI"""
        params = {
            'api_key': self.config.SERPAPI_API_KEY,
            'engine': 'google',
            'q': query,
            'num': min(num_results, 10)
        }
        
        if time_filter:
            params['tbs'] = self._get_tbs_filter(time_filter)
        
        try:
            response = requests.get(self.base_url, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for result in data.get('organic_results', []):
                result_data = {
                    'title': result.get('title', ''),
                    'url': result.get('link', ''),
                    'snippet': result.get('snippet', ''),
                    'domain': self._extract_domain(result.get('link', '')),
                    'source': 'SerpAPI',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result_data)
            
            return results
            
        except Exception as e:
            logger.error(f"SerpAPI error: {str(e)}")
            return []
    
    def _get_tbs_filter(self, time_filter: str) -> str:
        """Convert time filter to SerpAPI's tbs format"""
        mapping = {
            'day': 'qdr:d',
            'week': 'qdr:w',
            'month': 'qdr:m',
            'year': 'qdr:y'
        }
        return mapping.get(time_filter, '')
    
    def search_images(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search for images using SerpAPI"""
        params = {
            'api_key': self.config.SERPAPI_API_KEY,
            'engine': 'google_images',
            'q': query,
            'num': min(num_results, 10),
            'safe': 'active'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for result in data.get('images_results', []):
                result_data = {
                    'title': result.get('title', ''),
                    'url': result.get('original', ''),
                    'thumbnail': result.get('thumbnail', ''),
                    'image_url': result.get('original', ''),
                    'context_url': result.get('link', ''),
                    'width': result.get('original_width', 0),
                    'height': result.get('original_height', 0),
                    'snippet': result.get('snippet', ''),
                    'domain': self._extract_domain(result.get('link', '')),
                    'source': 'SerpAPI Images',
                    'result_type': 'image',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result_data)
            
            return results
            
        except Exception as e:
            logger.error(f"SerpAPI Image Search error: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ''


class BingSearchAPI:
    """Bing Web Search API implementation"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.bing.microsoft.com/v7.0/search"
    
    def search(self, query: str, num_results: int, time_filter: str = None) -> List[Dict]:
        """Search using Bing Web Search API"""
        headers = {
            'Ocp-Apim-Subscription-Key': self.config.BING_SEARCH_API_KEY
        }
        
        params = {
            'q': query,
            'count': min(num_results, 10),
            'mkt': 'en-US'
        }
        
        if time_filter:
            params['freshness'] = self._get_freshness_filter(time_filter)
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('webPages', {}).get('value', []):
                result = {
                    'title': item.get('name', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('snippet', ''),
                    'domain': self._extract_domain(item.get('url', '')),
                    'source': 'Bing Search',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Bing Search API error: {str(e)}")
            return []
    
    def _get_freshness_filter(self, time_filter: str) -> str:
        """Convert time filter to Bing's freshness format"""
        mapping = {
            'day': 'Day',
            'week': 'Week',
            'month': 'Month',
            'year': 'Year'
        }
        return mapping.get(time_filter, '')
    
    def search_images(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search for images using Bing Image Search API"""
        headers = {
            'Ocp-Apim-Subscription-Key': self.config.BING_SEARCH_API_KEY
        }
        
        params = {
            'q': query,
            'count': min(num_results, 10),
            'mkt': 'en-US',
            'safeSearch': 'Moderate',
            'imageType': 'Photo'
        }
        
        # Use Bing Image Search endpoint
        image_url = "https://api.bing.microsoft.com/v7.0/images/search"
        
        try:
            response = requests.get(image_url, headers=headers, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('value', []):
                result = {
                    'title': item.get('name', ''),
                    'url': item.get('contentUrl', ''),
                    'thumbnail': item.get('thumbnailUrl', ''),
                    'image_url': item.get('contentUrl', ''),
                    'context_url': item.get('hostPageUrl', ''),
                    'width': item.get('width', 0),
                    'height': item.get('height', 0),
                    'snippet': item.get('name', ''),
                    'domain': self._extract_domain(item.get('hostPageUrl', '')),
                    'source': 'Bing Images',
                    'result_type': 'image',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Bing Image Search API error: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ''


class NewsAPISearch:
    """NewsAPI implementation for news-specific searches"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://newsapi.org/v2/everything"
    
    def search(self, query: str, num_results: int, time_filter: str = None) -> List[Dict]:
        """Search using NewsAPI"""
        params = {
            'apiKey': self.config.NEWSAPI_KEY,
            'q': query,
            'pageSize': min(num_results, 10),
            'language': 'en',
            'sortBy': 'relevancy'
        }
        
        if time_filter:
            from_date = self._get_from_date(time_filter)
            if from_date:
                params['from'] = from_date
        
        try:
            response = requests.get(self.base_url, params=params, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for article in data.get('articles', []):
                result = {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'snippet': article.get('description', ''),
                    'domain': self._extract_domain(article.get('url', '')),
                    'source': 'NewsAPI',
                    'timestamp': article.get('publishedAt', datetime.now().isoformat()),
                    'author': article.get('author', ''),
                    'published_date': article.get('publishedAt', '')
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"NewsAPI error: {str(e)}")
            return []
    
    def _get_from_date(self, time_filter: str) -> Optional[str]:
        """Get from date based on time filter"""
        now = datetime.now()
        mapping = {
            'day': now - timedelta(days=1),
            'week': now - timedelta(weeks=1),
            'month': now - timedelta(days=30),
            'year': now - timedelta(days=365)
        }
        
        from_date = mapping.get(time_filter)
        return from_date.strftime('%Y-%m-%d') if from_date else None
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return ''


# Example usage and testing
if __name__ == "__main__":
    # Test the search functionality
    search_engine = WebSearchEngine()
    
    if search_engine.search_engines:
        print("Available search engines:")
        for engine in search_engine.search_engines:
            print(f"- {engine.__class__.__name__}")
        
        # Test search
        results = search_engine.search("artificial intelligence breakthroughs 2024", num_results=5)
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Source: {result['source']}")
            print()
    else:
        print("No search engines configured. Please add API keys to your .env file.")
