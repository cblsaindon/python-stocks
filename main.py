"""
 Developer: Candace Stokes
 Last Updated: 06/08/2024
 Description: Creates a stock report sharing earnings and losses.
"""

from stock import Stock, Bond, StockPrice
from utilities import *
from investor import Investor
from database import *
from datetime import datetime
import json
import pandas as pd

# Dictionary to store the data
stock_data = {}

# Convert the dictionary to a DataFrame for better visualization and manipulation
df_stock_data = pd.DataFrame(stock_data).T  # Transpose to get stocks as rows

# Convert the dictionary to a DataFrame for better visualization and manipulation
df_stock_data = pd.DataFrame(stock_data).T  # Transpose to get stocks as rows

# Initialize lists
stock_list = []
bond_list = []
investor_list = []
stockprice_list = []

# Get sqlite connection
try:
    cursor = establish_sql_connection()
except:
    print("Error establishing connection")

# Drop existing tables to start fresh (good for testing)
drop_tables(cursor)

# Create sqlite tables if they do not exist
try:
    create_tables(cursor)
except:
    print("Error creating tables")

# How to read and interpret a json file
file_path = 'C:/temp/AllStocks.json'
try:
    with open(file_path) as json_file:
        data_set = json.load(json_file)
except:
    print ("Error encountered when opening and setting stock file: " + file_path)

# Add the new stock pricing to the list
for stock in data_set:
    newStock = StockPrice(stock['Symbol'], datetime.strptime(stock['Date'], '%d-%b-%y'), stock['Open'],
                    stock['High'], stock['Low'], stock['Close'], stock['Volume'])
    stockprice_list.append(newStock)

# Open stock file
read_file_path = r'C:\temp\Assignment10_Stocks.csv'
try:
    read_file = open(read_file_path, 'r')
except FileNotFoundError:
    print ("Error encountered when opening stock file: " + read_file_path)

# Get headers
header = read_file.readline()
header_split = header.split(',')

# Get header indexes
symbol_index = header_split.index('SYMBOL')
noShare_index = header_split.index('NO_SHARES')
purchasePrice_index = header_split.index('PURCHASE_PRICE')
purchaseDate_index = header_split.index('PURCHASE_DATE\n')

for line in read_file:
    line_split = line.split(',')

    # Get current stock price from yfinance function
    currentValue = get_stock_price_from_ticker(line_split[symbol_index])

    new_stock = Stock(line_split[symbol_index],
                        float(line_split[noShare_index]),
                        float(line_split[purchasePrice_index]),
                        float(currentValue),
                        datetime.strptime(line_split[purchaseDate_index].strip(), '%m/%d/%Y'),
                        '')
    stock_list.append(new_stock)

# Add the price and date to all the stocks based off JSON
for stock in stock_list:
    for jsonStock in data_set:
        if stock.symbol == jsonStock['Symbol']:
            stock.add_price(jsonStock['Close'],datetime.strptime(jsonStock['Date'], '%d-%b-%y'))
        
# Open bond file
read_file_path = r'C:\temp\Assignment10_Bonds.csv'
try:
    read_file = open(read_file_path, 'r')
except FileNotFoundError:
    print ("Error encountered when opening bond file: " + read_file_path)

# Get headers
header = read_file.readline()
header_split = header.split(',')

# Get header indexes
symbol_index = header_split.index('SYMBOL')
noShare_index = header_split.index('NO_SHARES')
purchasePrice_index = header_split.index('PURCHASE_PRICE')
currentPrice_index = header_split.index('CURRENT_PRICE')
purchaseDate_index = header_split.index('PURCHASE_DATE')
coupon_index = header_split.index('Coupon')
yield_index = header_split.index('Yield\n')

for line in read_file:
    line_split = line.split(',')

    new_bond = Bond(line_split[symbol_index],
                        float(line_split[noShare_index]),
                        float(line_split[purchasePrice_index]),
                        float(line_split[currentPrice_index]),
                        datetime.strptime(line_split[purchaseDate_index].strip(), '%m/%d/%Y'),
                        '',
                        line_split[coupon_index],
                        line_split[yield_index]
                        )
    bond_list.append(new_bond)

# Create object for Bob Smith and add to Owner List
my_investor = Investor(1,'Bob Smith', '123 Safe Street Denver CO 80241', '555-303-2459',[])
investor_list.append(my_investor)

# Dynamically add stocks and bonds to the investor's portfolio
for stock in stock_list:    
    my_investor.add_stock(stock)
    stock.investorID = my_investor.investorID # Associate the investor id to the bond for the database

for bond in bond_list:    
    my_investor.add_stock(bond)
    bond.investorID = my_investor.investorID # Associate the investor id to the bond for the database

# Add stocks and bonds to database
write_data(cursor,stock_list, bond_list, investor_list, stockprice_list)

# Get the stock bond and investor data from the database
db_stocks = read_stock(cursor)
db_bonds = read_bond(cursor)
db_investors = read_investor(cursor)

# Prints out results
bond_table_data = []
stock_table_data = []

# Calculate and add date to list for tabulate table
for stock in db_stocks:
    priceVariation = stock.calculate_loss_gain() # Calculate amount earned or lost    
    yearlyEarningsLoss = stock.calculate_yearly_earnings_loss() # Get yearly earnings loss

    stock_table_data.append([stock.investorID, stock.symbol, stock.noShares, priceVariation, yearlyEarningsLoss]) # For tabulate

for bond in db_bonds:
    priceVariation = bond.calculate_loss_gain() # Calculate amount earned or lost
    yearlyEarningsLoss = bond.calculate_yearly_earnings_loss() # Get yearly earnings loss

    bond_table_data.append([bond.investorID, bond.symbol, bond.noShares, priceVariation, yearlyEarningsLoss, bond.coupon, bond.the_yield]) # For tabulate

# Create Reports
try:
    Report.create_stock_report(my_investor.name, stock_table_data)
except:
    print('An error occured when printing the stock list')

try:
    Report.create_bond_report(my_investor.name, bond_table_data)
except:
    print('An error occured when printing the bond list')

# Create the line chart!
try:
    create_line_chart(stock_list)
except:
    print('An error occured when creating the line chart')


