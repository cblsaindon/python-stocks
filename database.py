"""
 Developer: Candace Stokes
 Last Updated: 06/06/2024
 Description: Contains the class and methods required for the database calls
"""

from stock import Stock, Bond
from investor import Investor

import sqlite3

def establish_sql_connection():
    connection = sqlite3.connect('investments.db')
    return connection.cursor()

def drop_tables(cursor):
    """Takes in database cursor, executes sql drop commands."""
    sql_drop_stock = "DROP TABLE stock;"
    sql_drop_bond = "DROP TABLE bond;"
    sql_drop_investor = "DROP TABLE investor;"
    sql_drop_stockprice = "DROP TABLE stockprice;"
    cursor.execute(sql_drop_stock)
    cursor.execute(sql_drop_bond)
    cursor.execute(sql_drop_investor)
    cursor.execute(sql_drop_stockprice)

def create_tables(cursor):
    """Takes in database cursor, executes sql drop commands."""
    # Create SQLite Tables
    sql_create_stock_table = """ CREATE TABLE IF NOT EXISTS stock (
                                            stockID integer PRIMARY KEY,
                                            symbol text NOT NULL,
                                            noShares integer NOT NULL,
                                            purchasePrice integer NOT NULL,
                                            currentValue integer NOT NULL,
                                            purchaseDate datetime NOT NULL,
                                            investorID integer NULLABLE
                                        );"""
    
    sql_create_bond_table = """ CREATE TABLE IF NOT EXISTS bond (
                                            bondID integer PRIMARY KEY,
                                            symbol text NOT NULL,
                                            noShares integer NOT NULL,
                                            purchasePrice integer NOT NULL,
                                            currentValue integer NOT NULL,
                                            purchaseDate datetime NOT NULL,
                                            investorID integer NULLABLE,
                                            coupon integer NULLABLE,
                                            yield integer NULLABLE
                                        );"""

    sql_create_investor_table = """ CREATE TABLE IF NOT EXISTS investor (
                                            investorID integer PRIMARY KEY,
                                            name text NOT NULL,
                                            address text NOT NULL,
                                            phoneNumber text NOT NULL
                                        );"""

    sql_create_stockprice_table = """ CREATE TABLE IF NOT EXISTS stockprice (
                                            symbol text NOT NULL,
                                            date datetime NOT NULL,
                                            open integer NOT NULL,
                                            high integer NOT NULL,
                                            low integer NOT NULL,
                                            close integer NOT NULL,
                                            volume integer NOT NULL
                                        );"""
    
    cursor.execute(sql_create_stock_table)
    cursor.execute(sql_create_bond_table)
    cursor.execute(sql_create_investor_table)
    cursor.execute(sql_create_stockprice_table)

def write_data(cursor, stock_list, bond_list, investor_list, stockprice_list):
    """Takes in stock and bond related data, inserts into sql."""
    # Stock Price - Prepare a parameterized SQL statement
    sql_insert_stockprice = """INSERT INTO stockprice (
        symbol, date, open, high, low, close, volume
    ) VALUES (?, ?, ?, ?, ?, ?, ?);"""

    # Insert each stock in the list
    for stockPrice in stockprice_list:
        stockprice_data = (
            stockPrice.symbol,
            stockPrice.date,  # This is a datetime object
            stockPrice.open,
            stockPrice.high,
            stockPrice.low,
            stockPrice.close,
            stockPrice.volume
        )
        cursor.execute(sql_insert_stockprice, stockprice_data)

    # Prepare a parameterized SQL statement
    sql_insert_stock = """INSERT INTO stock (
        stockID, symbol, noShares, purchasePrice, currentValue, purchaseDate, investorID
    ) VALUES (?, ?, ?, ?, ?, ?, ?);"""

    # Insert each stock in the list
    for stock in stock_list:
        stock_data = (
            stock.stockID,
            stock.symbol,
            stock.noShares,
            stock.purchasePrice,
            stock.currentValue,
            stock.purchaseDate,  # This is a datetime object
            stock.investorID
        )
        cursor.execute(sql_insert_stock, stock_data)

   # Parameterized SQL statement for inserting bonds
    sql_insert_bond = """
    INSERT INTO bond (
        bondID, symbol, noShares, purchasePrice, currentValue, purchaseDate, investorID, coupon, yield
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    # Execute and commit bond data
    for bond in bond_list:
        bond_data = (
            bond.stockID,
            bond.symbol,
            bond.noShares,
            bond.purchasePrice,
            bond.currentValue,
            bond.purchaseDate,
            bond.investorID,
            bond.coupon,
            bond.the_yield
        )
        cursor.execute(sql_insert_bond, bond_data)

        for investor in investor_list:
            sql_insert_investor = "INSERT INTO investor VALUES(" + str(investor.investorID)
            sql_insert_investor = sql_insert_investor + ", '" + investor.name + "'"
            sql_insert_investor = sql_insert_investor + ", '" + investor.address + "'"
            sql_insert_investor = sql_insert_investor + ", '" + investor.phoneNumber +"');"       
    cursor.execute(sql_insert_investor)

    # Commit changes
    cursor.connection.commit()

def read_stock(cursor):
    """Takes in database cursor, grabs stock database data."""
    sql_select = "SELECT * FROM STOCK;"
    db = []

    for record in cursor.execute(sql_select):
        new_db = Stock(record[1], record[2], record[3], record[4], record[5], record[6])
        db.append(new_db)
    return db

def read_bond(cursor):
    """Takes in database cursor, grabs bond database data."""
    sql_select = "SELECT * FROM BOND;"
    db = []

    for record in cursor.execute(sql_select):
        new_db = Bond(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8])
        db.append(new_db)
    return db

def read_investor(cursor):
    """Takes in database cursor, grabs investor data."""
    sql_select = "SELECT * FROM INVESTOR;"
    db = []

    for record in cursor.execute(sql_select):
        new_db = Investor(record[0], record[1], record[2], record[3])
        db.append(new_db)
    return db