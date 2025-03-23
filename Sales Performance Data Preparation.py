#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import sqlite3

# Load the dataset
file_path = "C:/Users/tejas/OneDrive/Desktop/Pet Projects/Sales Performance dashboard/sales_data.csv"
sales_df = pd.read_csv(file_path)
print(sales_df.head())


# In[3]:


# Data cleaning

# Check for missing values
print(sales_df.isnull().sum())

# Drop rows with missing crucial information
sales_df.dropna(subset=['Product ID', 'Order Date', 'Profit', 'Customer Name'], inplace=True)

# Convert date columns to datetime
sales_df['Order Date'] = pd.to_datetime(sales_df['Order Date'], format='%Y-%m-%d')
sales_df['Ship Date'] = pd.to_datetime(sales_df['Ship Date'], format='%Y-%m-%d')

# Change date format to dd/mm/yyyy
sales_df['Order Date'] = sales_df['Order Date'].dt.strftime('%d/%m/%Y')
sales_df['Ship Date'] = sales_df['Ship Date'].dt.strftime('%d/%m/%Y')

# Normalize text data (strip whitespaces, convert to lowercase)
sales_df['Category'] = sales_df['Category'].str.strip().str.lower()
sales_df['Status'] = sales_df['Status'].str.strip().str.lower()

# Handle duplicates if any
sales_df.drop_duplicates(inplace=True)


# In[4]:


# Create a SQLite database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Create a table for sales data
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    ProductID TEXT,
    ProductName TEXT,
    QuantitySold INTEGER,
    Price REAL,
    Profit REAL,
    Discount REAL,
    OrderDate DATE,
    ShipDate DATE,
    Category TEXT,
    Status TEXT,
    City TEXT,
    State TEXT,
    PostalCode TEXT,
    CustomerName TEXT,
    CustomerEmail TEXT,
    PaymentMethod TEXT,
    DeliveryPartner TEXT,
    OrderTime TEXT,
    FeedbackRating REAL,
    SKU TEXT
)
''')

# Insert the data into the table
sales_df.to_sql('sales', conn, if_exists='replace', index=False)


# In[5]:


# Sql queries for analysis

# Sales Trends Over Time
query = '''
SELECT strftime('%Y-%m', DATE([Order Date], 'start of month')) AS Month, 
       SUM(Price) AS TotalRevenue
FROM sales
GROUP BY Month
ORDER BY Month;
'''
sales_trends = pd.read_sql(query, conn)
print(sales_trends)


# In[6]:


# Top 5 Products by Revenue

query = '''
SELECT [Product Name] AS ProductName, SUM(Profit) AS TotalProfit
FROM sales
GROUP BY [Product Name]
ORDER BY TotalProfit DESC
LIMIT 5;
'''
top_products = pd.read_sql(query, conn)
print(top_products)


# In[7]:


# Customer Segmentation by Feedback Rating

query = '''
SELECT [Feedback Rating] AS FeedbackRating, COUNT(*) AS CustomerCount
FROM sales
GROUP BY [Feedback Rating]
ORDER BY FeedbackRating DESC;
'''
customer_segments = pd.read_sql(query, conn)
print(customer_segments)


# In[8]:


# Return Analysis

query = '''
SELECT Status, COUNT(*) AS ReturnCount
FROM sales
WHERE LOWER(Status) = 'returned'
GROUP BY Status;
'''
returns_data = pd.read_sql(query, conn)
print(returns_data)


# In[9]:


# Closing connection 

conn.close()


# In[10]:


sales_df.to_excel('C:/Users/tejas/OneDrive/Desktop/Pet Projects/Sales Performance dashboard/final_sales_data.xlsx', index=False)

