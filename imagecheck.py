import csv
has_image = list()
no_image = list()
with open('/Users/widner/Projects/Freelance/MAPP/Data_Collection/data_sources/work.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['Image'] == '':
			no_image.append(row['title'])
		else:
			has_image.append(row['title'])

for title in sorted(set(no_image)):
	print(title)

print('--- HAS IMAGE ---')
for title in sorted(set(has_image)):
	print(title)