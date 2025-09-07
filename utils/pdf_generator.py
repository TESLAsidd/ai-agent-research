"""
PDF Generation Utility for AI Research Agent
Handles PDF report generation with proper formatting
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List
import os

class PDFGenerator:
    """Generate PDF reports from research data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f77b4')
        ))
        
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#34495e')
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Citation style
        self.styles.add(ParagraphStyle(
            name='Citation',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            rightIndent=20,
            textColor=colors.HexColor('#666666')
        ))
    
    def generate_pdf(self, results: Dict) -> bytes:
        """
        Generate PDF and return as bytes for Streamlit download
        
        Args:
            results: Research results dictionary
            
        Returns:
            PDF file content as bytes
        """
        import tempfile
        import os
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                temp_path = tmp_file.name
            
            # Generate PDF
            self.generate_research_report(results, temp_path)
            
            # Read PDF content as bytes
            with open(temp_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return pdf_content
            
        except Exception as e:
            # Clean up on error
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def generate_research_report(self, results: Dict, output_path: str) -> str:
        """
        Generate a comprehensive PDF research report
        
        Args:
            results: Research results dictionary
            output_path: Path to save the PDF file
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Title page
            story.extend(self._create_title_page(results))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self._create_executive_summary(results))
            story.append(PageBreak())
            
            # Key findings
            story.extend(self._create_key_findings(results))
            story.append(PageBreak())
            
            # Detailed analysis
            story.extend(self._create_detailed_analysis(results))
            story.append(PageBreak())
            
            # Trend analysis (unique feature)
            story.extend(self._create_trend_analysis(results))
            story.append(PageBreak())
            
            # Source analysis
            story.extend(self._create_source_analysis(results))
            story.append(PageBreak())
            
            # Citations
            story.extend(self._create_citations(results))
            
            # Build PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def _create_title_page(self, results: Dict) -> List:
        """Create title page content"""
        story = []
        
        # Title
        query = results.get('query', 'Research Report')
        title = f"Research Report: {query}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = "Generated by AI Research Agent"
        story.append(Paragraph(subtitle, self.styles['CustomHeading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Generation info
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated on: {timestamp}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Research metrics
        extracted_content = results.get('extracted_content', [])
        summaries = results.get('summaries', {})
        search_results = results.get('search_results', [])
        
        # Handle different search result formats
        if isinstance(search_results, dict):
            sources = search_results.get('search_results', [])
        else:
            sources = search_results
        
        total_sources = len(sources) if sources else len(extracted_content)
        unique_domains = len(set(content.get('domain', '') for content in extracted_content)) if extracted_content else 0
        total_words = sum(content.get('word_count', 0) for content in extracted_content) if extracted_content else 0
        
        metrics_data = [
            ['Metric', 'Value'],
            ['Research Query', query],
            ['Sources Analyzed', str(total_sources)],
            ['Unique Domains', str(unique_domains)],
            ['Total Words', str(total_words)],
            ['AI Model Used', summaries.get('metadata', {}).get('ai_model', 'Multiple AI Providers')]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 3*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(metrics_table)
        
        return story
    
    def _create_executive_summary(self, results: Dict) -> List:
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.1*inch))
        
        # Try multiple ways to get summary content - prioritize most complete
        executive_summary = None
        
        # 1. Check for full AI summaries structure (comprehensive research)
        summaries = results.get('summaries', {})
        if isinstance(summaries, dict) and summaries.get('executive_summary'):
            executive_summary = summaries['executive_summary']
        
        # 2. Check for basic summary from AI summarizer
        elif results.get('summary', {}).get('success'):
            summary_data = results['summary']
            executive_summary = summary_data.get('summary')
            
            # Add provider info if available
            provider = summary_data.get('provider', '')
            if provider:
                executive_summary = f"Generated by {provider}:\n\n{executive_summary}"
        
        # 3. Generate from search results if no summary available
        elif results.get('search_results'):
            search_results = results['search_results']
            if isinstance(search_results, dict):
                sources = search_results.get('search_results', [])
            else:
                sources = search_results
            
            if sources:
                query = results.get('query', 'the research topic')
                executive_summary = f"Research analysis of {query} based on {len(sources)} sources. "
                executive_summary += "This report synthesizes information from multiple web sources to provide "
                executive_summary += "comprehensive insights into current developments, key findings, and important trends in this area."
                
                # Add sample content from first few sources
                source_snippets = []
                for source in sources[:3]:
                    snippet = source.get('snippet', '')
                    if snippet and len(snippet) > 50:
                        source_snippets.append(snippet[:200] + "...")
                
                if source_snippets:
                    executive_summary += "\n\nKey insights from research sources:\n"
                    for i, snippet in enumerate(source_snippets, 1):
                        executive_summary += f"\n{i}. {snippet}"
        
        # 4. Fallback if no content available
        if not executive_summary:
            query = results.get('query', 'the research topic')
            executive_summary = f"This research report provides an analysis of {query}. "
            executive_summary += "The report covers available information and provides insights based on "
            executive_summary += "current data and research findings."
        
        story.append(Paragraph(executive_summary, self.styles['CustomBody']))
        
        return story
    
    def _create_key_findings(self, results: Dict) -> List:
        """Create key findings section"""
        story = []
        
        story.append(Paragraph("Key Findings", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.1*inch))
        
        # Try to get key findings from multiple sources
        key_findings = []
        
        # 1. Check full AI summaries structure
        summaries = results.get('summaries', {})
        if isinstance(summaries, dict) and summaries.get('key_findings'):
            key_findings = summaries['key_findings']
        
        # 2. Extract key findings from basic summary
        elif results.get('summary', {}).get('success'):
            summary_text = results['summary'].get('summary', '')
            # Try to extract bullet points or numbered lists from summary
            import re
            
            # Look for bullet points or numbered items
            bullets = re.findall(r'[•\-\*]\s*(.+?)(?=\n|$)', summary_text)
            numbered = re.findall(r'\d+\.\s*(.+?)(?=\n|$)', summary_text)
            
            if bullets:
                key_findings = bullets[:7]  # Limit to 7 findings
            elif numbered:
                key_findings = numbered[:7]
            else:
                # Split summary into sentences and take key ones
                sentences = [s.strip() for s in summary_text.split('.') if len(s.strip()) > 20]
                key_findings = sentences[:5]  # Take first 5 substantial sentences
        
        # 3. Generate findings from search results
        if not key_findings:
            search_results = results.get('search_results', [])
            if isinstance(search_results, dict):
                sources = search_results.get('search_results', [])
            else:
                sources = search_results
            
            if sources:
                query = results.get('query', 'this topic')
                findings_from_sources = []
                
                for source in sources[:5]:  # Use first 5 sources
                    title = source.get('title', '')
                    snippet = source.get('snippet', '')
                    
                    if snippet and len(snippet) > 30:
                        # Create a finding from the source
                        finding = f"According to {source.get('domain', 'research source')}: {snippet[:150]}..."
                        findings_from_sources.append(finding)
                
                key_findings = findings_from_sources
        
        # 4. Display findings or fallback message
        if key_findings:
            for i, finding in enumerate(key_findings, 1):
                story.append(Paragraph(f"{i}. {finding}", self.styles['CustomBody']))
                story.append(Spacer(1, 0.05*inch))
        else:
            query = results.get('query', 'this research topic')
            fallback_text = f"Key insights about {query} are available in the detailed analysis section. "
            fallback_text += "The research covers current developments, trends, and important information "
            fallback_text += "gathered from multiple authoritative sources."
            story.append(Paragraph(fallback_text, self.styles['CustomBody']))
        
        return story
    
    def _create_detailed_analysis(self, results: Dict) -> List:
        """Create detailed analysis section"""
        story = []
        
        story.append(Paragraph("Detailed Analysis", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.1*inch))
        
        # Try to get detailed analysis from multiple sources
        detailed_analysis = None
        
        # 1. Check full AI summaries structure
        summaries = results.get('summaries', {})
        if isinstance(summaries, dict) and summaries.get('detailed_analysis'):
            detailed_analysis = summaries['detailed_analysis']
        
        # 2. Use the main summary if available
        elif results.get('summary', {}).get('success'):
            summary_data = results['summary']
            detailed_analysis = summary_data.get('summary', '')
            
            provider = summary_data.get('provider', '')
            if provider:
                detailed_analysis = f"AI Analysis by {provider}:\n\n{detailed_analysis}"
        
        # 3. Generate analysis from extracted content
        elif results.get('extracted_content'):
            extracted_content = results['extracted_content']
            query = results.get('query', 'the research topic')
            
            analysis_parts = [
                f"Comprehensive analysis of {query} based on {len(extracted_content)} extracted sources:\n"
            ]
            
            for i, content in enumerate(extracted_content[:3], 1):
                title = content.get('title', f'Source {i}')
                text = content.get('text', content.get('content', ''))
                domain = content.get('domain', 'Unknown source')
                
                if text:
                    # Take a substantial excerpt
                    excerpt = text[:500] + "..." if len(text) > 500 else text
                    analysis_parts.append(f"\n{i}. Analysis from {domain} - {title}:\n{excerpt}")
            
            detailed_analysis = "\n".join(analysis_parts)
        
        # 4. Generate from search results if no extracted content
        elif results.get('search_results'):
            search_results = results['search_results']
            if isinstance(search_results, dict):
                sources = search_results.get('search_results', [])
            else:
                sources = search_results
            
            if sources:
                query = results.get('query', 'the research topic')
                analysis_parts = [
                    f"Research analysis of {query} compiled from {len(sources)} web sources:\n"
                ]
                
                for i, source in enumerate(sources[:5], 1):
                    title = source.get('title', f'Source {i}')
                    snippet = source.get('snippet', '')
                    domain = source.get('domain', 'Unknown')
                    
                    if snippet:
                        analysis_parts.append(f"\n{i}. From {domain} - {title}:\n{snippet}")
                
                detailed_analysis = "\n".join(analysis_parts)
        
        # 5. Fallback analysis
        if not detailed_analysis:
            query = results.get('query', 'the research topic')
            detailed_analysis = f"This section provides a detailed examination of {query}. "
            detailed_analysis += "The analysis synthesizes information from available sources to present "
            detailed_analysis += "a comprehensive understanding of current developments, methodologies, "
            detailed_analysis += "and implications in this field. "
            detailed_analysis += "\n\nKey areas of focus include current trends, emerging technologies, "
            detailed_analysis += "challenges and opportunities, and future directions for research and development."
        
        story.append(Paragraph(detailed_analysis, self.styles['CustomBody']))
        
        return story
    
    def _create_trend_analysis(self, results: Dict) -> List:
        """Create trend analysis section (unique feature)"""
        story = []
        
        story.append(Paragraph("Trend Analysis", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.1*inch))
        
        summaries = results.get('summaries', {})
        trend_data = summaries.get('trend_analysis', {})
        
        if "error" in trend_data:
            story.append(Paragraph(f"Trend analysis unavailable: {trend_data['error']}", self.styles['CustomBody']))
            return story
        
        # Emerging Trends
        if trend_data.get("emerging_trends"):
            story.append(Paragraph("Emerging Trends", self.styles['CustomHeading2']))
            for trend in trend_data["emerging_trends"]:
                story.append(Paragraph(f"• {trend}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
        
        # Research Gaps
        if trend_data.get("research_gaps"):
            story.append(Paragraph("Research Gaps", self.styles['CustomHeading2']))
            for gap in trend_data["research_gaps"]:
                story.append(Paragraph(f"• {gap}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
        
        # Future Directions
        if trend_data.get("future_directions"):
            story.append(Paragraph("Future Directions", self.styles['CustomHeading2']))
            for direction in trend_data["future_directions"]:
                story.append(Paragraph(f"• {direction}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
        
        # Full Analysis
        if trend_data.get("analysis_text"):
            story.append(Paragraph("Complete Trend Analysis", self.styles['CustomHeading2']))
            story.append(Paragraph(trend_data["analysis_text"], self.styles['CustomBody']))
        
        return story
    
    def _create_source_analysis(self, results: Dict) -> List:
        """Create source analysis section"""
        story = []
        
        story.append(Paragraph("Source Analysis", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.1*inch))
        
        # Get source data from multiple places
        summaries = results.get('summaries', {})
        source_data = summaries.get('source_analysis', {})
        
        # If no pre-computed source analysis, generate it
        if not source_data:
            search_results = results.get('search_results', [])
            extracted_content = results.get('extracted_content', [])
            
            # Handle different search result formats
            if isinstance(search_results, dict):
                sources = search_results.get('search_results', [])
            else:
                sources = search_results
            
            # Analyze sources
            total_sources = len(sources)
            total_content = len(extracted_content)
            
            # Get domains from both search results and extracted content
            domains = set()
            for source in sources:
                if source.get('domain'):
                    domains.add(source['domain'])
            for content in extracted_content:
                if content.get('domain'):
                    domains.add(content['domain'])
            
            unique_domains = len(domains)
            diversity_score = unique_domains / max(total_sources, 1) if total_sources > 0 else 0
            
            # Categorize domains
            domain_categories = {'academic': [], 'government': [], 'news': [], 'organization': [], 'other': []}
            for domain in domains:
                domain_lower = domain.lower()
                if any(edu in domain_lower for edu in ['.edu', 'university', 'college']):
                    domain_categories['academic'].append(domain)
                elif '.gov' in domain_lower:
                    domain_categories['government'].append(domain)
                elif any(news in domain_lower for news in ['news', 'media', '.com']):
                    domain_categories['news'].append(domain)
                elif '.org' in domain_lower:
                    domain_categories['organization'].append(domain)
                else:
                    domain_categories['other'].append(domain)
            
            # Assess quality
            high_quality_domains = ['.edu', '.gov', '.org']
            quality_count = sum(1 for domain in domains if any(hq in domain.lower() for hq in high_quality_domains))
            quality_ratio = quality_count / len(domains) if domains else 0
            
            if quality_ratio >= 0.7:
                source_quality = "High quality sources"
            elif quality_ratio >= 0.4:
                source_quality = "Mixed quality sources"
            else:
                source_quality = "General web sources"
            
            source_data = {
                'total_sources': total_sources,
                'extracted_content': total_content,
                'unique_domains': unique_domains,
                'diversity_score': round(diversity_score, 2),
                'source_quality': source_quality,
                'domain_categories': domain_categories
            }
        
        # Create metrics table
        if source_data:
            metrics_data = [
                ['Metric', 'Value'],
                ['Search Results', str(source_data.get('total_sources', 0))],
                ['Extracted Content', str(source_data.get('extracted_content', 0))],
                ['Unique Domains', str(source_data.get('unique_domains', 0))],
                ['Diversity Score', f"{source_data.get('diversity_score', 0):.2f}"],
                ['Source Quality', source_data.get('source_quality', 'Unknown')]
            ]
            
            metrics_table = Table(metrics_data, colWidths=[2*inch, 3*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metrics_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Domain categories
            domain_categories = source_data.get('domain_categories', {})
            if any(domains for domains in domain_categories.values()):
                story.append(Paragraph("Domain Categories", self.styles['CustomHeading2']))
                
                for category, domains in domain_categories.items():
                    if domains:
                        domain_list = ', '.join(domains[:5])  # Limit to 5 domains per category
                        if len(domains) > 5:
                            domain_list += f" (+{len(domains)-5} more)"
                        story.append(Paragraph(f"<b>{category.title()}:</b> {domain_list}", self.styles['CustomBody']))
                        story.append(Spacer(1, 0.05*inch))
        else:
            story.append(Paragraph("No source analysis data available.", self.styles['CustomBody']))
        
        return story
    
    def _create_citations(self, results: Dict) -> List:
        """Create citations section"""
        story = []
        
        story.append(Paragraph("References", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.1*inch))
        
        # Try to get citations from multiple sources
        citations = []
        
        # 1. Check for pre-formatted citations
        summaries = results.get('summaries', {})
        if summaries.get('citations'):
            citations = summaries['citations']
        
        # 2. Generate citations from extracted content
        elif results.get('extracted_content'):
            extracted_content = results['extracted_content']
            for i, content in enumerate(extracted_content, 1):
                title = content.get('title', f'Source {i}')
                url = content.get('url', '')
                domain = content.get('domain', 'Unknown')
                publish_date = content.get('publish_date', '')
                author = content.get('author', domain)
                
                # Create APA-style citation
                year = publish_date[:4] if publish_date else 'n.d.'
                apa_citation = f"{author}. ({year}). {title}. {domain}. Retrieved from {url}"
                
                citations.append({
                    'id': i,
                    'title': title,
                    'url': url,
                    'domain': domain,
                    'apa_format': apa_citation
                })
        
        # 3. Generate citations from search results
        elif results.get('search_results'):
            search_results = results['search_results']
            if isinstance(search_results, dict):
                sources = search_results.get('search_results', [])
            else:
                sources = search_results
            
            for i, source in enumerate(sources[:10], 1):  # Limit to 10 citations
                title = source.get('title', f'Source {i}')
                url = source.get('url', '')
                domain = source.get('domain', 'Unknown')
                
                # Create simple citation
                apa_citation = f"{domain}. (2024). {title}. Retrieved from {url}"
                
                citations.append({
                    'id': i,
                    'title': title,
                    'url': url,
                    'domain': domain,
                    'apa_format': apa_citation
                })
        
        # Display citations
        if citations:
            for citation in citations:
                citation_text = f"{citation['id']}. {citation['apa_format']}"
                story.append(Paragraph(citation_text, self.styles['Citation']))
                story.append(Spacer(1, 0.05*inch))
        else:
            story.append(Paragraph("Research conducted using web search and content analysis. Citations would be generated from specific academic or published sources when available.", self.styles['CustomBody']))
        
        return story


# Example usage
if __name__ == "__main__":
    # Test PDF generation
    generator = PDFGenerator()
    
    # Sample data
    sample_results = {
        'query': 'AI Breakthroughs 2024',
        'extracted_content': [
            {
                'title': 'Sample Article',
                'url': 'https://example.com',
                'domain': 'example.com',
                'word_count': 500
            }
        ],
        'summaries': {
            'executive_summary': 'This is a sample executive summary.',
            'key_findings': ['Finding 1', 'Finding 2'],
            'detailed_analysis': 'This is detailed analysis.',
            'trend_analysis': {
                'emerging_trends': ['Trend 1', 'Trend 2'],
                'research_gaps': ['Gap 1'],
                'future_directions': ['Direction 1']
            },
            'source_analysis': {
                'total_sources': 1,
                'unique_domains': 1,
                'diversity_score': 1.0,
                'source_quality': 'High quality sources'
            },
            'citations': [
                {
                    'id': 1,
                    'apa_format': 'Sample Citation (2024). Example.com.'
                }
            ]
        }
    }
    
    output_path = "sample_research_report.pdf"
    try:
        result_path = generator.generate_research_report(sample_results, output_path)
        print(f"PDF generated successfully: {result_path}")
    except Exception as e:
        print(f"PDF generation failed: {str(e)}")
