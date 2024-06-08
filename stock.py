"""
 Developer: Candace Stokes
 Last Updated: 06/08/2024
 Description: Contains the stock and bond class that stores the attributes and methods for manipulating stocks
"""

from datetime import datetime

class Stock:
    """
    A class to represent a stock.

    ...

    Attributes
    ----------
    stockID : int
        Automatically assigned unique identification number for each stock instance.
    symbol : str
        The stock symbol or ticker.
    noShares : int
        Number of shares held.
    purchasePrice : float
        The price per share at the time of purchase.
    currentValue : float
        The current price per share.
    purchaseDate : datetime
        The date on which the shares were purchased.
    investorID : int
        The ID of the investor who owns the stock.
    stockPriceList : list
        A list to store price values over time.
    stockDateCaptured : list
        A list to store the corresponding dates for the stock prices.

    Methods
    -------
    add_price(price, date)
        Adds a stock price and the corresponding date to the stock object.
    return_record()
        Returns a formatted string containing the stock details.
    calculate_loss_gain()
        Calculates the total money gain or loss based on the purchase and current prices.
    calculate_yearly_earnings_loss()
        Calculates the annualized percentage gain or loss.
    """

    # Class-level counter for purchase IDs
    next_stock_id = 1

    def __init__(self, symbol, noShares, purchasePrice, currentValue, purchaseDate, investorID):
        # Assign the next available purchase ID
        Stock.next_stock_id += 1

        self.stockID = Stock.next_stock_id # Purchase identification number
        self.symbol = symbol # the stock symbol
        self.noShares = noShares # number of shares purchased
        self.purchasePrice = purchasePrice # amount the stock was purchased for in dollars
        self.currentValue = currentValue # how much the stock is currently worth in dollars
        self.purchaseDate = purchaseDate # when the stock was purchased
        self.investorID = investorID # Comes from the investor table
        self.stockPriceList = []
        self.stockDateCaptured = []

    def add_price(self, price, date):
        """Takes in stock price and date, adds both to stock object."""
        # Add information to the class
        self.stockPriceList.append(price)
        self.stockDateCaptured.append(date)

    def return_record(self):
        """Price stock details."""
        print_string = self.symbol + ',' + str(self.noShares) + ", " + str(self.calculate_loss_gain()) + ',' + str(self.calculate_yearly_earnings_loss()) + ',,'
        
        return print_string

    def calculate_loss_gain(self):
        """Returns amount earned or lost."""
        priceVariation = (self.currentValue - self.purchasePrice) * self.noShares
        priceVariation = "{:,.2f}".format(priceVariation)
        
        return priceVariation

    def calculate_yearly_earnings_loss(self):
        """Returns the yearly earnings/loss rate."""
        currentDate = datetime.now()

        # Convert string to datetime
        date_string = "2015-08-01 00:00:00"
        date_format = "%Y-%m-%d %H:%M:%S"
        newPurchaseDate = datetime.strptime(date_string, date_format)
        DateDifference = (currentDate - newPurchaseDate).days
        yearlyEarningsLoss = ((((self.currentValue - self.purchasePrice)/self.purchasePrice)/DateDifference))*100
        yearlyEarningsLoss = "{:.2%}".format(yearlyEarningsLoss)

        return yearlyEarningsLoss

class Bond(Stock):
    """
    A class to represent a bond, inheriting from Stock.

    ...

    Attributes
    ----------
    coupon : float
        The bond's coupon rate, representing the annual interest payment as a percentage of the bond's face value.
    the_yield : float
        The yield of the bond at the time of purchase, reflecting the return over the bond's remaining life.

    Methods
    -------
    return_record()
        Returns a formatted string containing the bond details, including financial metrics and bond-specific attributes.
    """

    def __init__(self, symbol, noShares, purchasePrice, currentValue, purchaseDate, investorID, coupon, the_yield):
        super().__init__(symbol, noShares, purchasePrice, currentValue, purchaseDate, investorID)
        self.coupon = coupon
        self.the_yield = the_yield

    def return_record(self):
        """Prints bond details."""
        print_string = self.symbol + ',' + str(self.calculate_loss_gain()) + ',' + str(self.calculate_yearly_earnings_loss()) + ',' + str(self.coupon) + ',' + str(self.the_yield)
        return print_string
    
class StockPrice:
    """
    A class to represent the price data for a stock on a given day.

    ...

    Attributes
    ----------
    symbol : str
        The stock symbol or ticker.
    date : datetime
        The date of the stock price data.
    open : float
        The opening price of the stock for the given day.
    high : float
        The highest price of the stock during the trading day.
    low : float
        The lowest price of the stock during the trading day.
    close : float
        The closing price of the stock for the day.
    volume : int
        The volume of shares traded during the day.
    """
    def __init__(self, symbol, date, open, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume