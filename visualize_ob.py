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
import matplotlib.dates as mdates
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
	df.groupby(['Title'])[['Copies Ordered']].sum().sort_values('Copies Ordered').plot.barh(title = 'Number of Copies Sold')
	plt.ylabel('Book Titles', fontsize = 10)
	plt.xlabel('Copies Sold', fontsize = 10)
	#plt.savefig('totalCopies.png', bbox_inches='tight',dpi=100)
	plt.show()

#Income per month
def computeIncome(df):
	nonull = df[df['Date Order Received'].notnull()]
	nonull = nonull[nonull['Date Order Received'] < datetime.date.today()  ]
	nonull = nonull[nonull['Date Order Received']  > datetime.datetime(1910,1,1)]
	income = nonull.groupby([pd.Grouper(key='Date Order Received', freq='M')])[['Pence','Pounds','Shillings']].sum()
	labels =income.index.get_level_values('Date Order Received').strftime('%m/%d/%Y')
	incomeY = nonull.groupby([pd.Grouper(key='Date Order Received', freq='Y')])[['Pence','Pounds','Shillings']].sum()
	#Convert Pound, pence, Shillings into one unified unit
	# 12 pence in a shilling and 20 shillings, or 240 pence, in a pound
	income['total'] = income['Pounds'] + income['Pence']/240.0 + income['Shillings']/20.0
	#incomeY['total'] = incomeY['Pounds'] + incomeY['Pence']/240.0 + incomeY['Shillings']/20.0
	fig = plt.figure()
	fig.add_subplot(111)
	ax = income['total'].plot.bar(title = 'Monthly Income',color = 'red')
	income['total'].cumsum().plot(ax = ax, xticks = labels)
	index = np.arange(0,len(labels),6)
	label = labels[0:len(labels):6]
	plt.xticks( index,label, fontsize=5, rotation=30)
	myFmt = mdates.DateFormatter('%d')
	#ax.xaxis.set_major_formatter(myFmt)
	plt.xlabel('Date', fontsize=10)
	plt.ylabel('Income (Pound)',  fontsize = 10)
	plt.show()
	#plt.savefig('monthlyincome.png', bbox_inches='tight',dpi=100)
	
	#Add Cum sum income
	fig = plt.figure()
	income['total'].cumsum().plot(title='Cumulative Income: 1927-1946')
	plt.xlabel('Date', fontsize=10)
	plt.ylabel('Income (Pound)',  fontsize =10)
	#plt.savefig('cumsumIncome.png', bbox_inches='tight',dpi=100)
	
	#stacked bar charts for total income per month and per year showing which work contributes the most
	fig = plt.figure()
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
	volume = df.groupby(['Purchaser'])[['Copies Ordered']].sum().sort_values('Copies Ordered')
	volumebP = volume[volume >THRESHOLD]
	volumebP =volumebP.dropna()
	# plot chart
	fig = plt.figure()
	volumebP.plot.barh(title = 'Purcharser by volume')
	plt.yticks( fontsize=5)
	plt.savefig('volume.png', bbox_inches='tight',dpi=100)
	plt.show()

#Chart showing average, min, and max time between order filled and payment received per work and total
def diffFilledPayment(df):
	#Found weird discrepancies in data: Date Payment received parsed incorrectly with dates not matching the spreadsheet
	weirdEntries = df[df['Date Payment Received'] > datetime.datetime(1950,1,1)]
	weirdEntries2 = df[df['Date Payment Received'] < datetime.datetime(1920,1,1)]
	#Temoprarily ignore discrepancies
	df = df[df['Date Payment Received'] < datetime.datetime(1950,1,1)]
	df = df[df['Date Payment Received'] > datetime.datetime(1920,1,1)]
	df['Date Order Fulfilled'] = pd.to_datetime(df['Date Order Fulfilled'])
	df['Date Payment Received'] = pd.to_datetime(df['Date Payment Received'])
	df['diff'] = df['Date Payment Received'] - df['Date Order Fulfilled']
	#print(df['diff'].describe())
	print(df[df['diff'].min()== df['diff']])

#Finding discrepancies in the data frame, mostly in date field
#Generates error report
def detectAnomalies(df):
	print("Finding Discrepancies....")
	print("Checking for abnormal dates in entries")
	weirdEntries = df[df['Date Payment Received'] > datetime.datetime(1950,1,1)]
	weirdEntries2 = df[df['Date Payment Received'] < datetime.datetime(1920,1,1)]
	print("Error in Date Payment Received")
	print(weirdEntries)
	print(weirdEntries2)

	weirdEntries3= df[df['Date Order Received'] < datetime.datetime(1920,1,1)]
	weirdEntries4= df[df['Date Order Received']  > datetime.datetime(1950,1,1)]
	print("Error in Date Order Received")
	print(weirdEntries3)
	print(weirdEntries4)

	#weirdEntries5 = df[df['Date Order Fulfilled'] < datetime.datetime(1920,1,1)]
	#weirdEntries6= df[df['Date Order Fulfilled']  > datetime.datetime(1950,1,1)]
	print("Error in Date Order Fufilled")
	#print(weirdEntries5)
	#print(weirdEntries6)
	frames =  [weirdEntries, weirdEntries2, weirdEntries3, weirdEntries4]
	output = pd.concat(frames)
	output.to_csv('errorReport.csv')

#Tabular data with mean and max price for a book wrt to its marking
def groupByMarking(df):
	
	
	df['total'] = df['Pounds'] + df['Pence']/240.0 + df['Shillings']/20.0
	df['Copies Ordered'] = pd.to_numeric(df['Copies Ordered'], errors='coerce')
	df['total'] = pd.to_numeric(df['total'], errors='coerce')
	#df['average'] = df['total'].truediv(df['Copies Ordered'],fill_value = None)
	describ = df.groupby(['Title', 'Code / Notes'])['average'].describe()
	#describ.to_csv('groupByMarkingReport.csv')



#plotTotalSale(df)
#computeIncome(df)
#purchaserVolume(df)
#diffFilledPayment(df)
#detectAnomalies(df)
groupByMarking(df)

