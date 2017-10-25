# Parse Drupal import log errors
import re
person = re.compile('No match for (\w+): (.*)\.')
image = re.compile('The specified file sites/all/modules/custom/mapp_data_import/images/(\w+\.\w+)')
names = list()
results = dict()
images = list()
with open('logs/errors.txt', 'r') as f:
	for line in f:
		result = None
		result = person.search(line)
		if result is not None:
			role = result.group(1)
			name = result.group(2)
			names.append(name)
			if name in results:
				results[name] += ', ' + role
			else:
				results[name] = role
		result = image.search(line)
		if result is not None:
			images.append(result.group(1))

names = sorted(set(names))
with open('logs/people.txt', 'w') as f:
	for name in names:
		f.write(name + "\n")
		# f.write("{} ({})\n".format(name, results[name]))
images = sorted(set(images))
with open('logs/images.txt', 'w') as f:
	for image in images:
		f.write(image + "\n")
