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
    
    # Step 1: Collect portfolio information from user
    portfolio = []  # List to store tuples of (ticker, amount)
    
    while True:
        # Get ticker
        ticker = input("\nEnter stock ticker: ").strip().upper()
        
        # Validate ticker is not empty and contains only letters
        if ticker == "" or not ticker.isalpha():
            print("Error: Please enter a valid ticker symbol (letters only).")
            continue
        
        # Get investment amount
        while True:
            amount_str = input(f"Enter investment amount for {ticker}: $").strip()
            # Remove commas if user entered them
            amount_str = amount_str.replace(",", "")
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Error: Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        
        # Add to portfolio
        portfolio.append((ticker, amount))
        print(f"Added {ticker} with ${amount:,.2f}")
        
        # Ask if they want to add another stock
        while True:
            add_more = input("\nAdd another stock? (y/n): ").strip().lower()
            if add_more in ['y', 'n', 'yes', 'no']:
                break
            print("Error: Please enter 'y' or 'n'.")
        
        if add_more in ['n', 'no']:
            break
    
    # Step 2: Get holding period
    while True:
        period_str = input("\nEnter holding period (in years): ").strip()
        try:
            holding_period = int(period_str)
            if holding_period <= 0:
                print("Error: Holding period must be greater than 0.")
                continue
            break
        except ValueError:
            print("Error: Please enter a whole number of years.")
    
    print(f"\n{'='*60}")
    print(f"Calculating projections for {len(portfolio)} stock(s) over {holding_period} years...")
    print(f"{'='*60}")
    
    # Step 3: Calculate CAGR for each stock and project growth
    # US 10-year average inflation rate (approximate)
    INFLATION_RATE = 0.025  # 2.5%
    
    stock_projections = []  # List to store projection data for each stock
    
    for ticker, initial_amount in portfolio:
        print(f"\nAnalyzing {ticker}...")
        
        try:
            # Get historical data for CAGR calculation
            stock = yf.Ticker(ticker)
            
            # Use holding period for historical data, capped at 10 years
            history_period = min(holding_period, 10)
            history = stock.history(period=f"{history_period}y")
            
            if history.empty or len(history) < 2:
                print(f"Warning: Insufficient historical data for {ticker}. Skipping.")
                continue
            
            # Calculate CAGR: ((Ending Value / Beginning Value)^(1/years)) - 1
            start_price = history['Close'].iloc[0]
            end_price = history['Close'].iloc[-1]
            years_of_data = len(history) / 252  # Approximate trading days per year
            
            cagr = ((end_price / start_price) ** (1 / years_of_data)) - 1
            
            print(f"  Historical CAGR ({int(years_of_data)} years): {cagr*100:.2f}%")
            
            # Project future values year by year
            yearly_values = [initial_amount]  # Start with initial investment
            for year in range(1, holding_period + 1):
                # Apply CAGR to get nominal value
                projected_value = initial_amount * ((1 + cagr) ** year)
                yearly_values.append(projected_value)
            
            # Calculate inflation-adjusted final value
            nominal_final = yearly_values[-1]
            real_final = nominal_final / ((1 + INFLATION_RATE) ** holding_period)
            
            # Store projection data
            stock_projections.append({
                'ticker': ticker,
                'initial': initial_amount,
                'cagr': cagr,
                'yearly_values': yearly_values,
                'nominal_final': nominal_final,
                'real_final': real_final
            })
            
            print(f"  Initial Investment: ${initial_amount:,.2f}")
            print(f"  Projected Value (nominal): ${nominal_final:,.2f}")
            print(f"  Projected Value (inflation-adjusted): ${real_final:,.2f}")
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            continue
    
    # Check if we have any valid projections
    if not stock_projections:
        print("\nError: No valid stock data could be retrieved. Returning to menu.")
        return
    
    # Step 4: Calculate total portfolio projections
    print(f"\n{'='*60}")
    print("PORTFOLIO SUMMARY")
    print(f"{'='*60}")
    
    total_initial = sum(proj['initial'] for proj in stock_projections)
    total_nominal = sum(proj['nominal_final'] for proj in stock_projections)
    total_real = sum(proj['real_final'] for proj in stock_projections)
    
    print(f"\nTotal Initial Investment: ${total_initial:,.2f}")
    print(f"Total Projected Value (nominal): ${total_nominal:,.2f}")
    print(f"Total Projected Value (inflation-adjusted): ${total_real:,.2f}")
    print(f"Total Nominal Gain: ${total_nominal - total_initial:,.2f} ({((total_nominal/total_initial - 1)*100):.2f}%)")
    print(f"Total Real Gain: ${total_real - total_initial:,.2f} ({((total_real/total_initial - 1)*100):.2f}%)")
    
    # Step 5: Generate visualizations
    print("\nGenerating charts...")
    
    # Chart 1: Total portfolio value over time
    years = list(range(holding_period + 1))
    total_yearly_values = [0] * (holding_period + 1)
    
    # Sum up all stocks' values for each year
    for proj in stock_projections:
        for i, value in enumerate(proj['yearly_values']):
            total_yearly_values[i] += value
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, total_yearly_values, marker='o', linewidth=2, markersize=6, color='blue')
    plt.title(f'Total Portfolio Projected Growth ({holding_period} Years)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Format y-axis to show currency
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.show()
    
    # Chart 2: Individual stock projections
    plt.figure(figsize=(12, 7))
    
    for proj in stock_projections:
        plt.plot(years, proj['yearly_values'], marker='o', linewidth=2, 
                markersize=5, label=proj['ticker'])
    
    plt.title(f'Individual Stock Projected Growth ({holding_period} Years)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Investment Value ($)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Format y-axis to show currency
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.show()
    
    print("\nProjection complete! Charts displayed.")
    


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
