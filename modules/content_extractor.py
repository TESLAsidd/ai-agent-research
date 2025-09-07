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
                # Enhance with key points and brief details
                enhanced_content = self._enhance_with_key_points(best_content)
                enhanced_content['extraction_method'] = enhanced_content.get('extraction_method', 'unknown')
                enhanced_content['content_score'] = best_score
                
                # Cache the result
                if CACHE_AVAILABLE:
                    cache_manager.set_content_cache(url, enhanced_content)
                
                return enhanced_content
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {str(e)}")
            return None
    
    def _enhance_with_key_points(self, content: Dict) -> Dict:
        """
        Enhance extracted content with key points and brief details
        
        Args:
            content: Extracted content dictionary
            
        Returns:
            Enhanced content with key points
        """
        try:
            text = content.get('text', '')
            if not text:
                return content
            
            # Extract key points from the content
            key_points = self._extract_key_points(text)
            content['key_points'] = key_points
            
            # Extract brief summary
            brief_summary = self._extract_brief_summary(text)
            content['brief_summary'] = brief_summary
            
            return content
        except Exception as e:
            logger.error(f"Failed to enhance content with key points: {str(e)}")
            return content
    
    def _extract_key_points(self, text: str) -> List[str]:
        """
        Extract key points from text content
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of key points
        """
        try:
            # Split text into sentences
            sentences = re.split(r'[.!?]+', text)
            
            # Enhanced important indicators for better key point detection
            important_indicators = [
                'important', 'significant', 'key', 'main', 'primary', 'crucial', 'essential',
                'finding', 'discovery', 'result', 'conclusion', 'benefit', 'advantage',
                'challenge', 'problem', 'solution', 'approach', 'method', 'technique',
                'according to', 'researchers found', 'study shows', 'evidence suggests',
                'impact', 'effect', 'influence', 'relationship', 'correlation', 'cause',
                'recommend', 'suggest', 'propose', 'indicate', 'demonstrate', 'reveal',
                'increase', 'decrease', 'improve', 'reduce', 'enhance', 'decline'
            ]
            
            # Additional patterns for identifying important sentences
            patterns = [
                r'\d+\s*(?:percent|%)',  # Percentage patterns
                r'\d+\s*(?:million|billion|thousand)',  # Number patterns
                r'(?:first|second|third|fourth|fifth|major|primary)\s+(?:finding|discovery|result)',  # Ranking patterns
                r'(?:in|during|over)\s+(?:\d+|recent|past|last)\s*(?:year|month|week|day)s?',  # Time patterns
            ]
            
            key_points = []
            for sentence in sentences[:40]:  # Increased limit to first 40 sentences
                sentence = sentence.strip()
                if len(sentence) < 30 or len(sentence) > 300:  # Adjusted length constraints
                    continue
                
                # Check if sentence contains important indicators
                sentence_lower = sentence.lower()
                score = 0
                
                # Score based on important indicators
                for indicator in important_indicators:
                    if indicator in sentence_lower:
                        score += 1
                
                # Score based on patterns
                for pattern in patterns:
                    if re.search(pattern, sentence_lower):
                        score += 2  # Higher weight for patterns
                
                # Include sentence if it has a good score
                if score >= 1:
                    # Clean up the sentence
                    clean_sentence = sentence.strip()
                    if clean_sentence and not clean_sentence.endswith(('.', '!', '?')):
                        clean_sentence += '.'
                    
                    if clean_sentence:
                        key_points.append({
                            'text': clean_sentence,
                            'score': score
                        })
            
            # Sort by score and take top points
            key_points.sort(key=lambda x: x['score'], reverse=True)
            
            # Extract just the text and remove duplicates while preserving order
            unique_points = []
            seen = set()
            for point in key_points:
                text = point['text']
                if text not in seen:
                    seen.add(text)
                    unique_points.append(text)
            
            return unique_points[:10]  # Return top 10 key points
            
        except Exception as e:
            logger.error(f"Failed to extract key points: {str(e)}")
            return []
    
    def _extract_brief_summary(self, text: str) -> str:
        """
        Extract a brief summary from text content
        
        Args:
            text: Text content to summarize
            
        Returns:
            Brief summary string
        """
        try:
            # Take the first few sentences as a brief summary
            sentences = re.split(r'[.!?]+', text)
            
            # Filter and clean sentences
            clean_sentences = []
            for s in sentences[:10]:  # Look at first 10 sentences
                s = s.strip()
                # Only include sentences with reasonable length
                if 30 <= len(s) <= 300:
                    clean_sentences.append(s)
            
            # Select the most informative sentences (first and potentially others with indicators)
            summary_sentences = []
            
            if clean_sentences:
                # Always include the first sentence as it's often introductory
                summary_sentences.append(clean_sentences[0])
                
                # Look for sentences with important indicators
                important_indicators = [
                    'important', 'significant', 'key', 'main', 'primary', 'crucial',
                    'finding', 'discovery', 'result', 'conclusion', 'benefit',
                    'according to', 'researchers found', 'study shows', 'evidence suggests'
                ]
                
                for sentence in clean_sentences[1:5]:  # Check next 4 sentences
                    sentence_lower = sentence.lower()
                    if any(indicator in sentence_lower for indicator in important_indicators):
                        if sentence not in summary_sentences:  # Avoid duplicates
                            summary_sentences.append(sentence)
                            if len(summary_sentences) >= 3:  # Limit to 3 sentences
                                break
            
            # If we still don't have enough, add more clean sentences
            for sentence in clean_sentences[1:]:
                if len(summary_sentences) >= 3:
                    break
                if sentence not in summary_sentences:
                    summary_sentences.append(sentence)
            
            # Create the summary
            if summary_sentences:
                summary = '. '.join(summary_sentences[:3])  # Max 3 sentences
                if not summary.endswith(('.', '!', '?')):
                    summary += '.'
                return summary
            else:
                # Fallback to first part of text
                return text[:250] + "..." if len(text) > 250 else text
                
        except Exception as e:
            logger.error(f"Failed to extract brief summary: {str(e)}")
            return text[:250] + "..." if len(text) > 250 else text
    
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
        """Extract content using readability library"""
        if not READABILITY_AVAILABLE:
            logger.debug("Readability not available, skipping")
            return None
            
        try:
            response = self.session.get(url, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            # Parse with readability
            doc = readability.Document(response.text)
            title = doc.title()
            content = doc.summary()
            
            # Clean HTML tags from content
            soup = BeautifulSoup(content, 'html.parser')
            clean_content = soup.get_text()
            
            if len(clean_content) < self.config.MIN_ARTICLE_LENGTH:
                return None
            
            return {
                'title': title,
                'text': clean_content[:self.config.MAX_CONTENT_LENGTH],
                'url': url,
                'domain': urlparse(url).netloc,
                'extraction_method': 'readability',
                'word_count': len(clean_content.split()),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"Readability extraction failed: {str(e)}")
            return None
    
    def _extract_with_beautifulsoup(self, url: str) -> Optional[Dict]:
        """Extract content using BeautifulSoup"""
        try:
            response = self.session.get(url, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ''
            
            # Get main content (try common content containers)
            content_selectors = ['article', '.content', '.post', '.article', 'main', '.main']
            content_text = ''
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text()
                    break
            
            # Fallback to body text if no specific content container found
            if not content_text:
                body = soup.find('body')
                if body:
                    content_text = body.get_text()
            
            # Clean up whitespace
            content_text = re.sub(r'\s+', ' ', content_text).strip()
            
            if len(content_text) < self.config.MIN_ARTICLE_LENGTH:
                return None
            
            return {
                'title': title,
                'text': content_text[:self.config.MAX_CONTENT_LENGTH],
                'url': url,
                'domain': urlparse(url).netloc,
                'extraction_method': 'beautifulsoup',
                'word_count': len(content_text.split()),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"BeautifulSoup extraction failed: {str(e)}")
            return None
    
    def _score_content(self, content: Dict) -> float:
        """
        Score content quality based on various factors
        
        Args:
            content: Extracted content dictionary
            
        Returns:
            Quality score between 0 and 1
        """
        try:
            text = content.get('text', '')
            title = content.get('title', '')
            word_count = content.get('word_count', 0)
            
            if not text:
                return 0.0
            
            score = 0.0
            
            # Length scoring (prefer content of reasonable length)
            if 200 <= word_count <= 5000:
                score += 0.3
            elif word_count > 5000:
                score += 0.2
            elif word_count >= 100:
                score += 0.1
            
            # Title scoring
            if title and len(title) > 10:
                score += 0.2
            
            # Content quality scoring (check for too much repetition)
            if word_count > 0:
                unique_words = len(set(text.split()))
                diversity_ratio = unique_words / word_count
                if diversity_ratio > 0.4:
                    score += 0.3
                elif diversity_ratio > 0.2:
                    score += 0.2
                else:
                    score += 0.1
            
            # Check for structured content (headings, lists, etc.)
            if content.get('extraction_method') in ['newspaper3k', 'trafilatura']:
                score += 0.2
            
            return min(score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.debug(f"Content scoring failed: {str(e)}")
            return 0.1  # Default low score