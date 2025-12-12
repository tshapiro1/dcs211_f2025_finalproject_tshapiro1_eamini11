#!/usr/bin/env python3

# DCS211 Final Project - Investment Analyzer
# Teddy Shapiro & Edward Amini
# December 2025

import sys
import yfinance as yf
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
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
    print("   - Dual visual charts: 1-year and 5-year price history")
    print("   - Recent news headlines via Google News RSS feed")
    print("   - Earnings: Net Income, trailing EPS, next report date")
    print("   - Data sourced from yfinance API (Yahoo Finance)")
    print("\n2. Portfolio Growth Projector:")
    print("   - Enter stock ticker(s), investment amount(s), and holding period")
    print("   - Manual entry OR import from CSV/Excel file")
    print("   - CSV/Excel must have 'TICKER' and 'SHARES' columns")
    print("   - Calculates CAGR from historical data (5-year or max available)")
    print("   - Projects future growth with 2.5% inflation adjustment")
    print("   - Dual charts: Total portfolio + individual stock breakdowns")
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
    
    # ---------- 4. Recent News ----------
    
    print("\n--- Recent News ---")
    
    try:
        # Get company name for better search results
        company_name = info.get('longName', ticker)
        search_term = company_name if company_name else ticker
        
        # Build Google News RSS feed URL
        rss_url = f"https://news.google.com/rss/search?q={search_term}+stock&hl=en-US&gl=US&ceid=US:en"
        
        # Set browser headers so Google accepts our request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        # Fetch the news feed
        response = requests.get(rss_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Parse the XML response with BeautifulSoup
            soup = BeautifulSoup(response.content, 'xml')
            
            # Find all news articles
            articles = soup.find_all('item')
            
            # Display up to 5 recent articles
            if articles:
                for i, article in enumerate(articles[:5], 1):
                    title = article.find('title')
                    link = article.find('link')
                    date = article.find('pubDate')
                    
                    # Print article info if title exists
                    if title and title.text:
                        print(f"\n{i}. {title.text}")
                        if link and link.text:
                            print(f"   Link: {link.text}")
                        if date and date.text:
                            print(f"   Date: {date.text}")
            else:
                # No articles found in feed
                print("No recent news found.")
                print(f"\nView news at: https://finance.yahoo.com/quote/{ticker}/news")
        else:
            # Request failed
            print("Unable to fetch news automatically.")
            print(f"\nView news at: https://finance.yahoo.com/quote/{ticker}/news")
            
    except Exception as e:
        # Any error occurred
        print("Unable to fetch news automatically.")
        print(f"\nView news at: https://finance.yahoo.com/quote/{ticker}/news")
    
    # ---------- 5. Earnings Data ----------
    
    print("\n--- Earnings Information ---")
    try:
        # Get the quarterly income statement
        quarterly_income = ticker_obj.quarterly_income_stmt
        
        # Check if we have income data
        if quarterly_income is not None and not quarterly_income.empty:
            # Get the most recent quarter's Net Income
            if 'Net Income' in quarterly_income.index:
                latest_net_income = quarterly_income.loc['Net Income'].iloc[0]
                quarter_date = quarterly_income.columns[0]
                
                print(f"Most Recent Quarter Net Income: ${latest_net_income:,.0f}")
                print(f"Quarter Date: {quarter_date.strftime('%Y-%m-%d')}")
        
        # Get trailing EPS (earnings per share for last 12 months)
        eps = info.get('trailingEps')
        if eps:
            print(f"Trailing EPS (12 months): ${eps:.2f}")
        
        # Get next earnings date - try multiple sources
        next_earnings_found = False
        
        # Source 1: Try the info dictionary first (most reliable)
        earnings_date_list = info.get('earningsDate')
        if earnings_date_list and isinstance(earnings_date_list, list) and len(earnings_date_list) > 0:
            # Convert timestamp to readable date
            earnings_date = earnings_date_list[0]
            print(f"Next Earnings Date: {earnings_date.strftime('%Y-%m-%d')}")
            next_earnings_found = True
        
        # Source 2: Try calendar object
        if not next_earnings_found:
            try:
                calendar = ticker_obj.calendar
                if calendar is not None and 'Earnings Date' in calendar.index:
                    earnings_date = calendar.loc['Earnings Date'].iloc[0]
                    if pd.notna(earnings_date):
                        print(f"Next Earnings Date: {earnings_date.strftime('%Y-%m-%d')}")
                        next_earnings_found = True
            except:
                pass
        
        # If no date found, print message
        if not next_earnings_found:
            print("Next Earnings Date: Not available")
            
    except Exception as e:
        print(f"Unable to fetch earnings data: {e}")
    
    # ---------- 6. Historical Price Charts (displayed last) ----------
    
    print("\n--- Historical Price Charts ---")
    print("Close the chart windows to continue...\n")
    
    # Chart 1: 1-year history
    if not history_1y.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(history_1y.index, history_1y['Close'], linewidth=2, color='blue')
        plt.title(f'{ticker} Stock Price - Past Year', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Format y-axis to show currency
        ax = plt.gca()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
        
        plt.show()
        print("[Chart displayed: 1-year price history]")
    else:
        print("[1-year chart unavailable: Insufficient price data]")
    
    # Chart 2: 5-year history
    if not history_5y.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(history_5y.index, history_5y['Close'], linewidth=2, color='green')
        plt.title(f'{ticker} Stock Price - Past 5 Years', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Format y-axis to show currency
        ax = plt.gca()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
        
        plt.show()
        print("[Chart displayed: 5-year price history]")
    else:
        print("[5-year chart unavailable: Insufficient price data]")


def importPortfolioFromCSV() -> list:
    '''
    Import portfolio holdings from a CSV or Excel file.
    Expects columns labeled "TICKER" and "SHARES" (case-insensitive).
    Converts share quantities to dollar amounts using current market prices.
    
    Returns:
        list: List of tuples (ticker, dollar_amount) or empty list if import fails
    '''
    # Get file path from user
    file_input = input("\nEnter file path (CSV or Excel, or just filename if in current folder): ").strip()
    
    # Remove quotes if user copied path with quotes
    file_input = file_input.strip('"').strip("'")
    
    # Check if it's just a filename or full path
    import os
    if not os.path.isabs(file_input):
        # It's just a filename, look in current directory
        file_path = os.path.join(os.getcwd(), file_input)
    else:
        # It's a full path
        file_path = file_input
    
    # Try to read the file (support both CSV and Excel)
    try:
        # Check file extension
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            print("Error: File must be .csv, .xlsx, or .xls format")
            return []
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # Convert column names to uppercase and strip whitespace for case-insensitive matching
    df.columns = df.columns.str.strip().str.upper()
    
    # Debug: print columns found
    print(f"Columns found in file: {list(df.columns)}")
    
    # Check if TICKER and SHARES columns exist
    if 'TICKER' not in df.columns:
        print("Error: File must have a column labeled 'TICKER' (case doesn't matter)")
        print(f"Available columns: {list(df.columns)}")
        return []
    if 'SHARES' not in df.columns:
        print("Error: File must have a column labeled 'SHARES' (case doesn't matter)")
        print(f"Available columns: {list(df.columns)}")
        return []
    
    # Extract ticker and shares data
    portfolio = []
    print("\nProcessing CSV data...")
    
    for index, row in df.iterrows():
        ticker = str(row['TICKER']).strip().upper()
        shares = row['SHARES']
        
        # Skip empty rows
        if pd.isna(ticker) or ticker == '' or ticker == 'NAN':
            continue
        if pd.isna(shares) or shares == '':
            continue
        
        # Validate ticker (should be letters only)
        if not ticker.isalpha():
            print(f"Warning: Skipping invalid ticker '{ticker}' on row {index + 2}")
            continue
        
        # Convert shares to number
        try:
            shares = float(shares)
            if shares <= 0:
                print(f"Warning: Skipping {ticker} - shares must be greater than 0")
                continue
        except (ValueError, TypeError):
            print(f"Warning: Skipping {ticker} - invalid share quantity '{shares}'")
            continue
        
        # Fetch current price to calculate dollar amount
        print(f"Fetching current price for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get('currentPrice')
            
            if current_price is None or current_price <= 0:
                # Try getting from recent history instead
                history = stock.history(period="1d")
                if not history.empty:
                    current_price = history['Close'].iloc[-1]
                else:
                    print(f"Warning: Could not fetch price for {ticker}. Skipping.")
                    continue
            
            dollar_amount = shares * current_price
            portfolio.append((ticker, dollar_amount))
            print(f"  Added: {ticker} - {shares} shares @ ${current_price:.2f} = ${dollar_amount:,.2f}")
            
        except Exception as e:
            print(f"Warning: Error fetching data for {ticker}: {e}. Skipping.")
            continue
    
    if not portfolio:
        print("\nError: No valid stocks found in CSV.")
        return []
    
    print(f"\nSuccessfully imported {len(portfolio)} stocks from CSV.")
    return portfolio


def growthProjector() -> None:
    '''
    Project portfolio growth based on historical performance and inflation adjustment.
    Allows users to enter multiple stocks with investment amounts and holding periods.
    
    Returns:
        None
    '''
    print("\n--- Portfolio Growth Projector ---")
    
    # Step 1: Ask user how they want to input portfolio
    print("\nHow would you like to add stocks to your portfolio?")
    print("  1 - Manual entry (type tickers and amounts)")
    print("  2 - Import from CSV or Excel file")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Error: Please enter 1 or 2.")
    
    portfolio = []  # List to store tuples of (ticker, amount)
    
    if choice == '2':
        # Import from CSV
        portfolio = importPortfolioFromCSV()
        if not portfolio:
            print("\nCSV import failed. Returning to menu.")
            return
    else:
        # Manual entry
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
        try:
            # Get historical data for CAGR calculation
            stock = yf.Ticker(ticker)
            
            # Get company info to find IPO date
            info = stock.info
            
            # Get company name for display
            company_name = info.get('longName', ticker)
            print(f"\nAnalyzing {company_name} ({ticker})...")
            
            # Determine how long company has been public
            # Get all available historical data to check IPO date
            max_history = stock.history(period="max")
            
            if max_history.empty:
                print(f"Warning: No historical data available for {ticker}. Skipping.")
                continue
            
            # Calculate years since IPO (first available trading date)
            first_date = max_history.index[0]
            # Convert to timezone-naive datetime
            first_date_naive = pd.to_datetime(first_date).tz_localize(None)
            years_since_ipo = (datetime.now() - first_date_naive).days / 365.25
            
            print(f"  Years since IPO: {years_since_ipo:.1f}")
            
            # Determine which period to use based on company age
            if years_since_ipo < 5:
                # Young company - use all available data
                history = max_history
                print(f"  Using all available data (young company)")
            elif years_since_ipo < 10:
                # Mid-age company - use recent 3-5 years to avoid early hypergrowth
                history = stock.history(period="5y")
                print(f"  Using recent 5 years (excluding early hypergrowth)")
            else:
                # Mature company - use recent 5 years
                history = stock.history(period="5y")
                print(f"  Using recent 5 years (mature company)")
            
            if history.empty or len(history) < 2:
                print(f"Warning: Insufficient historical data for {ticker}. Skipping.")
                continue
            
            # Calculate CAGR: ((Ending Value / Beginning Value)^(1/years)) - 1
            start_price = history['Close'].iloc[0]
            end_price = history['Close'].iloc[-1]
            years_of_data = len(history) / 252  # Approximate trading days per year
            
            cagr = ((end_price / start_price) ** (1 / years_of_data)) - 1
            
            # Cap CAGR at 15% to prevent unrealistic projections
            MAX_CAGR = 0.15
            if cagr > MAX_CAGR:
                print(f"  Calculated CAGR: {cagr*100:.2f}% (capped at {MAX_CAGR*100:.0f}%)")
                cagr = MAX_CAGR
            else:
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
            
            # Check for NaN values (can happen with invalid/problem stocks)
            if pd.isna(nominal_final) or pd.isna(real_final) or any(pd.isna(v) for v in yearly_values):
                print(f"  Warning: Unable to calculate valid projections for {ticker}. Skipping.")
                continue
            
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
    
    # Calculate portfolio CAGR (using total portfolio growth)
    portfolio_cagr = ((total_nominal / total_initial) ** (1 / holding_period)) - 1
    
    # Calculate average individual stock CAGR
    average_stock_cagr = sum(proj['cagr'] for proj in stock_projections) / len(stock_projections)
    
    print(f"\nTotal Initial Investment: ${total_initial:,.2f}")
    print(f"Total Projected Value (nominal): ${total_nominal:,.2f}")
    print(f"Total Projected Value (inflation-adjusted): ${total_real:,.2f}")
    print(f"Total Nominal Gain: ${total_nominal - total_initial:,.2f} ({((total_nominal/total_initial - 1)*100):.2f}%)")
    print(f"Total Real Gain: ${total_real - total_initial:,.2f} ({((total_real/total_initial - 1)*100):.2f}%)")
    print(f"\nPortfolio CAGR: {portfolio_cagr*100:.2f}%")
    print(f"Average Stock CAGR: {average_stock_cagr*100:.2f}%")
    
    # Step 5: Generate visualizations
    print("\nGenerating charts...")
    
    # Chart 1: Total portfolio value over time
    years = list(range(holding_period + 1))
    total_yearly_values = [0] * (holding_period + 1)
    
    # Sum up all stocks' values for each year
    for proj in stock_projections:
        for i, value in enumerate(proj['yearly_values']):
            total_yearly_values[i] += value
    
    # Debug output
    print(f"\nDebug - Total yearly values: {[f'${v:,.0f}' for v in total_yearly_values[:5]]}... to ${total_yearly_values[-1]:,.0f}")
    print(f"Debug - Number of years: {len(years)}, Number of values: {len(total_yearly_values)}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, total_yearly_values, marker='o', linewidth=2, markersize=6, color='blue', label='Total Portfolio')
    plt.title(f'Total Portfolio Projected Growth ({holding_period} Years)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Set explicit axis limits for better visualization
    plt.xlim(-0.5, holding_period + 0.5)
    y_min = min(total_yearly_values) * 0.95
    y_max = max(total_yearly_values) * 1.05
    plt.ylim(y_min, y_max)
    
    plt.tight_layout()
    
    # Format y-axis to show currency
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.show()
    
    # Chart 2: Individual stock projections
    plt.figure(figsize=(14, 8))
    
    # Use a colormap with many distinct colors
    import matplotlib.cm as cm
    colors = cm.tab20c(range(len(stock_projections)))  # tab20c has 20 distinct colors
    
    # If more than 20 stocks, use additional colormaps
    if len(stock_projections) > 20:
        colors = list(cm.tab20c(range(20))) + list(cm.tab20b(range(len(stock_projections) - 20)))
    
    for idx, proj in enumerate(stock_projections):
        plt.plot(years, proj['yearly_values'], marker='o', linewidth=2.5, 
                markersize=4, label=proj['ticker'], color=colors[idx], alpha=0.8)
    
    plt.title(f'Individual Stock Projected Growth ({holding_period} Years)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Investment Value ($)', fontsize=12)
    
    # Improve legend: place outside plot area if many stocks
    if len(stock_projections) > 10:
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9, ncol=1)
    else:
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
