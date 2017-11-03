'''
Parse order books data

Mike Widner <mikewidner@stanford.edu>
'''

import os
import re
import csv
import sys
import string
import argparse
import pandas as pd 


def parse_options():
    parser = argparse.ArgumentParser(
        description='Chunk files into different sizes')
    parser.add_argument('-i', dest='input', required=True,
                        help='Input file of data CSV')
    parser.add_argument('-o', dest='output', required=True,
                        help='Output path for results')
    parser.add_argument('-v', '--verbose', dest='verbose',
                        action='store_true', help='Verbose output')
    return parser.parse_args()


def check_output_path(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except OSError as err:
			print(err)


def fill_empties(df):
	''' Fill empty columns with appropriate values '''
	df['Author'].fillna(method='ffill', inplace=True)	# Fill down empty authors

	# Numeric values
	columns = ['Copies Ordered', 'Pounds', 'Shillings', 'Pence']
	for col in columns:
		df[col].fillna(0, inplace=True)

	# Strings
	columns = ['Markings', 'Hand', 'Comments', 'Code / Notes']
	for col in columns:
		df[col].fillna("", inplace=True)


def convert_dates(df):
	''' Convert columns with date into date types '''
	columns = ['Date Order Received', 'Date Order Fulfilled', 'Date Payment Received']
	for col in columns:
		df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
	return df


def find_crossrefs(df):
	''' 
	Traverse the cross-references given to figure out empty dates 
	'''
	# Find numbers in Purchaser field
	pattern = r"see (\d+)"
	df['Cross Reference'] = df['Purchaser'].str.extract(pattern, flags=re.IGNORECASE, expand=True)
	return df


def subtract_returned_copies(df):
	'''
	Find purchasers with numbers in them and "retd" or ""
	make the copies ordered a negative number
	sums should work correctly then
	'''
	pattern1 = r"retd\.? (\d+)"
	pattern2 = r"(\d+) (?:retd|\"|rd)"
	# Using two patterns to avoid having possible multiple groups
	df['Copies Returned'] = df['Purchaser'].str.extract(pattern1, flags=re.IGNORECASE, expand=False)
	df['Copies Returned'] = df['Purchaser'].str.extract(pattern2, flags=re.IGNORECASE, expand=False)
	return df

def sum_pounds_shillings_pence(df):
	pass


def clean_purchaser_entries(df):
	'''
	Regularize entries for purchasers
	'''
	# ADD: Tokenize names, if first token matches, do edit distance of second token
	# if close, automatically join; use longer label?
	pattern = r",.+$"
	df['Purchaser'] = df['Purchaser'].str.replace(pattern, '')
	pattern = r"\([^)]+\)$|\[[^\]]+\]" # remove ()[] at end of entry
	df['Purchaser'] = df['Purchaser'].str.replace(pattern, '')

	pattern = r"Bk\.?"
	df['Purchaser'] = df['Purchaser'].str.replace(pattern, 'Book')

	remove_punc = str.maketrans('', '', string.punctuation.replace('&', ''))
	df['Purchaser'] = df['Purchaser'].str.translate(remove_punc)
	df['Purchaser'] = df['Purchaser'].str.strip()
	return df


def write_purchasers(df, outpath):
	df['Purchaser'] = df['Purchaser'].astype(str)
	# df = clean_purchaser_entries(df)
	with open(os.path.join(outpath, 'purchasers.txt'), 'w') as outfile:
		for purchaser in sorted(df['Purchaser'].unique()):
			outfile.write(str(purchaser) + "\n")


def write_hand_date_ranges(df, outpath):
	'''
	Calculate and write min-max date ranges each hand is active
	'''
	pass


def load_dataframe(inputfile):
	df = pd.read_csv(inputfile, quoting=0, 
		parse_dates=['Date Order Received', 'Date Order Fulfilled', 'Date Payment Received'], 
		dayfirst=True)
	fill_empties(df)
	df = convert_dates(df)
	df['Copies Ordered'].apply(pd.to_numeric, errors='raise')
	return df


def write_work_purchaser_edges(df, filename):
	# TODO: Add header source, target, weight
	df[['Title', 'Purchaser', 'Copies Ordered']].groupby(['Title', 'Purchaser']).sum().to_csv(outpath)
	df_orders_by_year = df.groupby(df['Date Order Received'].dt.year)
	for year, group in df_orders_by_year:
		filename = 'work_purchaser_edges_' + str(int(year)) + '.csv'
		group.groupby(['Title', 'Purchaser']).sum().to_csv(filename)


def write_processed_data(df, infile, outpath):
	basename = os.path.basename(infile)
	(root, ext) = os.path.splitext(basename)
	df.to_csv(os.path.join(outpath, root + '_processed' + ext))


def main():
	options = parse_options()
	check_output_path(options.output)
	df = load_dataframe(options.input)
	df = find_crossrefs(df)
	df = subtract_returned_copies(df)
	# print(df[~df['Cross Reference'].isnull()].sample(n=100))
	write_processed_data(df, options.input, options.output)

	quit()
	write_purchasers(df, options.output)
	# write_work_purchaser_edges(df, os.path.join(options.output, filename))


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print("This script requires Python 3.")
        exit(-1)
    main()