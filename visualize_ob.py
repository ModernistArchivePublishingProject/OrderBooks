'''
Visualize Orderbook data
Cherie Xu <cxuhan@stanford.edu>
'''

import os
import re
import csv
import sys
import string
import pandas as pd
import matplotlib.pyplot as plt
import collections


#import csv, read in data frames, create arrays 
inputfile = './output.csv/obeverything_processed.csv'
df = pd.read_csv(inputfile, quoting=0, 
		parse_dates=['Date Order Received', 'Date Order Fulfilled', 'Date Payment Received'], 
		dayfirst=True)
#get unique book names
titles = df['Title'].unique()
print(titles)
count = dict.fromkeys(titles,0)
# Get sales count for each book titles
# Get two dfs
copies = {}
#df['Copies Ordered'].convert_objects(convert_numeric=True)
#print(df['Copies Ordered'].sum())
df['Date Order Received'] = pd.to_datetime(df['Date Order Received'], errors = 'coerce', origin = '1920-01-01')
df['Copies Ordered'] = pd.to_numeric(df['Copies Ordered'], errors='coerce')
df['Pence'] = pd.to_numeric(df['Pence'], errors='coerce')
df['Pounds'] = pd.to_numeric(df['Pounds'], errors='coerce')
df['Shillings'] = pd.to_numeric(df['Shillings'], errors='coerce')
df[['Pence','Pounds','Shillings']].fillna(0)
print(df [['Pence','Pounds','Shillings']])
#df.groupby(['Title'])[['Copies Ordered']].sum().plot.bar(title = 'Number of Transactions per book')
#print (df.groupby(['Title', pd.Grouper(key='Date Order Received', freq='M')])[['Copies Ordered']].sum())
#counts.plot(kind='bar',title = 'Bar chart for book sales')
#plt.show()
#Show income per month
print (df.groupby([pd.Grouper(key='Date Order Received', freq='M')])[['Pence','Pounds','Shillings']].sum())

