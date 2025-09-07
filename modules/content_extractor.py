"""
Content Extraction Module for AI Research Agent
Handles web scraping and content extraction from URLs
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime
import logging
from urllib.parse import urlparse, urljoin
import re

# Content extraction libraries
from bs4 import BeautifulSoup
import newspaper
from fake_useragent import UserAgent

# Optional imports
try:
    from trafilatura import extract as trafilatura_extract
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False
    trafilatura_extract = None

try:
    import readability
    READABILITY_AVAILABLE = True
except ImportError:
    READABILITY_AVAILABLE = False
    readability = None

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

class ContentExtractor:
    """Main content extraction engine"""
    
    def __init__(self):
        self.config = Config()
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def extract_from_urls(self, urls: List[str]) -> List[Dict]:
        """
        Extract content from a list of URLs
        
        Args:
            urls: List of URLs to extract content from
            
        Returns:
            List of extracted content with metadata
        """
        extracted_content = []
        
        for url in urls:
            try:
                logger.info(f"Extracting content from: {url}")
                content = self.extract_from_url(url)
                if content:
                    extracted_content.append(content)
                
                # Add delay to be respectful
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error extracting from {url}: {str(e)}")
                continue
        
        return extracted_content
    
    def extract_from_url(self, url: str) -> Optional[Dict]:
        """
        Extract content from a single URL using multiple methods
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary with extracted content and metadata
        """
        # Check cache first
        if CACHE_AVAILABLE:
            cached_content = cache_manager.get_content_cache(url)
            if cached_content:
                logger.info(f"Using cached content for: {url[:50]}...")
                return cached_content
        
        try:
            # Try multiple extraction methods (conditionally based on availability)
            methods = [self._extract_with_newspaper]
            
            if TRAFILATURA_AVAILABLE:
                methods.append(self._extract_with_trafilatura)
            
            if READABILITY_AVAILABLE:
                methods.append(self._extract_with_readability)
                
            methods.append(self._extract_with_beautifulsoup)
            
            best_content = None
            best_score = 0
            
            for method in methods:
                try:
                    content = method(url)
                    if content and self._score_content(content):
                        score = self._score_content(content)
                        if score > best_score:
                            best_score = score
                            best_content = content
                except Exception as e:
                    logger.debug(f"Method {method.__name__} failed: {str(e)}")
                    continue
            
            if best_content:
                best_content['extraction_method'] = best_content.get('extraction_method', 'unknown')
                best_content['content_score'] = best_score
                
                # Cache the result
                if CACHE_AVAILABLE:
                    cache_manager.set_content_cache(url, best_content)
                
                return best_content
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {str(e)}")
            return None
    
    def _extract_with_newspaper(self, url: str) -> Optional[Dict]:
        """Extract content using newspaper3k library"""
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            
            if len(article.text) < self.config.MIN_ARTICLE_LENGTH:
                return None
            
            return {
                'title': article.title or '',
                'text': article.text[:self.config.MAX_CONTENT_LENGTH],
                'authors': article.authors,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                'url': url,
                'domain': urlparse(url).netloc,
                'extraction_method': 'newspaper3k',
                'word_count': len(article.text.split()),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"Newspaper extraction failed: {str(e)}")
            return None
    
    def _extract_with_trafilatura(self, url: str) -> Optional[Dict]:
        """Extract content using trafilatura library"""
        if not TRAFILATURA_AVAILABLE:
            logger.debug("Trafilatura not available, skipping")
            return None
            
        try:
            response = self.session.get(url, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            # Extract main content
            content = trafilatura_extract(response.text, include_comments=False, include_tables=True)
            
            if not content or len(content) < self.config.MIN_ARTICLE_LENGTH:
                return None
            
            # Parse HTML to get title
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            return {
                'title': title_text,
                'text': content[:self.config.MAX_CONTENT_LENGTH],
                'url': url,
                'domain': urlparse(url).netloc,
                'extraction_method': 'trafilatura',
                'word_count': len(content.split()),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"Trafilatura extraction failed: {str(e)}")
            return None
    
    def _extract_with_readability(self, url: str) -> Optional[Dict]:
        """Extract content using readability-lxml library"""
        if not READABILITY_AVAILABLE:
            logger.debug("Readability not available, skipping")
            return None
            
        try:
            response = self.session.get(url, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            doc = readability.Document(response.text)
            content = doc.summary()
            
            if not content or len(content) < self.config.MIN_ARTICLE_LENGTH:
                return None
            
            # Parse the extracted content
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()
            
            # Get title from original document
            title_soup = BeautifulSoup(response.text, 'html.parser')
            title = title_soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            return {
                'title': title_text,
                'text': text_content[:self.config.MAX_CONTENT_LENGTH],
                'url': url,
                'domain': urlparse(url).netloc,
                'extraction_method': 'readability',
                'word_count': len(text_content.split()),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"Readability extraction failed: {str(e)}")
            return None
    
    def _extract_with_beautifulsoup(self, url: str) -> Optional[Dict]:
        """Extract content using BeautifulSoup as fallback"""
        try:
            response = self.session.get(url, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find main content areas
            content_selectors = [
                'article',
                'main',
                '.content',
                '.post-content',
                '.entry-content',
                '.article-content',
                '#content',
                '.main-content'
            ]
            
            content_element = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    break
            
            if not content_element:
                content_element = soup.find('body')
            
            text_content = content_element.get_text() if content_element else soup.get_text()
            
            # Clean up text
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            if len(text_content) < self.config.MIN_ARTICLE_LENGTH:
                return None
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            return {
                'title': title_text,
                'text': text_content[:self.config.MAX_CONTENT_LENGTH],
                'url': url,
                'domain': urlparse(url).netloc,
                'extraction_method': 'beautifulsoup',
                'word_count': len(text_content.split()),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"BeautifulSoup extraction failed: {str(e)}")
            return None
    
    def _score_content(self, content: Dict) -> int:
        """Score content quality based on various factors"""
        score = 0
        
        # Length score
        word_count = content.get('word_count', 0)
        if word_count > 500:
            score += 3
        elif word_count > 200:
            score += 2
        elif word_count > 100:
            score += 1
        
        # Title quality
        title = content.get('title', '')
        if len(title) > 10 and len(title) < 200:
            score += 2
        
        # Domain authority (simple heuristic)
        domain = content.get('domain', '')
        if any(auth_domain in domain.lower() for auth_domain in ['edu', 'gov', 'org', 'nature.com', 'science.org', 'arxiv.org']):
            score += 3
        
        # Content structure
        text = content.get('text', '')
        if any(indicator in text.lower() for indicator in ['abstract', 'introduction', 'conclusion', 'methodology']):
            score += 2
        
        return score
    
    def extract_key_phrases(self, text: str, num_phrases: int = 10) -> List[str]:
        """Extract key phrases from text using simple frequency analysis"""
        try:
            # Simple key phrase extraction
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            
            # Remove common stop words
            stop_words = {
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
                'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
                'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
                'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
                'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
            }
            
            filtered_words = [word for word in words if word not in stop_words]
            
            # Count word frequencies
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top phrases
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:num_phrases]]
            
        except Exception as e:
            logger.error(f"Key phrase extraction failed: {str(e)}")
            return []
    
    def summarize_content(self, content_list: List[Dict]) -> Dict:
        """Create a summary of extracted content"""
        if not content_list:
            return {}
        
        total_articles = len(content_list)
        total_words = sum(content.get('word_count', 0) for content in content_list)
        
        # Extract common themes
        all_text = ' '.join(content.get('text', '') for content in content_list)
        key_phrases = self.extract_key_phrases(all_text, 15)
        
        # Get source diversity
        domains = set(content.get('domain', '') for content in content_list)
        
        return {
            'total_articles': total_articles,
            'total_words': total_words,
            'average_words_per_article': total_words // total_articles if total_articles > 0 else 0,
            'unique_domains': len(domains),
            'domains': list(domains),
            'key_phrases': key_phrases,
            'extraction_summary_timestamp': datetime.now().isoformat()
        }


# Example usage and testing
if __name__ == "__main__":
    extractor = ContentExtractor()
    
    # Test URLs
    test_urls = [
        "https://www.nature.com/articles/s41586-024-07354-8",
        "https://www.science.org/content/article/ai-breakthrough-2024"
    ]
    
    print("Testing content extraction...")
    results = extractor.extract_from_urls(test_urls)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Article {i} ---")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        print(f"Word Count: {result.get('word_count', 0)}")
        print(f"Method: {result.get('extraction_method', 'N/A')}")
        print(f"Score: {result.get('content_score', 0)}")
        print(f"Text Preview: {result.get('text', '')[:200]}...")
