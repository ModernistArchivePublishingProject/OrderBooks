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
df['Copies Ordered'].convert_objects(convert_numeric=True)
#print(df['Copies Ordered'].sum())
df.groupby(['Title'])[['Copies Ordered']].count().plot.bar(title = 'Number of Transactions per book')
#counts.plot(kind='bar',title = 'Bar chart for book sales')
plt.show()

