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
df['Copies Ordered'] = pd.to_numeric(df['Copies Ordered'], errors='coerce')
df['Pence'] = pd.to_numeric(df['Pence'], errors='coerce')
df['Pounds'] = pd.to_numeric(df['Pounds'], errors='coerce')
df['Shillings'] = pd.to_numeric(df['Shillings'], errors='coerce')


#TODO Write function to collapse titles to clean up bar charts
def collapseTitles(df):
	#get unique book names
	titles = df['Title'].unique()
	#print(titles)
	pass

#Total Copies sold of each book
def plotTotalSale(df):
	plt.figure(0)
	df.groupby(['Title'])[['Copies Ordered']].sum().plot.bar(title = 'Number of Copies Sold')
	plt.xlabel('Book Titles', fontsize = 10)
	plt.ylabel('Copies Sold', fontsize = 10)
	#plt.savefig('totalCopies.png')
	plt.show()

#Income per month
def computeIncome(df):
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
	#plt.savefig('monthlyincome.png')
	#Add Cum sum income
	fig = plt.figure(2)
	income['total'].cumsum().plot(title='Cumulative Income: 1927-1946')
	plt.xlabel('Date', fontsize=10)
	plt.ylabel('Income (Pound)',  fontsize =10)
	#plt.savefig('cumsumIncome.png')
	
	#stacked bar charts for total income per month and per year showing which work contributes the most
	fig = plt.figure(3)
	incomeByTitle = nonull.groupby([pd.Grouper(key='Date Order Received', freq='Y'), 'Title'])[['Pence','Pounds','Shillings']].sum()
	incomeByTitle['total'] = incomeByTitle['Pounds'] + incomeByTitle['Pence']/240.0 + incomeByTitle['Shillings']/20.0
	unstacked = incomeByTitle['total'].unstack('Title')
	unstacked.plot.bar(title = 'Yearly Income stacked bar char', stacked = True)
	plt.xticks( fontsize=5, rotation=30)
	incomeByTitleM = nonull.groupby([pd.Grouper(key='Date Order Received', freq='M'), 'Title'])[['Pence','Pounds','Shillings']].sum()
	incomeByTitleM['total'] = incomeByTitleM['Pounds'] + incomeByTitleM['Pence']/240.0 + incomeByTitleM['Shillings']/20.0
	unstacked = incomeByTitleM['total'].unstack('Title')
	unstacked.plot.bar(title = 'Monthly Income stacked bar char', stacked = True)
	plt.xticks( index,label, fontsize=5, rotation=30)
	plt.show()

#barchart for purchaser by volume
def purchaserVolume(df):
	THRESHOLD = 200.0
	
	volume = df.groupby(['Purchaser'])[['Copies Ordered']].sum()
	volumebP = volume[volume >THRESHOLD]
	volumebP =volumebP.dropna()
	# plot chart
	fig = plt.figure(4)
	volumebP.plot.pie(y = 'Copies Ordered',labels = volumebP.index.get_level_values('Purchaser'), legend = False,  autopct='%1.1f%%')
	#plt.savefig('volume.png')
	plt.show()

#Chart showing average, min, and max time between order filled and payment received per work and total
def diffFilledPayment(df):
	df['Date Order Fulfilled'] = pd.to_datetime(df['Date Order Fulfilled'])
	df['Date Payment Received'] = pd.to_datetime(df['Date Payment Received'])
	df['diff'] = df['Date Payment Received'] - df['Date Order Fulfilled']
	print(df['diff'].describe())
	print(df[df['diff'].max()== df['diff']])
	#Found weird discrepancies in data: Date Payment received parsed incorrectly with dates not matching the spreadsheet
	weirdEntries = df[df['Date Payment Received'] > datetime.datetime(1950,1,1)]


#plotTotalSale(df)
#computeIncome(df)
#purchaserVolume(df)
diffFilledPayment(df)

