"""
Enhanced Image Module for AI Research Agent
Provides advanced image search, analysis, and visualization capabilities
"""

import requests
import json
import base64
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2

from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for optional dependencies
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("pytesseract not available - OCR features disabled")

class EnhancedImageProcessor:
    """Enhanced image processing with multiple APIs and analysis features"""
    
    def __init__(self):
        self.config = Config()
        self.image_sources = {
            'unsplash': getattr(self.config, 'UNSPLASH_ACCESS_KEY', None),
            'pixabay': getattr(self.config, 'PIXABAY_API_KEY', None),
            'serpapi': getattr(self.config, 'SERPAPI_API_KEY', None)
        }
        self.analysis_enabled = self._parse_bool_setting(getattr(self.config, 'IMAGE_ANALYSIS_ENABLED', 'true'))
        self.ocr_enabled = self._parse_bool_setting(getattr(self.config, 'OCR_ENABLED', 'true')) and OCR_AVAILABLE
    
    def _parse_bool_setting(self, value) -> bool:
        """Safely parse boolean settings that might be strings or booleans"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        else:
            return False
    
    def search_high_quality_images(self, query: str, count: int = 10, image_type: str = 'all') -> Dict:
        """Search for high-quality images from multiple sources"""
        try:
            all_images = []
            
            # Search Unsplash for professional photos
            if self.image_sources['unsplash']:
                unsplash_images = self._search_unsplash(query, count//2)
                all_images.extend(unsplash_images)
            
            # Search Pixabay for stock images
            if self.image_sources['pixabay']:
                pixabay_images = self._search_pixabay(query, count//2, image_type)
                all_images.extend(pixabay_images)
            
            # Search via SerpAPI for web images
            if self.image_sources['serpapi'] and len(all_images) < count:
                serpapi_images = self._search_serpapi_images(query, count - len(all_images))
                all_images.extend(serpapi_images)
            
            # Rank and filter images
            ranked_images = self._rank_images(all_images, query)
            
            return {
                'query': query,
                'total_found': len(ranked_images),
                'images': ranked_images[:count],
                'sources_used': [source for source, key in self.image_sources.items() if key],
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Image search failed: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def search_trend_images(self, trend_topic: str, time_period: str = 'year') -> Dict:
        """Search for images related to trending topics with temporal context"""
        try:
            # Enhanced query for trending topics
            trend_queries = [
                f"{trend_topic} {datetime.now().year}",
                f"{trend_topic} trends {time_period}",
                f"{trend_topic} analysis data visualization",
                f"{trend_topic} statistics charts graphs"
            ]
            
            all_trend_images = []
            
            for trend_query in trend_queries:
                images = self.search_high_quality_images(trend_query, 5, 'all')
                if images.get('success'):
                    # Add trend context to each image
                    for img in images['images']:
                        img['trend_context'] = trend_query
                        img['trend_relevance'] = self._calculate_trend_relevance(img, trend_topic)
                    all_trend_images.extend(images['images'])
            
            # Sort by trend relevance
            all_trend_images.sort(key=lambda x: x.get('trend_relevance', 0), reverse=True)
            
            return {
                'trend_topic': trend_topic,
                'time_period': time_period,
                'total_images': len(all_trend_images),
                'trend_images': all_trend_images[:15],  # Top 15 most relevant
                'search_queries_used': trend_queries,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Trend image search failed: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def analyze_image_content(self, image_url: str) -> Dict:
        """Analyze image content including OCR, objects, and context"""
        try:
            if not self.analysis_enabled:
                return {'error': 'Image analysis disabled', 'success': False}
            
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Load image
            image = Image.open(BytesIO(response.content))
            image_array = np.array(image)
            
            analysis_results = {
                'image_url': image_url,
                'basic_info': self._get_image_info(image),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            # OCR Analysis
            if self.ocr_enabled:
                ocr_results = self._extract_text_ocr(image_array)
                analysis_results['ocr'] = ocr_results
            
            # Color Analysis
            color_analysis = self._analyze_colors(image_array)
            analysis_results['colors'] = color_analysis
            
            # Quality Assessment
            quality_score = self._assess_image_quality(image_array)
            analysis_results['quality'] = quality_score
            
            # Object Detection (basic)
            objects = self._detect_basic_objects(image_array)
            analysis_results['objects'] = objects
            
            # Content Classification
            content_type = self._classify_content(image, analysis_results)
            analysis_results['content_classification'] = content_type
            
            analysis_results['success'] = True
            return analysis_results
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def create_image_collage(self, images: List[Dict], theme: str) -> Dict:
        """Create a collage from multiple images with trend theme"""
        try:
            if not images:
                return {'error': 'No images provided', 'success': False}
            
            # Download and process images
            processed_images = []
            for img in images[:9]:  # Max 9 images for 3x3 grid
                try:
                    response = requests.get(img['url'], timeout=20)
                    pil_img = Image.open(BytesIO(response.content))
                    
                    # Resize to standard size
                    pil_img = pil_img.resize((300, 300), Image.Resampling.LANCZOS)
                    processed_images.append(pil_img)
                except:
                    continue
            
            if not processed_images:
                return {'error': 'No images could be processed', 'success': False}
            
            # Calculate grid dimensions
            grid_size = int(np.ceil(np.sqrt(len(processed_images))))
            collage_width = grid_size * 300
            collage_height = grid_size * 300
            
            # Create collage
            collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
            
            for idx, img in enumerate(processed_images):
                row = idx // grid_size
                col = idx % grid_size
                x = col * 300
                y = row * 300
                collage.paste(img, (x, y))
            
            # Save to BytesIO
            collage_bytes = BytesIO()
            collage.save(collage_bytes, format='PNG', quality=95)
            collage_bytes.seek(0)
            
            # Convert to base64 for display
            collage_b64 = base64.b64encode(collage_bytes.getvalue()).decode()
            
            return {
                'theme': theme,
                'images_used': len(processed_images),
                'collage_size': f"{collage_width}x{collage_height}",
                'collage_b64': collage_b64,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Collage creation failed: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def _search_unsplash(self, query: str, count: int) -> List[Dict]:
        """Search Unsplash API for professional photos"""
        try:
            if not self.image_sources['unsplash']:
                return []
            
            headers = {'Authorization': f"Client-ID {self.image_sources['unsplash']}"}
            url = "https://api.unsplash.com/search/photos"
            
            params = {
                'query': query,
                'per_page': min(count, 30),
                'order_by': 'relevant',
                'orientation': 'landscape'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for item in data.get('results', []):
                image_data = {
                    'url': item['urls']['regular'],
                    'thumbnail': item['urls']['small'],
                    'title': item.get('alt_description', '') or item.get('description', ''),
                    'source': 'Unsplash',
                    'photographer': item['user']['name'],
                    'width': item['width'],
                    'height': item['height'],
                    'quality_score': 9,  # Unsplash photos are high quality
                    'download_url': item['links']['download'],
                    'tags': item.get('tags', [])
                }
                images.append(image_data)
            
            return images
            
        except Exception as e:
            logger.error(f"Unsplash search failed: {str(e)}")
            return []
    
    def _search_pixabay(self, query: str, count: int, image_type: str) -> List[Dict]:
        """Search Pixabay API for stock images"""
        try:
            if not self.image_sources['pixabay']:
                return []
            
            url = "https://pixabay.com/api/"
            
            params = {
                'key': self.image_sources['pixabay'],
                'q': query,
                'image_type': 'photo',
                'orientation': 'horizontal',
                'category': 'business,science,education',
                'min_width': 1920,
                'min_height': 1080,
                'per_page': min(count, 20),
                'safesearch': 'true'
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for item in data.get('hits', []):
                image_data = {
                    'url': item['webformatURL'],
                    'thumbnail': item['previewURL'],
                    'title': item.get('tags', ''),
                    'source': 'Pixabay',
                    'photographer': item.get('user', 'Pixabay'),
                    'width': item['imageWidth'],
                    'height': item['imageHeight'],
                    'quality_score': 7,  # Good quality stock images
                    'download_url': item['largeImageURL'],
                    'tags': item.get('tags', '').split(', ')
                }
                images.append(image_data)
            
            return images
            
        except Exception as e:
            logger.error(f"Pixabay search failed: {str(e)}")
            return []
    
    def _search_serpapi_images(self, query: str, count: int) -> List[Dict]:
        """Search Google Images via SerpAPI"""
        try:
            if not self.image_sources['serpapi']:
                return []
            
            url = "https://serpapi.com/search"
            
            params = {
                'engine': 'google_images',
                'q': query,
                'api_key': self.image_sources['serpapi'],
                'num': min(count, 20),
                'ijn': 0
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for item in data.get('images_results', []):
                image_data = {
                    'url': item.get('original', ''),
                    'thumbnail': item.get('thumbnail', ''),
                    'title': item.get('title', ''),
                    'source': 'Google Images',
                    'photographer': item.get('source', ''),
                    'width': 0,  # Not provided by SerpAPI
                    'height': 0,
                    'quality_score': 5,  # Variable quality from web
                    'download_url': item.get('original', ''),
                    'tags': []
                }
                if image_data['url']:
                    images.append(image_data)
            
            return images
            
        except Exception as e:
            logger.error(f"SerpAPI image search failed: {str(e)}")
            return []
    
    def _rank_images(self, images: List[Dict], query: str) -> List[Dict]:
        """Rank images by relevance and quality"""
        try:
            query_words = set(query.lower().split())
            
            for img in images:
                score = img.get('quality_score', 5)
                
                # Title relevance
                title_words = set(img.get('title', '').lower().split())
                title_matches = len(query_words.intersection(title_words))
                score += title_matches * 2
                
                # Tag relevance
                tag_words = set(' '.join(img.get('tags', [])).lower().split())
                tag_matches = len(query_words.intersection(tag_words))
                score += tag_matches * 1.5
                
                # Source quality bonus
                if img.get('source') == 'Unsplash':
                    score += 2
                elif img.get('source') == 'Pixabay':
                    score += 1
                
                # Size bonus (prefer larger images)
                if img.get('width', 0) > 1920:
                    score += 1
                
                img['relevance_score'] = score
            
            # Sort by relevance score
            images.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            return images
            
        except Exception as e:
            logger.error(f"Image ranking failed: {str(e)}")
            return images
    
    def _calculate_trend_relevance(self, image: Dict, trend_topic: str) -> float:
        """Calculate how relevant an image is to a trending topic"""
        try:
            relevance = 0.0
            trend_words = set(trend_topic.lower().split())
            
            # Check title relevance
            title_words = set(image.get('title', '').lower().split())
            title_overlap = len(trend_words.intersection(title_words))
            relevance += title_overlap * 0.3
            
            # Check tag relevance
            tag_words = set(' '.join(image.get('tags', [])).lower().split())
            tag_overlap = len(trend_words.intersection(tag_words))
            relevance += tag_overlap * 0.2
            
            # Quality bonus
            relevance += image.get('quality_score', 5) * 0.1
            
            # Source reliability bonus
            if image.get('source') in ['Unsplash', 'Pixabay']:
                relevance += 0.5
            
            return relevance
            
        except Exception as e:
            logger.error(f"Trend relevance calculation failed: {str(e)}")
            return 0.0
    
    def _get_image_info(self, image: Image.Image) -> Dict:
        """Get basic image information"""
        return {
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'format': image.format,
            'size_bytes': len(image.tobytes()) if hasattr(image, 'tobytes') else 0
        }
    
    def _extract_text_ocr(self, image_array: np.ndarray) -> Dict:
        """Extract text from image using OCR"""
        try:
            if not OCR_AVAILABLE:
                return {
                    "text": "",
                    "confidence": 0,
                    "word_count": 0,
                    "has_text": False,
                    "error": "OCR not available - pytesseract not installed",
                    "method": "none"
                }
            
            # Convert to grayscale for better OCR
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Apply image preprocessing for better OCR
            processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Extract text
            text = pytesseract.image_to_string(processed, lang='eng')
            
            # Get detailed data
            data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            words = [word for word in text.split() if word.strip()]
            
            return {
                "text": text.strip(),
                "confidence": round(avg_confidence, 2),
                "word_count": len(words),
                "has_text": len(words) > 0,
                "method": "pytesseract",
                "languages_detected": ["eng"]  # Could be expanded
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return {
                "text": "",
                "confidence": 0,
                "word_count": 0,
                "has_text": False,
                "error": str(e),
                "method": "failed"
            }
    
    def _analyze_colors(self, image_array: np.ndarray) -> Dict:
        """Analyze color composition of image"""
        try:
            # Convert to RGB if needed
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                rgb_image = image_array
            else:
                rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            
            # Calculate dominant colors
            pixels = rgb_image.reshape(-1, 3)
            
            # Simple color analysis
            avg_color = np.mean(pixels, axis=0)
            brightness = np.mean(avg_color)
            
            # Color distribution
            red_avg = np.mean(pixels[:, 0])
            green_avg = np.mean(pixels[:, 1])
            blue_avg = np.mean(pixels[:, 2])
            
            return {
                'average_color': [int(avg_color[0]), int(avg_color[1]), int(avg_color[2])],
                'brightness': round(brightness, 2),
                'red_component': round(red_avg, 2),
                'green_component': round(green_avg, 2),
                'blue_component': round(blue_avg, 2),
                'dominant_tone': 'warm' if red_avg > blue_avg else 'cool'
            }
            
        except Exception as e:
            logger.error(f"Color analysis failed: {str(e)}")
            return {'error': str(e)}
    
    def _assess_image_quality(self, image_array: np.ndarray) -> Dict:
        """Assess image quality metrics"""
        try:
            # Convert to grayscale for analysis
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Calculate sharpness (using Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            
            # Calculate contrast
            contrast = gray.std()
            
            # Calculate brightness
            brightness = gray.mean()
            
            # Quality score (0-10)
            quality_score = min(10, (sharpness / 1000 + contrast / 50 + brightness / 50) / 3 * 10)
            
            return {
                'sharpness': round(sharpness, 2),
                'contrast': round(contrast, 2),
                'brightness': round(brightness, 2),
                'quality_score': round(quality_score, 1),
                'assessment': 'High' if quality_score > 7 else 'Medium' if quality_score > 4 else 'Low'
            }
            
        except Exception as e:
            logger.error(f"Quality assessment failed: {str(e)}")
            return {'error': str(e)}
    
    def _detect_basic_objects(self, image_array: np.ndarray) -> Dict:
        """Basic object detection using simple methods"""
        try:
            # Simple edge detection for object counting
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter significant contours
            significant_contours = [c for c in contours if cv2.contourArea(c) > 1000]
            
            return {
                'total_contours': len(contours),
                'significant_objects': len(significant_contours),
                'has_multiple_objects': len(significant_contours) > 1,
                'complexity': 'High' if len(significant_contours) > 10 else 'Medium' if len(significant_contours) > 3 else 'Low'
            }
            
        except Exception as e:
            logger.error(f"Object detection failed: {str(e)}")
            return {'error': str(e)}
    
    def _classify_content(self, image: Image.Image, analysis: Dict) -> Dict:
        """Classify image content type"""
        try:
            # Simple classification based on analysis
            content_type = 'general'
            confidence = 0.5
            
            # Check OCR results for charts/data
            ocr_text = analysis.get('ocr', {}).get('text', '').lower()
            if any(word in ocr_text for word in ['chart', 'graph', 'data', 'trend', '%', 'analysis']):
                content_type = 'data_visualization'
                confidence = 0.8
            
            # Check for business/professional content
            elif any(word in ocr_text for word in ['business', 'market', 'finance', 'report']):
                content_type = 'business'
                confidence = 0.7
            
            # Check image properties
            quality = analysis.get('quality', {})
            if quality.get('quality_score', 0) > 8:
                if content_type == 'general':
                    content_type = 'professional'
                    confidence = 0.6
            
            return {
                'type': content_type,
                'confidence': confidence,
                'suitable_for_trends': content_type in ['data_visualization', 'business', 'professional']
            }
            
        except Exception as e:
            logger.error(f"Content classification failed: {str(e)}")
            return {'type': 'unknown', 'confidence': 0, 'error': str(e)}

# Example usage
if __name__ == "__main__":
    processor = EnhancedImageProcessor()
    
    # Test image search
    results = processor.search_high_quality_images("AI trends 2024", 5)
    if results.get('success'):
        print(f"Found {results['total_found']} images")
        for img in results['images'][:2]:
            print(f"- {img['title']} from {img['source']}")