#!/usr/bin/env python3

# DCS211 Final Project - Investment Analyzer
# Teddy Shapiro & Edward Amini
# December 2025

import sys
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
import pandas as pd


def usage() -> None:
    '''Print usage message and program description.'''
    print("=" * 60)
    print("Investment Analyzer - Stock Analysis & Portfolio Projector")
    print("=" * 60)
    print("\nThis utility provides two main tools:")
    print("\n1. Stock Analysis:")
    print("   - Current price, daily change %, volume, market cap, P/E ratio")
    print("   - Historical performance (1-year, 5-year returns)")
    print("   - Visual chart of historical prices")
    print("   - Recent news headlines")
    print("   - Earnings data (last quarter vs. expectations, next date)")
    print("\n2. Portfolio Growth Projector:")
    print("   - Enter stock ticker(s), investment amount(s), and holding period")
    print("   - Calculate projected returns using historical average (CAGR)")
    print("   - Inflation-adjusted real returns")
    print("   - Visual chart of projected portfolio growth")
    print("\nUsage: python investment_analyzer.py")
    print("=" * 60)


def stockAnalysis() -> None:
    '''
    Analyze individual stocks with current metrics, historical performance,
    news headlines, and earnings data.
    
    Returns:
        None
    '''
    print("\n--- Stock Analysis Tool ---")
    
    # Need to --- Implement stock analysis functionality
    # - Prompt user for stock ticker
    # - Fetch current price, daily change %, volume, market cap, P/E ratio
    # - Get historical performance (1-year, 5-year returns)
    # - Generate matplotlib chart of historical prices
    # - Fetch recent news headlines
    # - Get earnings data (last quarter, next earnings date)
    # - Display all information to user
    


def growthProjector() -> None:
    '''
    Project portfolio growth based on historical performance and inflation adjustment.
    Allows users to enter multiple stocks with investment amounts and holding periods.
    
    Returns:
        None
    '''
    print("\n--- Portfolio Growth Projector ---")
    
    # Need to --- Implement portfolio growth projector functionality
    # - Prompt user for stock ticker(s)
    # - Prompt for investment amount(s) for each stock
    # - Prompt for holding period
    # - Calculate projected returns using historical CAGR
    # - Apply inflation adjustment for real returns
    # - Generate matplotlib chart showing projected growth
    # - Display results to user
    


def main() -> None:
    '''
    Main function that displays menu and handles user's tool selection.
    
    Returns:
        None
    '''
    # Display usage/welcome message
    usage()
    
    # Main program loop
    while True:
        print("\n" + "=" * 60) 
        print("Select a tool:")
        print("  1 - Stock Analysis")
        print("  2 - Portfolio Growth Projector")
        print("  3 - Help (show instructions)")
        print("  4 - Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            stockAnalysis()
        elif choice == '2':
            growthProjector()
        elif choice == '3':
            usage()
        elif choice == '4':
            print("\nThank you for using Investment Analyzer.")
            sys.exit(0)
        else:
            print(f"\nInvalid choice '{choice}'. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
