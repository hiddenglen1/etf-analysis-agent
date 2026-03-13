#!/usr/bin/env python3
"""
Ana Gent - ETF Analysis Agent
Leverages Claude, Alpha Vantage, and Finnhub.io APIs to analyze and price ETFs.
"""

import os
import json
from typing import Any
from dotenv import load_dotenv
import anthropic

from agents.data_fetcher import DataFetcher
from agents.sentiment_analyzer import SentimentAnalyzer
from agents.etf_analyzer import ETFAnalyzer
from utils.config import Config
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

def initialize_agent():
    """Initialize the Ana Gent agent with API configurations."""
    config = Config()
    config.validate()
    
    data_fetcher = DataFetcher(
        alpha_vantage_key=config.alpha_vantage_key,
        finnhub_key=config.finnhub_key
    )
    sentiment_analyzer = SentimentAnalyzer()
    etf_analyzer = ETFAnalyzer(data_fetcher, sentiment_analyzer)
    
    return etf_analyzer, config

def main():
    """Main entry point for the Ana Gent agent."""
    print("\n" + "="*60)
    print("Welcome to Ana Gent - ETF Analysis Agent")
    print("="*60)
    print("Powered by: Claude AI + Alpha Vantage + Finnhub.io\n")
    
    try:
        etf_analyzer, config = initialize_agent()
    except ValueError as e:
        logger.error(f"Configuration Error: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure the following environment variables are set:")
        print("  - ANTHROPIC_API_KEY")
        print("  - ALPHA_VANTAGE_API_KEY")
        print("  - FINNHUB_API_KEY")
        return
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("  1. Analyze an ETF")
        print("  2. Compare ETF Components")
        print("  3. Get Latest News & Sentiment")
        print("  4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            etf_ticker = input("Enter ETF ticker (e.g., SPY, QQQ): ").strip().upper()
            if etf_ticker:
                analyze_etf(etf_analyzer, etf_ticker)
        
        elif choice == "2":
            etf_ticker = input("Enter ETF ticker: ").strip().upper()
            if etf_ticker:
                compare_components(etf_analyzer, etf_ticker)
        
        elif choice == "3":
            ticker = input("Enter ticker symbol: ").strip().upper()
            if ticker:
                get_news_sentiment(etf_analyzer, ticker)
        
        elif choice == "4":
            print("\n👋 Thank you for using Ana Gent. Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")


def analyze_etf(etf_analyzer: "ETFAnalyzer", etf_ticker: str):
    """Analyze a single ETF."""
    print(f"\n🔍 Analyzing {etf_ticker}...")
    
    try:
        result = etf_analyzer.analyze_etf(etf_ticker)
        
        print("\n" + "="*60)
        print(f"ETF Analysis Report: {etf_ticker}")
        print("="*60)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        logger.error(f"Error analyzing ETF {etf_ticker}: {e}")
        print(f"\n❌ Error: {e}")


def compare_components(etf_analyzer: "ETFAnalyzer", etf_ticker: str):
    """Compare top components of an ETF."""
    print(f"\n🔍 Fetching components for {etf_ticker}...")
    
    try:
        components = etf_analyzer.get_top_components(etf_ticker, limit=5)
        
        if components:
            print(f"\n📊 Top Components of {etf_ticker}:")
            print("="*60)
            for comp in components:
                print(f"  {comp['symbol']}: {comp.get('weight', 'N/A')}%")
        else:
            print(f"No components found for {etf_ticker}")
    
    except Exception as e:
        logger.error(f"Error fetching components: {e}")
        print(f"\n❌ Error: {e}")


def get_news_sentiment(etf_analyzer: "ETFAnalyzer", ticker: str):
    """Get latest news and sentiment for a ticker."""
    print(f"\n📰 Fetching news for {ticker}...")
    
    try:
        news_items = etf_analyzer.get_news(ticker, days=7)
        
        if news_items:
            print(f"\n📰 Recent News for {ticker}:")
            print("="*60)
            for i, news in enumerate(news_items[:5], 1):
                print(f"\n{i}. {news.get('headline', 'N/A')}")
                print(f"   Source: {news.get('source', 'N/A')}")
                print(f"   Sentiment: {news.get('sentiment', 'Neutral')}")
        else:
            print(f"No news found for {ticker}")
    
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()