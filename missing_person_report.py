import csv
import os

directory = '/Users/widner/Projects/Freelance/MAPP/Data_Collection/data_sources/'
people = list()
found = list()
data_sources = ['business.csv', 'correspondence.csv', 'edition.csv', 'primary_object.csv', 'related_material.csv', 'work.csv']
columns = ['Recipient', 'Author', 'Person involved', 'Publisher', 'Illustrator', 'Printer', 'Owner', 'Reader']

# Populate list of known people
with open(directory + 'person-latest.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		people.append(row['name'])

people = set(people)
names = dict()

for filename in data_sources:
	with open(directory + filename) as csvfile:
		reader = csv.DictReader(csvfile)
		names[filename] = list()
		for row in reader:
			for col in columns:
				if col in row:
					if '|' in row[col]:
						found.extend(row[col].split('|'))
						names[filename].extend(row[col].split('|'))
					else:
						names[filename].append(row[col])
						found.append(row[col])

found = set(found)
missing = sorted(found - people)
for filename in names:
	print('--------- {} ---------'.format(filename))
	for person in missing:
		if person in names[filename]:
			print(person)
	# print(person)
print(len(missing))