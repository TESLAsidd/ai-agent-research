"""
Historical Data Module for AI Research Agent
Provides historical trends, past year graphs, data and records analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoricalDataAnalyzer:
    """Analyzes historical trends and generates visualizations"""
    
    def __init__(self):
        self.config = Config()
        self.data_sources = {
            'alpha_vantage': getattr(self.config, 'ALPHA_VANTAGE_API_KEY', None),
            'fred': getattr(self.config, 'FRED_API_KEY', None),
            'yfinance': self._parse_bool_setting(getattr(self.config, 'YFINANCE_ENABLED', 'true')),
            'world_bank': self._parse_bool_setting(getattr(self.config, 'WORLD_BANK_API_ENABLED', 'true'))
        }
    
    def _parse_bool_setting(self, value) -> bool:
        """Safely parse boolean settings that might be strings or booleans"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        else:
            return False
    
    def get_stock_trends(self, symbol: str, period: str = '1y') -> Dict:
        """Get stock market trends and historical data"""
        try:
            # Use Yahoo Finance for free stock data
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist_data = ticker.history(period=period)
            info = ticker.info
            
            if hist_data.empty:
                return {"error": f"No data found for symbol {symbol}"}
            
            # Calculate key metrics
            current_price = hist_data['Close'].iloc[-1]
            start_price = hist_data['Close'].iloc[0]
            price_change = current_price - start_price
            price_change_pct = (price_change / start_price) * 100
            
            # Calculate volatility and moving averages
            hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
            hist_data['Volatility'] = hist_data['Close'].rolling(window=20).std()
            
            # Create interactive chart
            chart_html = self._create_stock_chart(hist_data, symbol, info.get('longName', symbol))
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', symbol),
                'current_price': round(current_price, 2),
                'price_change': round(price_change, 2),
                'price_change_pct': round(price_change_pct, 2),
                'period': period,
                'data_points': len(hist_data),
                'volatility': round(hist_data['Volatility'].iloc[-1], 2),
                'chart_html': chart_html,
                'historical_data': hist_data.to_dict('records'),
                'summary': self._generate_stock_summary(hist_data, symbol, price_change_pct),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting stock trends for {symbol}: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def get_economic_indicators(self, indicator: str = 'GDP', years: int = 5) -> Dict:
        """Get economic indicators and trends"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years * 365)
            
            # Try different data sources
            if self.data_sources['fred']:
                return self._get_fred_data(indicator, start_date, end_date)
            elif self.data_sources['world_bank']:
                return self._get_world_bank_data(indicator, years)
            else:
                return self._get_demo_economic_data(indicator, years)
                
        except Exception as e:
            logger.error(f"Error getting economic indicators: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def get_market_trends(self, market: str = 'S&P500', period: str = '1y') -> Dict:
        """Get overall market trends and analysis"""
        try:
            # Map market names to Yahoo Finance symbols
            market_symbols = {
                'S&P500': '^GSPC',
                'NASDAQ': '^IXIC',
                'DOW': '^DJI',
                'CRYPTO': 'BTC-USD',
                'GOLD': 'GC=F',
                'OIL': 'CL=F'
            }
            
            symbol = market_symbols.get(market, '^GSPC')
            return self.get_stock_trends(symbol, period)
            
        except Exception as e:
            logger.error(f"Error getting market trends: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def analyze_historical_patterns(self, data_type: str, query: str) -> Dict:
        """Analyze historical patterns and generate insights"""
        try:
            patterns = []
            
            if 'stock' in data_type.lower() or 'market' in data_type.lower():
                # Analyze multiple market indices
                indices = ['^GSPC', '^IXIC', '^DJI']
                for idx in indices:
                    try:
                        ticker = yf.Ticker(idx)
                        hist = ticker.history(period='1y')
                        if not hist.empty:
                            pattern = self._analyze_price_patterns(hist, idx)
                            patterns.append(pattern)
                    except:
                        continue
            
            elif 'crypto' in data_type.lower():
                # Analyze cryptocurrency trends
                crypto_symbols = ['BTC-USD', 'ETH-USD', 'ADA-USD']
                for symbol in crypto_symbols:
                    try:
                        ticker = yf.Ticker(symbol)
                        hist = ticker.history(period='1y')
                        if not hist.empty:
                            pattern = self._analyze_price_patterns(hist, symbol)
                            patterns.append(pattern)
                    except:
                        continue
            
            # Generate comprehensive analysis
            analysis = self._generate_pattern_analysis(patterns, query)
            
            return {
                'data_type': data_type,
                'query': query,
                'patterns_found': len(patterns),
                'patterns': patterns,
                'analysis': analysis,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing historical patterns: {str(e)}")
            return {'error': str(e), 'success': False}
    
    def _create_stock_chart(self, data: pd.DataFrame, symbol: str, name: str) -> str:
        """Create interactive stock chart with Plotly"""
        try:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f'{name} ({symbol}) - Price & Moving Averages', 'Volume'),
                row_width=[0.7, 0.3]
            )
            
            # Price and moving averages
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    name='Close Price',
                    line=dict(color='#1f77b4', width=2)
                ),
                row=1, col=1
            )
            
            if 'MA20' in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data['MA20'],
                        name='MA20',
                        line=dict(color='orange', width=1)
                    ),
                    row=1, col=1
                )
            
            if 'MA50' in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data['MA50'],
                        name='MA50',
                        line=dict(color='red', width=1)
                    ),
                    row=1, col=1
                )
            
            # Volume
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name='Volume',
                    marker_color='lightblue'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f'{name} ({symbol}) - Historical Analysis',
                xaxis_title='Date',
                height=600,
                showlegend=True,
                template='plotly_white'
            )
            
            return fig.to_html(include_plotlyjs='cdn')
            
        except Exception as e:
            logger.error(f"Error creating chart: {str(e)}")
            return f"<p>Chart generation failed: {str(e)}</p>"
    
    def _generate_stock_summary(self, data: pd.DataFrame, symbol: str, change_pct: float) -> str:
        """Generate AI-powered summary of stock performance"""
        try:
            trend = "bullish" if change_pct > 0 else "bearish"
            volatility_level = "high" if data['Close'].std() > data['Close'].mean() * 0.1 else "moderate"
            
            recent_high = data['Close'].max()
            recent_low = data['Close'].min()
            current_price = data['Close'].iloc[-1]
            
            summary = f"""
            📊 **{symbol} Performance Analysis (Past Year)**
            
            **Trend**: {trend.upper()} ({change_pct:+.2f}%)
            **Volatility**: {volatility_level.upper()}
            **Price Range**: ${recent_low:.2f} - ${recent_high:.2f}
            **Current Position**: {'Near highs' if current_price > recent_high * 0.9 else 'Near lows' if current_price < recent_low * 1.1 else 'Mid-range'}
            
            **Key Insights**:
            • {'Strong upward momentum' if change_pct > 10 else 'Moderate gains' if change_pct > 0 else 'Declining trend' if change_pct < -10 else 'Sideways movement'}
            • {'High volatility suggests increased risk' if volatility_level == 'high' else 'Moderate volatility indicates stability'}
            • {'Consider profit-taking opportunities' if current_price > recent_high * 0.95 else 'Potential buying opportunity' if current_price < recent_low * 1.05 else 'Monitor for breakout signals'}
            """
            
            return summary.strip()
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def _analyze_price_patterns(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Analyze price patterns and trends"""
        try:
            # Calculate various technical indicators
            data['Returns'] = data['Close'].pct_change()
            data['Volatility'] = data['Returns'].rolling(window=20).std() * np.sqrt(252)
            
            # Trend analysis
            returns_1m = (data['Close'].iloc[-1] / data['Close'].iloc[-21] - 1) * 100 if len(data) > 21 else 0
            returns_3m = (data['Close'].iloc[-1] / data['Close'].iloc[-63] - 1) * 100 if len(data) > 63 else 0
            returns_6m = (data['Close'].iloc[-1] / data['Close'].iloc[-126] - 1) * 100 if len(data) > 126 else 0
            
            return {
                'symbol': symbol,
                'returns_1m': round(returns_1m, 2),
                'returns_3m': round(returns_3m, 2),
                'returns_6m': round(returns_6m, 2),
                'volatility': round(data['Volatility'].iloc[-1], 4) if not data['Volatility'].empty else 0,
                'trend': 'Bullish' if returns_3m > 0 else 'Bearish',
                'data_points': len(data)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing patterns for {symbol}: {str(e)}")
            return {'symbol': symbol, 'error': str(e)}
    
    def _generate_pattern_analysis(self, patterns: List[Dict], query: str) -> str:
        """Generate comprehensive pattern analysis"""
        try:
            if not patterns:
                return "No pattern data available for analysis."
            
            # Calculate averages
            avg_1m = np.mean([p.get('returns_1m', 0) for p in patterns if 'returns_1m' in p])
            avg_3m = np.mean([p.get('returns_3m', 0) for p in patterns if 'returns_3m' in p])
            avg_6m = np.mean([p.get('returns_6m', 0) for p in patterns if 'returns_6m' in p])
            
            bullish_count = sum(1 for p in patterns if p.get('trend') == 'Bullish')
            total_count = len(patterns)
            
            analysis = f"""
            🔍 **Historical Pattern Analysis for: {query}**
            
            **Market Sentiment**: {'BULLISH' if bullish_count > total_count/2 else 'BEARISH'} ({bullish_count}/{total_count} assets trending up)
            
            **Performance Overview**:
            • 1-Month Average: {avg_1m:+.2f}%
            • 3-Month Average: {avg_3m:+.2f}%
            • 6-Month Average: {avg_6m:+.2f}%
            
            **Key Patterns Identified**:
            • {'Strong momentum across markets' if avg_3m > 5 else 'Moderate growth trend' if avg_3m > 0 else 'Market correction phase' if avg_3m > -10 else 'Significant market decline'}
            • {'High correlation between assets' if len(set(p.get('trend') for p in patterns)) == 1 else 'Mixed market conditions'}
            • {'Increasing volatility' if any(p.get('volatility', 0) > 0.3 for p in patterns) else 'Stable market conditions'}
            
            **Investment Insights**:
            • {'Consider diversification' if bullish_count == total_count else 'Monitor risk levels' if bullish_count < total_count/3 else 'Balanced approach recommended'}
            • {'Focus on defensive assets' if avg_6m < -5 else 'Growth opportunities available' if avg_6m > 10 else 'Maintain current allocation'}
            """
            
            return analysis.strip()
            
        except Exception as e:
            return f"Pattern analysis failed: {str(e)}"
    
    def _get_fred_data(self, indicator: str, start_date: datetime, end_date: datetime) -> Dict:
        """Get Federal Reserve Economic Data"""
        try:
            # FRED API implementation would go here
            # For now, return demo data
            return self._get_demo_economic_data(indicator, 5)
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _get_world_bank_data(self, indicator: str, years: int) -> Dict:
        """Get World Bank economic data"""
        try:
            # World Bank API implementation would go here
            # For now, return demo data
            return self._get_demo_economic_data(indicator, years)
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _get_demo_economic_data(self, indicator: str, years: int) -> Dict:
        """Generate demo economic data for testing"""
        try:
            dates = pd.date_range(end=datetime.now(), periods=years*4, freq='Q')
            
            if indicator.upper() == 'GDP':
                # Simulate GDP growth data
                base_growth = 2.5
                values = [base_growth + np.random.normal(0, 0.5) for _ in range(len(dates))]
                title = "GDP Growth Rate (%)"
            elif indicator.upper() == 'INFLATION':
                # Simulate inflation data
                base_inflation = 2.0
                values = [base_inflation + np.random.normal(0, 0.8) for _ in range(len(dates))]
                title = "Inflation Rate (%)"
            else:
                # Generic economic indicator
                base_value = 100
                values = [base_value + i*2 + np.random.normal(0, 5) for i in range(len(dates))]
                title = f"{indicator} Index"
            
            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=values,
                mode='lines+markers',
                name=indicator,
                line=dict(color='#1f77b4', width=3)
            ))
            
            fig.update_layout(
                title=f"{title} - {years} Year Trend",
                xaxis_title="Date",
                yaxis_title=title,
                template='plotly_white',
                height=400
            )
            
            chart_html = fig.to_html(include_plotlyjs='cdn')
            
            return {
                'indicator': indicator,
                'title': title,
                'period_years': years,
                'data_points': len(values),
                'current_value': round(values[-1], 2),
                'avg_value': round(np.mean(values), 2),
                'trend': 'Increasing' if values[-1] > values[0] else 'Decreasing',
                'chart_html': chart_html,
                'data': [{'date': d.strftime('%Y-%m-%d'), 'value': round(v, 2)} for d, v in zip(dates, values)],
                'success': True,
                'source': 'Demo Data',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}

# Example usage
if __name__ == "__main__":
    analyzer = HistoricalDataAnalyzer()
    
    # Test stock analysis
    result = analyzer.get_stock_trends('AAPL', '1y')
    if result.get('success'):
        print(f"Stock analysis completed for AAPL")
        print(f"Price change: {result['price_change_pct']:.2f}%")
    
    # Test market trends
    market_result = analyzer.get_market_trends('S&P500', '1y')
    if market_result.get('success'):
        print(f"Market analysis completed for S&P500")