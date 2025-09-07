"""
Cache Manager for AI Research Agent
Provides intelligent caching for search results, content extraction, and AI summaries
"""

import json
import hashlib
import os
import pickle
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    """Intelligent caching system for research results"""
    
    def __init__(self, cache_dir: str = "cache", max_age_hours: int = 24, max_cache_size_mb: int = 100):
        self.cache_dir = Path(cache_dir)
        self.max_age = timedelta(hours=max_age_hours)
        self.max_cache_size = max_cache_size_mb * 1024 * 1024  # Convert to bytes
        
        # Create cache directories
        self.cache_dir.mkdir(exist_ok=True)
        (self.cache_dir / "search").mkdir(exist_ok=True)
        (self.cache_dir / "content").mkdir(exist_ok=True)
        (self.cache_dir / "summaries").mkdir(exist_ok=True)
        (self.cache_dir / "images").mkdir(exist_ok=True)
        
        # Clean old cache on initialization
        self._cleanup_old_cache()
    
    def _generate_cache_key(self, data: Any) -> str:
        """Generate a unique cache key from data"""
        if isinstance(data, dict):
            # Sort dict for consistent hashing
            data_str = json.dumps(data, sort_keys=True)
        elif isinstance(data, str):
            data_str = data
        else:
            data_str = str(data)
        
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _get_cache_path(self, cache_type: str, cache_key: str) -> Path:
        """Get the full path for a cache file"""
        return self.cache_dir / cache_type / f"{cache_key}.cache"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache file is still valid (not expired)"""
        if not cache_path.exists():
            return False
        
        file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return datetime.now() - file_time < self.max_age
    
    def get_search_cache(self, query: str, search_params: Dict) -> Optional[List[Dict]]:
        """Get cached search results"""
        cache_key = self._generate_cache_key({
            'query': query,
            'params': search_params
        })
        
        cache_path = self._get_cache_path("search", cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                logger.info(f"Cache hit for search query: {query[:50]}...")
                return cached_data
            except Exception as e:
                logger.error(f"Failed to load search cache: {str(e)}")
                # Remove corrupted cache file
                cache_path.unlink(missing_ok=True)
        
        return None
    
    def set_search_cache(self, query: str, search_params: Dict, results: List[Dict]):
        """Cache search results"""
        cache_key = self._generate_cache_key({
            'query': query,
            'params': search_params
        })
        
        cache_path = self._get_cache_path("search", cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(results, f)
            logger.info(f"Cached search results for: {query[:50]}...")
        except Exception as e:
            logger.error(f"Failed to cache search results: {str(e)}")
    
    def get_content_cache(self, url: str) -> Optional[Dict]:
        """Get cached content extraction results"""
        cache_key = self._generate_cache_key(url)
        cache_path = self._get_cache_path("content", cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                logger.info(f"Cache hit for content: {url[:50]}...")
                return cached_data
            except Exception as e:
                logger.error(f"Failed to load content cache: {str(e)}")
                cache_path.unlink(missing_ok=True)
        
        return None
    
    def set_content_cache(self, url: str, content: Dict):
        """Cache content extraction results"""
        cache_key = self._generate_cache_key(url)
        cache_path = self._get_cache_path("content", cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(content, f)
            logger.info(f"Cached content for: {url[:50]}...")
        except Exception as e:
            logger.error(f"Failed to cache content: {str(e)}")
    
    def get_summary_cache(self, content_hash: str, query: str, summary_type: str) -> Optional[Dict]:
        """Get cached AI summary results"""
        cache_key = self._generate_cache_key({
            'content_hash': content_hash,
            'query': query,
            'summary_type': summary_type
        })
        
        cache_path = self._get_cache_path("summaries", cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                logger.info(f"Cache hit for summary: {query[:50]}...")
                return cached_data
            except Exception as e:
                logger.error(f"Failed to load summary cache: {str(e)}")
                cache_path.unlink(missing_ok=True)
        
        return None
    
    def set_summary_cache(self, content_hash: str, query: str, summary_type: str, summary: Dict):
        """Cache AI summary results"""
        cache_key = self._generate_cache_key({
            'content_hash': content_hash,
            'query': query,
            'summary_type': summary_type
        })
        
        cache_path = self._get_cache_path("summaries", cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(summary, f)
            logger.info(f"Cached summary for: {query[:50]}...")
        except Exception as e:
            logger.error(f"Failed to cache summary: {str(e)}")
    
    def get_image_cache(self, query: str, search_params: Dict) -> Optional[List[Dict]]:
        """Get cached image search results"""
        cache_key = self._generate_cache_key({
            'query': query,
            'params': search_params,
            'type': 'images'
        })
        
        cache_path = self._get_cache_path("images", cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                logger.info(f"Cache hit for image search: {query[:50]}...")
                return cached_data
            except Exception as e:
                logger.error(f"Failed to load image cache: {str(e)}")
                cache_path.unlink(missing_ok=True)
        
        return None
    
    def set_image_cache(self, query: str, search_params: Dict, results: List[Dict]):
        """Cache image search results"""
        cache_key = self._generate_cache_key({
            'query': query,
            'params': search_params,
            'type': 'images'
        })
        
        cache_path = self._get_cache_path("images", cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(results, f)
            logger.info(f"Cached image results for: {query[:50]}...")
        except Exception as e:
            logger.error(f"Failed to cache image results: {str(e)}")
    
    def _cleanup_old_cache(self):
        """Remove expired cache files and manage cache size"""
        try:
            total_size = 0
            cache_files = []
            
            # Collect all cache files with their stats
            for cache_type in ["search", "content", "summaries", "images"]:
                cache_type_dir = self.cache_dir / cache_type
                if cache_type_dir.exists():
                    for cache_file in cache_type_dir.glob("*.cache"):
                        file_stat = cache_file.stat()
                        file_time = datetime.fromtimestamp(file_stat.st_mtime)
                        
                        # Remove expired files
                        if datetime.now() - file_time > self.max_age:
                            cache_file.unlink()
                            logger.info(f"Removed expired cache: {cache_file.name}")
                        else:
                            cache_files.append({
                                'path': cache_file,
                                'size': file_stat.st_size,
                                'time': file_time
                            })
                            total_size += file_stat.st_size
            
            # If cache is too large, remove oldest files
            if total_size > self.max_cache_size:
                # Sort by time (oldest first)
                cache_files.sort(key=lambda x: x['time'])
                
                while total_size > self.max_cache_size * 0.8:  # Reduce to 80% of max
                    if not cache_files:
                        break
                    
                    oldest_file = cache_files.pop(0)
                    oldest_file['path'].unlink()
                    total_size -= oldest_file['size']
                    logger.info(f"Removed old cache for size limit: {oldest_file['path'].name}")
        
        except Exception as e:
            logger.error(f"Failed to cleanup cache: {str(e)}")
    
    def clear_cache(self, cache_type: str = None):
        """Clear all cache or specific cache type"""
        try:
            if cache_type:
                cache_type_dir = self.cache_dir / cache_type
                if cache_type_dir.exists():
                    for cache_file in cache_type_dir.glob("*.cache"):
                        cache_file.unlink()
                    logger.info(f"Cleared {cache_type} cache")
            else:
                for cache_type in ["search", "content", "summaries", "images"]:
                    cache_type_dir = self.cache_dir / cache_type
                    if cache_type_dir.exists():
                        for cache_file in cache_type_dir.glob("*.cache"):
                            cache_file.unlink()
                logger.info("Cleared all cache")
        
        except Exception as e:
            logger.error(f"Failed to clear cache: {str(e)}")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        stats = {
            'total_files': 0,
            'total_size_mb': 0,
            'by_type': {}
        }
        
        try:
            for cache_type in ["search", "content", "summaries", "images"]:
                cache_type_dir = self.cache_dir / cache_type
                type_files = 0
                type_size = 0
                
                if cache_type_dir.exists():
                    for cache_file in cache_type_dir.glob("*.cache"):
                        type_files += 1
                        type_size += cache_file.stat().st_size
                
                stats['by_type'][cache_type] = {
                    'files': type_files,
                    'size_mb': round(type_size / (1024 * 1024), 2)
                }
                
                stats['total_files'] += type_files
                stats['total_size_mb'] += stats['by_type'][cache_type]['size_mb']
            
            stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        
        except Exception as e:
            logger.error(f"Failed to get cache stats: {str(e)}")
        
        return stats
    
    def generate_content_hash(self, content_list: List[Dict]) -> str:
        """Generate a hash for content list to use as cache key"""
        # Create a simplified representation for hashing
        content_signatures = []
        for content in content_list:
            signature = {
                'url': content.get('url', ''),
                'title': content.get('title', ''),
                'word_count': content.get('word_count', 0)
            }
            content_signatures.append(signature)
        
        return self._generate_cache_key(content_signatures)


# Global cache instance
cache_manager = CacheManager()

# Example usage and testing
if __name__ == "__main__":
    # Test the cache manager
    cache = CacheManager(cache_dir="test_cache")
    
    # Test search cache
    test_results = [{'title': 'Test Result', 'url': 'https://example.com'}]
    cache.set_search_cache("test query", {'num_results': 10}, test_results)
    
    cached_results = cache.get_search_cache("test query", {'num_results': 10})
    print(f"Cache test: {'PASS' if cached_results == test_results else 'FAIL'}")
    
    # Print cache stats
    stats = cache.get_cache_stats()
    print(f"Cache stats: {stats}")
    
    # Cleanup test cache
    import shutil
    shutil.rmtree("test_cache", ignore_errors=True)