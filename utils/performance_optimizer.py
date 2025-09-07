"""
Performance Optimization Module for AI Research Agent
Provides speed improvements and efficient processing
"""

import time
import functools
import threading
import multiprocessing
from typing import List, Dict, Any, Callable
import concurrent.futures
import logging

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Optimizes performance across the application"""
    
    def __init__(self):
        self.max_workers = min(8, multiprocessing.cpu_count())
        self._cache = {}
        self._lock = threading.Lock()
    
    def time_function(self, func: Callable) -> Callable:
        """Decorator to time function execution"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
            return result
        return wrapper
    
    def parallel_map(self, func: Callable, items: List[Any], max_workers: int = None) -> List[Any]:
        """Execute function in parallel for faster processing"""
        if not items:
            return []
        
        if len(items) == 1:
            return [func(items[0])]
        
        max_workers = max_workers or min(self.max_workers, len(items))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, item) for item in items]
            results = []
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Parallel execution error: {str(e)}")
                    results.append(None)
            
            return [r for r in results if r is not None]
    
    def batch_process(self, func: Callable, items: List[Any], batch_size: int = 5) -> List[Any]:
        """Process items in batches for memory efficiency"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = self.parallel_map(func, batch)
            results.extend(batch_results)
            
            # Small delay to prevent overwhelming APIs
            time.sleep(0.1)
        
        return results
    
    def memoize(self, ttl_seconds: int = 300):
        """Decorator for function memoization with TTL"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                key = str(hash((str(args), str(sorted(kwargs.items())))))
                
                with self._lock:
                    # Check if cached result exists and is still valid
                    if key in self._cache:
                        result, timestamp = self._cache[key]
                        if time.time() - timestamp < ttl_seconds:
                            return result
                        else:
                            del self._cache[key]
                    
                    # Execute function and cache result
                    result = func(*args, **kwargs)
                    self._cache[key] = (result, time.time())
                    return result
            
            return wrapper
        return decorator
    
    def optimize_search_results(self, results: List[Dict]) -> List[Dict]:
        """Optimize search results for faster processing"""
        if not results:
            return []
        
        # Remove duplicates efficiently
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        # Sort by relevance score if available
        try:
            unique_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        except:
            pass
        
        return unique_results
    
    def compress_content(self, content: str, max_length: int = 2000) -> str:
        """Compress content while preserving important information"""
        if len(content) <= max_length:
            return content
        
        # Smart truncation - preserve sentences
        sentences = content.split('. ')
        result = ""
        
        for sentence in sentences:
            if len(result) + len(sentence) + 2 <= max_length:
                result += sentence + ". "
            else:
                break
        
        return result.strip()
    
    def clear_cache(self):
        """Clear the performance cache"""
        with self._lock:
            self._cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        with self._lock:
            return {
                'cache_size': len(self._cache),
                'memory_usage': sum(len(str(v)) for v in self._cache.values())
            }

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

# Decorators for easy use
time_it = performance_optimizer.time_function
memoize = performance_optimizer.memoize

def fast_parallel_process(func: Callable, items: List[Any], max_workers: int = None) -> List[Any]:
    """Quick access to parallel processing"""
    return performance_optimizer.parallel_map(func, items, max_workers)

def optimize_for_speed(func: Callable) -> Callable:
    """Decorator that applies multiple speed optimizations"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Apply memoization for frequently called functions
        if hasattr(func, '_memoized'):
            return func(*args, **kwargs)
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        if end_time - start_time > 1.0:  # Log slow functions
            logger.warning(f"{func.__name__} took {end_time - start_time:.2f}s - consider optimization")
        
        return result
    
    return wrapper


# Example usage and testing
if __name__ == "__main__":
    def sample_task(x):
        time.sleep(0.1)  # Simulate work
        return x * 2
    
    # Test parallel processing
    items = list(range(10))
    
    print("Testing performance optimizer...")
    start = time.time()
    results = fast_parallel_process(sample_task, items)
    end = time.time()
    
    print(f"Processed {len(items)} items in {end - start:.2f}s")
    print(f"Results: {results}")
    
    # Test cache stats
    stats = performance_optimizer.get_cache_stats()
    print(f"Cache stats: {stats}")