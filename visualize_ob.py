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
import datetime
import numpy as np


#import csv, read in data frames, create arrays 
inputfile = './output.csv/obeverything_processed.csv'
df = pd.read_csv(inputfile, quoting=0, 
		parse_dates=['Date Order Received', 'Date Order Fulfilled', 'Date Payment Received'], 
		dayfirst=True)
#get unique book names
titles = df['Title'].unique()
#print(titles)

#Total Copies sold of each book
def plotTotalSale(df):
	df['Copies Ordered'] = pd.to_numeric(df['Copies Ordered'], errors='coerce')
	plt.figure(0)
	df.groupby(['Title'])[['Copies Ordered']].sum().plot.bar(title = 'Number of Copies Sold')
	plt.xlabel('Book Titles', fontsize = 10)
	plt.ylabel('Copies Sold', fontsize = 10)
	plt.show()

#Income per month
def computeIncome(df):
	df['Copies Ordered'] = pd.to_numeric(df['Copies Ordered'], errors='coerce')
	df['Pence'] = pd.to_numeric(df['Pence'], errors='coerce')
	df['Pounds'] = pd.to_numeric(df['Pounds'], errors='coerce')
	df['Shillings'] = pd.to_numeric(df['Shillings'], errors='coerce')
	nonull = df[df['Date Order Received'].notnull()]
	nonull = nonull[nonull['Date Order Received'] < datetime.date.today()  ]
	nonull = nonull[nonull['Date Order Received']  > datetime.datetime(1910,1,1)]
	income = nonull.groupby([pd.Grouper(key='Date Order Received', freq='M')])[['Pence','Pounds','Shillings']].sum()
	labels =income.index.get_level_values('Date Order Received')
	#Convert Pound, pence, Shillings into one unified unit
	# 12 pence in a shilling and 20 shillings, or 240 pence, in a pound
	income['total'] = income['Pounds'] + income['Pence']/240.0 + income['Shillings']/20.0
	plt.figure(1)
	income['total'].plot.bar(title = 'Monthly Income')
	index = np.arange(0,len(labels),6)
	label = labels[0:len(labels):6]
	plt.xticks( index,label, fontsize=5, rotation=30)
	plt.xlabel('Date', fontsize=10)
	plt.ylabel('Income (Pound)',  fontsize =10)
	#Add Cum sum income
	plt.figure(2)
	income['total'].cumsum().plot(title='Cumulative Income: 1927-1946')
	#plt.xticks( index,labels, fontsize=5, rotation=30)
	plt.xlabel('Date', fontsize=10)
	plt.ylabel('Income (Pound)',  fontsize =10)
	plt.show()


#plotTotalSale(df)
computeIncome(df)

