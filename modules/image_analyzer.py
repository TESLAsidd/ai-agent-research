"""
Image Analysis Module for AI Research Agent
Handles image processing, OCR, and visual content analysis
"""

import requests
import base64
import io
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from openai import OpenAI

# Optional OCR import with graceful fallback
try:
    import pytesseract
    import cv2
    OCR_AVAILABLE = True
except ImportError as e:
    OCR_AVAILABLE = False
    pytesseract = None
    cv2 = None
    print(f"Warning: OCR features not available - {e}")

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

class ImageAnalyzer:
    """Advanced image analysis and OCR capabilities"""
    
    def __init__(self):
        self.config = Config()
        if self.config.OPENAI_API_KEY:
            self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        else:
            self.client = None
            logger.warning("OpenAI API key not found. AI image analysis will be limited.")
    
    def analyze_image(self, image_url: str, query_context: str = "") -> Dict:
        """
        Comprehensive image analysis including OCR and AI description
        
        Args:
            image_url: URL of the image to analyze
            query_context: Context from the research query for better analysis
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Check cache first
            if CACHE_AVAILABLE:
                cache_key = f"{image_url}_{query_context}"
                cached_result = cache_manager.get_content_cache(cache_key)
                if cached_result:
                    logger.info(f"Using cached image analysis for: {image_url[:50]}...")
                    return cached_result
            
            # Download and process image
            image_data = self._download_image(image_url)
            if not image_data:
                return {"error": "Failed to download image"}
            
            analysis_result = {
                "image_url": image_url,
                "analysis_timestamp": datetime.now().isoformat(),
                "file_size_bytes": len(image_data),
                "success": True
            }
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_data))
            analysis_result["dimensions"] = {
                "width": pil_image.width,
                "height": pil_image.height,
                "format": pil_image.format,
                "mode": pil_image.mode
            }
            
            # Perform OCR
            ocr_result = self._extract_text_ocr(pil_image)
            analysis_result["ocr"] = ocr_result
            
            # AI-powered image description
            if self.client:
                ai_description = self._get_ai_image_description(image_data, query_context)
                analysis_result["ai_description"] = ai_description
            
            # Image quality assessment
            quality_assessment = self._assess_image_quality(pil_image)
            analysis_result["quality"] = quality_assessment
            
            # Extract visual features
            visual_features = self._extract_visual_features(pil_image)
            analysis_result["visual_features"] = visual_features
            
            # Cache the result
            if CACHE_AVAILABLE:
                cache_key = f"{image_url}_{query_context}"
                cache_manager.set_content_cache(cache_key, analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Image analysis failed for {image_url}: {str(e)}")
            return {
                "error": f"Image analysis failed: {str(e)}",
                "image_url": image_url,
                "analysis_timestamp": datetime.now().isoformat(),
                "success": False
            }
    
    def _download_image(self, image_url: str, max_size_mb: int = 10) -> Optional[bytes]:
        """Download image with size and format validation"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(image_url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()
            
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                logger.warning(f"Image too large: {int(content_length) / (1024*1024):.1f} MB")
                return None
            
            # Download with size limit
            image_data = b""
            max_bytes = max_size_mb * 1024 * 1024
            
            for chunk in response.iter_content(chunk_size=8192):
                if len(image_data) + len(chunk) > max_bytes:
                    logger.warning("Image download size limit exceeded")
                    return None
                image_data += chunk
            
            # Validate image format
            try:
                Image.open(io.BytesIO(image_data))
                return image_data
            except Exception:
                logger.warning("Invalid image format")
                return None
                
        except Exception as e:
            logger.error(f"Failed to download image: {str(e)}")
            return None
    
    def _extract_text_ocr(self, pil_image: Image.Image) -> Dict:
        """Extract text from image using OCR with graceful fallback"""
        if not OCR_AVAILABLE:
            return {
                "text": "",
                "confidence": 0,
                "word_count": 0,
                "has_text": False,
                "error": "OCR not available - pytesseract or cv2 not installed",
                "method": "none"
            }
        
        try:
            # Check if Tesseract is actually available
            try:
                pytesseract.get_tesseract_version()
            except Exception:
                return {
                    "text": "",
                    "confidence": 0,
                    "word_count": 0,
                    "has_text": False,
                    "error": "Tesseract OCR not installed on system",
                    "method": "tesseract_missing"
                }
            
            # Convert to RGB if needed
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Enhance image for better OCR
            enhanced_image = self._enhance_for_ocr(pil_image)
            
            # Perform OCR with different configurations
            ocr_configs = [
                '--psm 3',  # Default
                '--psm 6',  # Uniform block of text
                '--psm 8',  # Single word
                '--psm 13', # Raw line
            ]
            
            best_text = ""
            best_confidence = 0
            
            for config in ocr_configs:
                try:
                    # Extract text with confidence scores
                    data = pytesseract.image_to_data(enhanced_image, config=config, output_type=pytesseract.Output.DICT)
                    
                    # Filter out low confidence text
                    confidences = [int(conf) for conf in data['conf'] if int(conf) > 30]
                    texts = [data['text'][i] for i, conf in enumerate(data['conf']) if int(conf) > 30 and data['text'][i].strip()]
                    
                    if confidences and texts:
                        avg_confidence = sum(confidences) / len(confidences)
                        extracted_text = ' '.join(texts)
                        
                        if avg_confidence > best_confidence and len(extracted_text) > len(best_text):
                            best_confidence = avg_confidence
                            best_text = extracted_text
                            
                except Exception as e:
                    logger.debug(f"OCR config {config} failed: {str(e)}")
                    continue
            
            return {
                "text": best_text.strip(),
                "confidence": best_confidence,
                "word_count": len(best_text.split()) if best_text else 0,
                "has_text": bool(best_text.strip()),
                "method": "tesseract"
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return {
                "text": "",
                "confidence": 0,
                "word_count": 0,
                "has_text": False,
                "error": f"OCR failed: {str(e)}",
                "method": "tesseract_error"
            }
    
    def _enhance_for_ocr(self, pil_image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR results"""
        try:
            # Convert to grayscale
            if pil_image.mode != 'L':
                pil_image = pil_image.convert('L')
            
            # Resize if too small (improve OCR accuracy)
            if pil_image.width < 300 or pil_image.height < 300:
                scale_factor = max(300 / pil_image.width, 300 / pil_image.height)
                new_size = (int(pil_image.width * scale_factor), int(pil_image.height * scale_factor))
                pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.5)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(1.2)
            
            # Apply slight denoising
            pil_image = pil_image.filter(ImageFilter.MedianFilter(size=3))
            
            return pil_image
            
        except Exception as e:
            logger.warning(f"Image enhancement failed: {str(e)}")
            return pil_image
    
    def _get_ai_image_description(self, image_data: bytes, query_context: str = "") -> Dict:
        """Get AI-powered image description using OpenAI Vision API"""
        try:
            if not self.client:
                return {"error": "OpenAI API not configured"}
            
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Create prompt with context
            prompt = f"""Analyze this image in the context of a research query about: "{query_context}"

Please provide:
1. A detailed description of what you see in the image
2. Any text or data visible in the image
3. Relevance to the research topic
4. Key visual elements (charts, graphs, diagrams, people, objects)
5. Overall quality and clarity of the image

Be specific and detailed in your analysis."""
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            description = response.choices[0].message.content
            
            return {
                "description": description,
                "model": "gpt-4-vision-preview",
                "success": True,
                "relevance_score": self._calculate_relevance_score(description, query_context)
            }
            
        except Exception as e:
            logger.error(f"AI image description failed: {str(e)}")
            return {
                "error": f"AI description failed: {str(e)}",
                "success": False
            }
    
    def _assess_image_quality(self, pil_image: Image.Image) -> Dict:
        """Assess image quality metrics with graceful fallback"""
        try:
            # Basic quality metrics that don't require cv2
            quality_metrics = {
                "resolution": pil_image.width * pil_image.height,
                "aspect_ratio": pil_image.width / pil_image.height,
                "file_format": pil_image.format
            }
            
            if not OCR_AVAILABLE or cv2 is None:
                # Fallback quality assessment without cv2
                img_array = np.array(pil_image.convert('L'))  # Grayscale
                quality_metrics["brightness"] = float(np.mean(img_array))
                quality_metrics["contrast"] = float(np.std(img_array))
                
                # Simple quality score based on resolution and contrast
                quality_score = min(100, max(0, 
                    (min(quality_metrics["resolution"] / 1000000, 1) * 50) +  # Resolution contributes 50%
                    (min(quality_metrics["contrast"] / 50, 1) * 50)  # Contrast contributes 50%
                ))
                
                quality_metrics["overall_score"] = round(quality_score, 1)
                quality_metrics["quality_rating"] = self._get_quality_rating(quality_score)
                quality_metrics["method"] = "basic"
                
                return quality_metrics
            
            # Advanced quality assessment with cv2
            img_array = np.array(pil_image.convert('RGB'))
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Calculate blur metric (Laplacian variance)
            blur_metric = cv2.Laplacian(gray, cv2.CV_64F).var()
            quality_metrics["blur_score"] = float(blur_metric)
            quality_metrics["is_blurry"] = blur_metric < 100
            
            # Calculate brightness and contrast
            quality_metrics["brightness"] = float(np.mean(gray))
            quality_metrics["contrast"] = float(np.std(gray))
            
            # Overall quality score (0-100)
            quality_score = min(100, max(0, 
                (blur_metric / 500 * 40) +  # Blur contributes 40%
                (min(quality_metrics["contrast"] / 50, 1) * 30) +  # Contrast contributes 30%
                (min(quality_metrics["resolution"] / 1000000, 1) * 30)  # Resolution contributes 30%
            ))
            
            quality_metrics["overall_score"] = round(quality_score, 1)
            quality_metrics["quality_rating"] = self._get_quality_rating(quality_score)
            quality_metrics["method"] = "advanced"
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Quality assessment failed: {str(e)}")
            return {
                "error": f"Quality assessment failed: {str(e)}",
                "overall_score": 0,
                "quality_rating": "unknown",
                "method": "error"
            }
    
    def _extract_visual_features(self, pil_image: Image.Image) -> Dict:
        """Extract visual features from the image with graceful fallback"""
        try:
            # Convert to RGB
            img_rgb = pil_image.convert('RGB')
            img_array = np.array(img_rgb)
            
            # Basic color analysis without advanced dependencies
            colors = {
                "dominant_colors": self._get_dominant_colors_basic(img_array),
                "color_diversity": self._calculate_color_diversity_basic(img_array),
                "is_grayscale": self._is_grayscale(img_array)
            }
            
            # Basic chart/text detection
            contains_chart = False
            text_regions = {"text_area_ratio": 0, "detected": False}
            
            if OCR_AVAILABLE and cv2 is not None:
                # Advanced detection if cv2 is available
                contains_chart = self._detect_chart_elements(img_array)
                text_regions = self._detect_text_regions(img_array)
            
            return {
                "colors": colors,
                "contains_chart": contains_chart,
                "text_regions": text_regions,
                "has_complex_content": contains_chart or text_regions["text_area_ratio"] > 0.1,
                "method": "advanced" if OCR_AVAILABLE and cv2 is not None else "basic"
            }
            
        except Exception as e:
            logger.error(f"Visual feature extraction failed: {str(e)}")
            return {"error": str(e), "method": "error"}
    
    def _get_dominant_colors_basic(self, img_array: np.ndarray) -> List[Dict]:
        """Get dominant colors using basic numpy operations"""
        try:
            # Reshape image to be a list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Sample pixels to reduce computation
            if len(pixels) > 10000:
                indices = np.random.choice(len(pixels), 10000, replace=False)
                pixels = pixels[indices]
            
            # Simple histogram-based approach
            colors = []
            
            # Calculate mean color
            mean_color = np.mean(pixels, axis=0)
            colors.append({
                "rgb": [int(c) for c in mean_color],
                "hex": f"#{int(mean_color[0]):02x}{int(mean_color[1]):02x}{int(mean_color[2]):02x}",
                "percentage": 100.0,
                "method": "mean"
            })
            
            return colors
            
        except Exception as e:
            logger.debug(f"Basic dominant color extraction failed: {str(e)}")
            return []
    
    def _calculate_color_diversity_basic(self, img_array: np.ndarray) -> float:
        """Calculate basic color diversity score"""
        try:
            # Calculate standard deviation of each color channel
            std_r = np.std(img_array[:, :, 0])
            std_g = np.std(img_array[:, :, 1]) 
            std_b = np.std(img_array[:, :, 2])
            
            # Average standard deviation as diversity measure
            diversity = (std_r + std_g + std_b) / 3
            
            # Normalize to 0-100 scale
            return min(100.0, diversity / 128 * 100)
            
        except Exception as e:
            logger.debug(f"Basic color diversity calculation failed: {str(e)}")
            return 0.0
            
            # Calculate entropy (measure of color diversity)
            def entropy(hist):
                hist = hist[hist > 0]  # Remove zeros
                hist = hist / hist.sum()  # Normalize
                return -np.sum(hist * np.log2(hist))
            
            avg_entropy = (entropy(hist_r) + entropy(hist_g) + entropy(hist_b)) / 3
            return float(avg_entropy / 8)  # Normalize to 0-1
            
        except Exception:
            return 0.0
    
    def _is_grayscale(self, img_array: np.ndarray) -> bool:
        """Check if image is effectively grayscale"""
        try:
            # Calculate color variance
            r_var = np.var(img_array[:, :, 0])
            g_var = np.var(img_array[:, :, 1])
            b_var = np.var(img_array[:, :, 2])
            
            # Check if color channels are similar
            total_var = r_var + g_var + b_var
            return total_var < 1000  # Threshold for grayscale detection
            
        except Exception:
            return False
    
    def _detect_chart_elements(self, img_array: np.ndarray) -> bool:
        """Detect if image contains charts or graphs"""
        try:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Detect lines (common in charts)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            # Detect circles (common in pie charts)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
            
            # Simple heuristic: if many lines or circles detected, likely a chart
            has_lines = lines is not None and len(lines) > 10
            has_circles = circles is not None and len(circles[0]) > 0
            
            return has_lines or has_circles
            
        except Exception:
            return False
    
    def _detect_text_regions(self, img_array: np.ndarray) -> Dict:
        """Detect text regions in the image"""
        try:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Use MSER to detect text regions
            mser = cv2.MSER_create()
            regions, _ = mser.detectRegions(gray)
            
            total_area = img_array.shape[0] * img_array.shape[1]
            text_area = sum(len(region) for region in regions)
            
            return {
                "text_regions_count": len(regions),
                "text_area_ratio": text_area / total_area,
                "has_significant_text": text_area / total_area > 0.05
            }
            
        except Exception:
            return {
                "text_regions_count": 0,
                "text_area_ratio": 0.0,
                "has_significant_text": False
            }
    
    def _calculate_relevance_score(self, description: str, query_context: str) -> float:
        """Calculate relevance score based on description and query context"""
        try:
            if not query_context or not description:
                return 0.0
            
            # Simple keyword matching approach
            query_words = set(query_context.lower().split())
            description_words = set(description.lower().split())
            
            # Calculate Jaccard similarity
            intersection = len(query_words.intersection(description_words))
            union = len(query_words.union(description_words))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception:
            return 0.0
    
    def _get_quality_rating(self, score: float) -> str:
        """Convert quality score to rating"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        elif score >= 20:
            return "poor"
        else:
            return "very_poor"

    def analyze_multiple_images(self, image_urls: List[str], query_context: str = "") -> List[Dict]:
        """Analyze multiple images efficiently"""
        results = []
        
        for url in image_urls:
            try:
                result = self.analyze_image(url, query_context)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze image {url}: {str(e)}")
                results.append({
                    "error": str(e),
                    "image_url": url,
                    "success": False
                })
        
        return results


# Example usage and testing
if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    
    # Test with a sample image URL
    test_url = "https://via.placeholder.com/800x600/0000FF/FFFFFF?text=Sample+Chart"
    
    print("Testing image analysis...")
    result = analyzer.analyze_image(test_url, "data visualization chart")
    
    if result.get("success"):
        print(f"✅ Analysis successful!")
        print(f"Dimensions: {result['dimensions']}")
        print(f"OCR Text: {result['ocr']['text'][:100]}...")
        print(f"Quality Score: {result['quality']['overall_score']}")
        if "ai_description" in result:
            print(f"AI Description: {result['ai_description']['description'][:100]}...")
    else:
        print(f"❌ Analysis failed: {result.get('error')}")