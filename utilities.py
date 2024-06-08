"""
 Developer: Candace Stokes
 Last Updated: 06/08/2024
 Description: Utilities useful to the stock assignment
"""

from tabulate import tabulate
import yfinance as yahooFinance
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import random

class Report:
    @staticmethod
    def create_stock_report(owner_name, table_data):
        """Takes in stock table data, prints table."""
        # Headers for the table
        headers = ["Investor ID", "Stock", "Share #", "Earnings/Loss", "Yearly Earning/Loss"]

        # Generate and print the table
        print(f"Stock ownership for {owner_name}")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def create_bond_report(owner_name, table_data):
        """Takes in bond table data, prints data."""
        # Headers for the table
        headers = ["Investor ID", "Stock", "Share #", "Earnings/Loss", "Yearly Earning/Loss", "Coupon", "Yield"]

        # Generate and print the table
        print(f"Bond ownership for {owner_name}")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

class Header:

    def return_header(self, name):
        """Takes in owners name, returns header."""
        header = 'Stock and bond ownership for ' + name
        header = header + '\n'
        header = 'Stock,Share #,Earnings/Loss,Yearly Earning/Loss,Coupon,Yield'
        header = header + '\n'
        return header
    
def get_stock_price_from_ticker(symbol):
    """Takes in stock symbol, returns current price."""
    try:
        # Directly access the current price from yfinance
        currentPrice = yahooFinance.Ticker(symbol).info['currentPrice']
        print(currentPrice)
        if currentPrice is None:
            raise ValueError(f"No current price available for symbol {symbol}.")
        return currentPrice
    except KeyError:
        # Handle the case where the 'currentPrice' key does not exist
        raise ValueError(f"Cannot find current price for symbol {symbol}.")
    except Exception as e:
        # Handle any other exceptions that may occur
        raise RuntimeError(f"Failed to retrieve stock data for {symbol}: {str(e)}")
    
def create_line_chart(stock_list):
    """Takes in list of stocks, saves and shows line chart."""
    # Increase size
    plt.figure(figsize=(12, 6))

    # Dynamically create lines using random colors and class data
    for stock in stock_list:
        stockValueList = []
        plotLabel = stock.symbol
        r = random.uniform(0, 1)
        g = random.uniform(0, 1)
        b = random.uniform(0, 1)
        for stockPrice in stock.stockPriceList:
            stockValueList.append(stockPrice * stock.noShares)
        plt.plot(stock.stockDateCaptured, stockValueList, label=plotLabel, color=(r,g,b))

    # Format date axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10))) # We want to format for quarterly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Formatting dates
    plt.gcf().autofmt_xdate()

    # Adding title and labels
    plt.title('Stock Portfolio Value over Time')
    plt.xlabel('Date')
    plt.ylabel('Stock Value')

    # Add legend
    plt.legend(loc='upper left')

    # Save and show plot
    plt.savefig(r'C:\Users\cblsa\OneDrive\Desktop\python_work\FinalStockWeek10Assignment\stock_value_over_time.png')
    plt.show()