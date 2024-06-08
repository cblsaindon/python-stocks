"""
 Developer: Candace Stokes
 Last Updated: 06/06/2024
 Description: Unit tests for the stock application.
"""

import unittest
from datetime import datetime
from stock import Stock, Bond  # Import your classes
from unittest.mock import patch
from utilities import Report
from tabulate import tabulate
from investor import Investor

class TestStock(unittest.TestCase):
    def setUp(self):
        """Create a test instance of Stock with known values."""
        self.stock = Stock('AAPL', 100, 150, 200, datetime.now(), 1)

    def test_add_price(self):
        """Test adding price and date records to the stock."""
        self.stock.add_price(210, datetime.now())
        self.assertEqual(self.stock.stockPriceList[-1], 210)

    def test_return_record(self):
        """Test the return record output format."""
        record = self.stock.return_record()
        self.assertTrue(isinstance(record, str))

    def test_calculate_loss_gain(self):
        """Test the calculation of loss or gain."""
        expected_gain = (self.stock.currentValue - self.stock.purchasePrice) * self.stock.noShares
        self.assertEqual(self.stock.calculate_loss_gain(), "{:,.2f}".format(expected_gain))

class TestBond(unittest.TestCase):
    def setUp(self):
        """Create a test instance of Bond with known values."""
        self.bond = Bond('US2027', 50, 105, 110, datetime.now(), 1, 2.5, '1.5%')

    def test_return_record(self):
        """Test bond specific output that includes coupon and yield."""
        record = self.bond.return_record()
        self.assertIn('2.5', record)
        self.assertIn('1.5%', record)

class TestUtilities(unittest.TestCase):
    @patch('builtins.print')  # Mocking the print function
    def test_create_stock_report(self, mock_print):
        """Test the stock report output."""
        data = [['1', 'AAPL', 100, '100.00', '10%']]
        Report.create_stock_report('John Doe', data)
        mock_print.assert_called_with(tabulate(data, headers=['Investor ID', 'Stock', 'Share #', 'Earnings/Loss', 'Yearly Earning/Loss'], tablefmt="grid"))

class TestInvestor(unittest.TestCase):
    def setUp(self):
        """Set up test variables for each test."""
        self.investor = Investor(1, "John Doe", "123 Elm Street", "555-1234", [])

    def test_add_stock(self):
        """Test adding a stock to the investor's portfolio."""
        self.investor.add_stock('AAPL')  # Assuming 'AAPL' is a placeholder for a stock object
        self.assertIn('AAPL', self.investor.stocks)
        self.assertEqual(len(self.investor.stocks), 1)

    def test_return_record(self):
        """Test the return_record method output."""
        record = self.investor.return_record()
        expected_string = "John Doe,123 Elm Street,555-1234,"
        self.assertEqual(record, expected_string)

if __name__ == '__main__':
    unittest.main()