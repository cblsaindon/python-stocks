"""
 Developer: Candace Stokes
 Last Updated: 06/08/2024
 Description: Contains the class and methods required for the investor class
"""

class Investor:
    """
    A class to represent an investor.

    ...

    Attributes
    ----------
    investorID : int
        unique identifier for the investor
    name : str
        full name of the investor
    address : str
        home address of the investor
    phoneNumber : str
        contact phone number of the investor
    stocks : list, optional
        list of stock objects owned by the investor, default is an empty list

    Methods
    -------
    add_stock(stock)
        Adds a stock object to the investor's list of stocks.
    return_record()
        Returns a comma-separated string of the investor details.
    """
    def __init__(self, investorID, name, address, phoneNumber, stocks = []):
        self.investorID = investorID
        self.name = name
        self.address = address
        self.phoneNumber = phoneNumber
        self.stocks = stocks

    def add_stock(self, stock):
        """Takes in stock object, adds to investor object."""
        self.stocks.append(stock)

    def return_record(self):
        """Prints investor details."""
        print_string = self.name + ',' + self.address + ',' + self.phoneNumber + ','
        return print_string

