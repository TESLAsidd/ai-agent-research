"""
Citation Management Module for AI Research Agent
Handles citation formatting, tracking, and validation
"""

import re
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class CitationManager:
    """Manages citations and source tracking"""
    
    def __init__(self):
        self.citation_styles = ['APA', 'MLA', 'Chicago', 'Harvard', 'IEEE']
        self.citation_counter = 0
    
    def create_citation(self, source_data: Dict) -> Dict:
        """
        Create a comprehensive citation from source data
        
        Args:
            source_data: Dictionary containing source information
            
        Returns:
            Dictionary with formatted citations in multiple styles
        """
        self.citation_counter += 1
        
        citation = {
            'id': self.citation_counter,
            'title': source_data.get('title', 'Untitled'),
            'url': source_data.get('url', ''),
            'domain': source_data.get('domain', ''),
            'author': source_data.get('author', ''),
            'publish_date': source_data.get('publish_date', ''),
            'access_date': datetime.now().strftime('%Y-%m-%d'),
            'word_count': source_data.get('word_count', 0),
            'extraction_method': source_data.get('extraction_method', ''),
            'content_score': source_data.get('content_score', 0)
        }
        
        # Generate citations in different styles
        citation['formatted_citations'] = {
            'APA': self._format_apa_citation(citation),
            'MLA': self._format_mla_citation(citation),
            'Chicago': self._format_chicago_citation(citation),
            'Harvard': self._format_harvard_citation(citation),
            'IEEE': self._format_ieee_citation(citation)
        }
        
        return citation
    
    def _format_apa_citation(self, citation: Dict) -> str:
        """Format citation in APA style"""
        parts = []
        
        # Author
        if citation['author']:
            parts.append(f"{citation['author']}.")
        
        # Date
        date_str = self._format_date_apa(citation['publish_date'])
        if date_str:
            parts.append(f"({date_str}).")
        
        # Title
        title = citation['title']
        if title and title != 'Untitled':
            parts.append(f"{title}.")
        
        # Source
        domain = citation['domain']
        if domain:
            parts.append(f"{domain}.")
        
        # URL
        url = citation['url']
        if url:
            parts.append(f"Retrieved {citation['access_date']} from {url}")
        
        return " ".join(parts)
    
    def _format_mla_citation(self, citation: Dict) -> str:
        """Format citation in MLA style"""
        parts = []
        
        # Author
        if citation['author']:
            parts.append(f"{citation['author']}.")
        
        # Title
        title = citation['title']
        if title and title != 'Untitled':
            parts.append(f'"{title}."')
        
        # Source
        domain = citation['domain']
        if domain:
            parts.append(f"{domain},")
        
        # Date
        date_str = self._format_date_mla(citation['publish_date'])
        if date_str:
            parts.append(f"{date_str},")
        
        # URL
        url = citation['url']
        if url:
            parts.append(f"{url}.")
        
        return " ".join(parts)
    
    def _format_chicago_citation(self, citation: Dict) -> str:
        """Format citation in Chicago style"""
        parts = []
        
        # Author
        if citation['author']:
            parts.append(f"{citation['author']},")
        
        # Title
        title = citation['title']
        if title and title != 'Untitled':
            parts.append(f'"{title},"')
        
        # Source
        domain = citation['domain']
        if domain:
            parts.append(f"{domain},")
        
        # Date
        date_str = self._format_date_chicago(citation['publish_date'])
        if date_str:
            parts.append(f"{date_str},")
        
        # URL
        url = citation['url']
        if url:
            parts.append(f"{url}.")
        
        return " ".join(parts)
    
    def _format_harvard_citation(self, citation: Dict) -> str:
        """Format citation in Harvard style"""
        parts = []
        
        # Author
        if citation['author']:
            parts.append(f"{citation['author']}")
        
        # Date
        date_str = self._format_date_harvard(citation['publish_date'])
        if date_str:
            parts.append(f"{date_str}")
        
        # Title
        title = citation['title']
        if title and title != 'Untitled':
            parts.append(f"{title}.")
        
        # Source
        domain = citation['domain']
        if domain:
            parts.append(f"[Online] Available at: {domain}")
        
        # URL
        url = citation['url']
        if url:
            parts.append(f"[Accessed {citation['access_date']}]")
        
        return ". ".join(parts)
    
    def _format_ieee_citation(self, citation: Dict) -> str:
        """Format citation in IEEE style"""
        parts = []
        
        # Author
        if citation['author']:
            parts.append(f"{citation['author']}")
        
        # Title
        title = citation['title']
        if title and title != 'Untitled':
            parts.append(f'"{title},"')
        
        # Source
        domain = citation['domain']
        if domain:
            parts.append(f"{domain}")
        
        # Date
        date_str = self._format_date_ieee(citation['publish_date'])
        if date_str:
            parts.append(f"{date_str}")
        
        # URL
        url = citation['url']
        if url:
            parts.append(f"[Online]. Available: {url}")
        
        return " ".join(parts)
    
    def _format_date_apa(self, date_str: str) -> str:
        """Format date for APA style"""
        if not date_str:
            return "n.d."
        
        try:
            # Try to parse various date formats
            if len(date_str) >= 4:
                year = date_str[:4]
                return year
            return "n.d."
        except:
            return "n.d."
    
    def _format_date_mla(self, date_str: str) -> str:
        """Format date for MLA style"""
        if not date_str:
            return "n.d."
        
        try:
            if len(date_str) >= 4:
                year = date_str[:4]
                return year
            return "n.d."
        except:
            return "n.d."
    
    def _format_date_chicago(self, date_str: str) -> str:
        """Format date for Chicago style"""
        if not date_str:
            return "n.d."
        
        try:
            if len(date_str) >= 4:
                year = date_str[:4]
                return year
            return "n.d."
        except:
            return "n.d."
    
    def _format_date_harvard(self, date_str: str) -> str:
        """Format date for Harvard style"""
        if not date_str:
            return "n.d."
        
        try:
            if len(date_str) >= 4:
                year = date_str[:4]
                return f"({year})"
            return "(n.d.)"
        except:
            return "(n.d.)"
    
    def _format_date_ieee(self, date_str: str) -> str:
        """Format date for IEEE style"""
        if not date_str:
            return "n.d."
        
        try:
            if len(date_str) >= 4:
                year = date_str[:4]
                return year
            return "n.d."
        except:
            return "n.d."
    
    def validate_citation(self, citation: Dict) -> Dict:
        """
        Validate citation completeness and quality
        
        Args:
            citation: Citation dictionary to validate
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'is_valid': True,
            'completeness_score': 0,
            'quality_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        # Check completeness
        required_fields = ['title', 'url', 'domain']
        optional_fields = ['author', 'publish_date']
        
        completeness_score = 0
        for field in required_fields:
            if citation.get(field):
                completeness_score += 1
            else:
                validation['issues'].append(f"Missing required field: {field}")
        
        for field in optional_fields:
            if citation.get(field):
                completeness_score += 0.5
        
        validation['completeness_score'] = completeness_score / len(required_fields + optional_fields)
        
        # Check quality
        quality_score = 0
        
        # Title quality
        title = citation.get('title', '')
        if title and title != 'Untitled' and len(title) > 10:
            quality_score += 1
        else:
            validation['issues'].append("Title is missing or too short")
        
        # URL quality
        url = citation.get('url', '')
        if url and self._is_valid_url(url):
            quality_score += 1
        else:
            validation['issues'].append("Invalid or missing URL")
        
        # Domain quality
        domain = citation.get('domain', '')
        if domain and len(domain) > 3:
            quality_score += 1
        else:
            validation['issues'].append("Invalid or missing domain")
        
        # Author quality
        author = citation.get('author', '')
        if author and len(author) > 2:
            quality_score += 0.5
        
        # Date quality
        publish_date = citation.get('publish_date', '')
        if publish_date and len(publish_date) >= 4:
            quality_score += 0.5
        
        validation['quality_score'] = quality_score / 4
        
        # Overall validation
        if validation['completeness_score'] < 0.5 or validation['quality_score'] < 0.5:
            validation['is_valid'] = False
        
        # Recommendations
        if validation['completeness_score'] < 0.8:
            validation['recommendations'].append("Improve citation completeness")
        
        if validation['quality_score'] < 0.8:
            validation['recommendations'].append("Improve citation quality")
        
        return validation
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def generate_citation_report(self, citations: List[Dict]) -> Dict:
        """
        Generate a comprehensive citation report
        
        Args:
            citations: List of citation dictionaries
            
        Returns:
            Dictionary with citation statistics and analysis
        """
        if not citations:
            return {'error': 'No citations to analyze'}
        
        report = {
            'total_citations': len(citations),
            'citation_statistics': {},
            'domain_analysis': {},
            'quality_analysis': {},
            'style_comparison': {},
            'recommendations': []
        }
        
        # Citation statistics
        valid_citations = 0
        total_completeness = 0
        total_quality = 0
        
        for citation in citations:
            validation = self.validate_citation(citation)
            if validation['is_valid']:
                valid_citations += 1
            
            total_completeness += validation['completeness_score']
            total_quality += validation['quality_score']
        
        report['citation_statistics'] = {
            'valid_citations': valid_citations,
            'invalid_citations': len(citations) - valid_citations,
            'average_completeness': total_completeness / len(citations),
            'average_quality': total_quality / len(citations)
        }
        
        # Domain analysis
        domains = [citation.get('domain', '') for citation in citations]
        domain_counts = {}
        for domain in domains:
            if domain:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        report['domain_analysis'] = {
            'unique_domains': len(domain_counts),
            'most_common_domains': sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'domain_distribution': domain_counts
        }
        
        # Quality analysis
        quality_issues = []
        for citation in citations:
            validation = self.validate_citation(citation)
            quality_issues.extend(validation['issues'])
        
        issue_counts = {}
        for issue in quality_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        report['quality_analysis'] = {
            'common_issues': sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'total_issues': len(quality_issues)
        }
        
        # Style comparison
        style_counts = {}
        for citation in citations:
            formatted_citations = citation.get('formatted_citations', {})
            for style, formatted_citation in formatted_citations.items():
                if formatted_citation:
                    style_counts[style] = style_counts.get(style, 0) + 1
        
        report['style_comparison'] = style_counts
        
        # Recommendations
        if report['citation_statistics']['average_completeness'] < 0.8:
            report['recommendations'].append("Improve citation completeness by ensuring all required fields are present")
        
        if report['citation_statistics']['average_quality'] < 0.8:
            report['recommendations'].append("Improve citation quality by validating URLs and ensuring proper formatting")
        
        if report['domain_analysis']['unique_domains'] < len(citations) * 0.5:
            report['recommendations'].append("Increase source diversity by using more unique domains")
        
        return report


# Example usage and testing
if __name__ == "__main__":
    # Test citation manager
    manager = CitationManager()
    
    # Sample source data
    sample_source = {
        'title': 'AI Breakthroughs in 2024',
        'url': 'https://example.com/ai-breakthroughs',
        'domain': 'example.com',
        'author': 'John Doe',
        'publish_date': '2024-01-15',
        'word_count': 1000,
        'extraction_method': 'newspaper3k',
        'content_score': 8
    }
    
    # Create citation
    citation = manager.create_citation(sample_source)
    print("Generated Citation:")
    print(f"ID: {citation['id']}")
    print(f"APA: {citation['formatted_citations']['APA']}")
    print(f"MLA: {citation['formatted_citations']['MLA']}")
    
    # Validate citation
    validation = manager.validate_citation(citation)
    print(f"\nValidation Results:")
    print(f"Valid: {validation['is_valid']}")
    print(f"Completeness Score: {validation['completeness_score']:.2f}")
    print(f"Quality Score: {validation['quality_score']:.2f}")
    
    # Generate report
    report = manager.generate_citation_report([citation])
    print(f"\nCitation Report:")
    print(f"Total Citations: {report['total_citations']}")
    print(f"Valid Citations: {report['citation_statistics']['valid_citations']}")
    print(f"Average Quality: {report['citation_statistics']['average_quality']:.2f}")
