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
from helper import fmt_large as fl
from helper import fmt_num as fn


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


def get_ticker() -> str:
    """
    Prompt the user repeatedly for a valid stock ticker.

    Returns:
        str: A cleaned, uppercase ticker symbol once valid input is provided.
    """
    while True:
        ticker = input("Please enter the stock ticker you would like to analyze: ").strip()

        # Check empty input
        if ticker == "":
            print("Error: No ticker entered. Please try again.\n")
            continue

        # Basic validation: must be alphabetic
        if not ticker.isalpha():
            print("Error: Ticker symbols must contain only letters. Example: AAPL")
            continue

        # If valid, return uppercase version
        return ticker.upper()



# Steps to Implement Stock Analysis:
# 1. Ask user for stock ticker.
# 2. Use yfinance to fetch current price, change %, volume, market cap, P/E.
# 3. Compute historical returns (1-year and 5-year).
# 4. Generate a matplotlib line chart of historical closing prices.
# 5. Fetch recent news headlines related to the stock.
# 6. Retrieve earnings data: last quarter EPS vs expected, next earnings date.
# 7. Display all gathered information in readable format.

def stockAnalysis() -> None:
    """
    Implements the Stock Analysis tool for the Investment Analyzer program.

    After prompting the user for a stock ticker, this function retrieves 
    real-time market metrics, historical performance, recent news, and 
    earnings information using the yfinance library and related APIs. 
    It also generates a visual chart of historical prices using matplotlib.

    Functionality:
        • Validate and process user ticker input
        • Fetch current stock metrics (price, daily change %, volume)
        • Retrieve valuation metrics (market cap, P/E ratio)
        • Compute historical returns (1-year and 5-year)
        • Generate a historical price chart
        • Display recent news headlines for the stock
        • Retrieve last quarterly earnings (actual vs. expected)
        • Display next earnings report date

    Returns:
        None
    """
    # Need to --- Implement stock analysis functionality
    # - Prompt user for stock ticker
    # - Fetch current price, daily change %, volume, market cap, P/E ratio
    # - Get historical performance (1-year, 5-year returns)
    # - Generate matplotlib chart of historical prices
    # - Fetch recent news headlines
    # - Get earnings data (last quarter, next earnings date)
    # - Display all information to user


    print("\n--- Stock Analysis Tool ---")

    ticker = get_ticker()  # ALWAYS returns a valid ticker now

    stock = yf.Ticker(ticker)

    # 2. Fetch data using yfinance
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info  # dictionary of metrics

    # Extract core metrics with safe .get() lookups
    current_price = info.get("currentPrice")
    previous_close = info.get("previousClose")
    volume = info.get("volume")
    market_cap = info.get("marketCap")
    pe_ratio = info.get("trailingPE")

    # Calculate daily % change only if values are present
    if current_price is not None and previous_close is not None:
        daily_change_percent = ((current_price - previous_close) / previous_close) * 100
    else:
        daily_change_percent = None
    # The output for the User    
    print("\n--- Current Stock Metrics ---")
    print(f"Current Price:        {fn(current_price)}")
    print(f"Previous Close:       {fn(previous_close)}")
    if daily_change_percent is not None:
        print(f"Daily Change (%):     {daily_change_percent:.2f}%")
    else:
        print("Daily Change (%):     N/A")
    print(f"Volume:               {fn(volume)}")
    print(f"Market Cap:           {fl(market_cap)}")
    print(f"Trailing P/E Ratio:   {fn(pe_ratio)}")
    
    # ---------- 3. Historical Performance ----------

    # Download historical price data
    history_1y = ticker_obj.history(period="1y")
    history_5y = ticker_obj.history(period="5y")

    # 1-year return
    if not history_1y.empty:
        start_1y = history_1y["Close"].iloc[0]
        end_1y = history_1y["Close"].iloc[-1]
        return_1y = ((end_1y - start_1y) / start_1y) * 100
    else:
        return_1y = None

    # 5-year return
    if not history_5y.empty:
        start_5y = history_5y["Close"].iloc[0]
        end_5y = history_5y["Close"].iloc[-1]
        return_5y = ((end_5y - start_5y) / start_5y) * 100
    else:
        return_5y = None

    # Display results
    print("\n--- Historical Performance ---")
    if return_1y is not None:
        print(f"1-Year Return:        {return_1y:.2f}%")
    else:
        print("1-Year Return:        N/A")

    if return_5y is not None:
        print(f"5-Year Return:        {return_5y:.2f}%")
    else:
        print("5-Year Return:        N/A")

    '''
    # 3. Historical performance
    download 1-year price history with period="1y"
    download 5-year price history with period="5y"

    compute 1-year return:
        (last_close - first_close) / first_close * 100

    compute 5-year return the same way

    # 4. Plot historical chart
    create matplotlib figure
    plot closing prices with dates
    label axes and title
    show plot

    # 5. Recent news
    attempt to fetch ticker_obj.news
    if news exists:
       print latest 5 headlines with URLs
    else:
       print "No news available"

    # 6. Earnings data
    try to fetch earnings dataframe via ticker_obj.earnings
    try to fetch quarterly earnings via ticker_obj.quarterly_earnings
    extract last EPS actual, last EPS estimate
    extract next earnings date

    # 7. Display results neatly
    print current price, daily change %, volume, market cap, PE
    print 1-year and 5-year returns
    print news headlines
    print earnings info

    return None
'''


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
    stockAnalysis()
    input()
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
