import json
# Processing
# with open('treasury1.csv', 'r') as f:
# 	lines = f.readlines()
# 	with open('treasury.csv', 'w+') as f1:
# 		l = 1000
# 		for i in range(l):
# 			# print "{} out of {} complete".format(i, l)
# 			f1.write(lines[i])

# Analysis
# query = {'zipcode' : '03244'}
# keys = ['zipcode', 'dollarsobligated', 'fundingrequestingagencyid', 'effectivedate', 
# 		'contractactiontype', 'descriptionofcontractrequirement', 'vendorname', 'streetaddress',
# 		'city', 'state', 'productorservicecode', 'numberofemployees', 'unique_transaction_id']
# LIMIT = 1000

def intersect(results):
	intersection = []
	smallest_set = results[0]

	for subset in results:
		if len(subset) < len(smallest_set):
			smallest_set = subset
	for line in smallest_set:
		for subset in results:
			for l in subset:
				try:
					if line[0] == l[0]:
						intersection.append(l)

	return intersection

def filter(query, limit):
	with open('treasury.csv', 'r') as f:
		lines = f.readlines()
		lines = lines[0:limit]
		categories = lines[0].split(',')
		cat_nums = []
		cat_names = []

		for q in query:
			for i, category in enumerate(categories):
				if str(category) == str(q):
					cat_nums.append(i)
					cat_names.append(category)

		results = []
		assert len(cat_names) == len(cat_nums)

		for i in range(len(cat_names)):
			results.append([])
			cat_name = cat_names[i]
			cat_num = cat_nums[i]
			append_or_not = False
			# print "Filtering by {}".format(cat_name)
			for line in lines[1:]:
				# try:
				l = line.split(',')
				cur_val = l[cat_num]
				search_val = query[cat_name]
				if cat_name == 'zipcode':
					if len(str(cur_val)) < 9 and not len(str(cur_val)) == 5:
						cur_val = '0' + str(cur_val)
					if str(search_val[0:2]) == cur_val[0:2]:
						append_or_not = True
				elif cat_name == 'principalnaicscode':
					if int(str(search_val)[0:2]) == int(str(cur_val)[0:2]):
						append_or_not = True
				elif cat_name == 'numberofemployees':
					if search_val == 'under 10 employees':
						if int(cur_val) < 10:
							append_or_not = True
					elif search_val == '10 - 100 employees':
						if int(cur_val) >= 10 and int(cur_val) <= 100:
							append_or_not = True
					elif search_val == 'over 100 employees':
						if int(cur_val) > 1000:
							append_or_not = True
				elif cur_val == search_val:
					append_or_not = True

				if append_or_not:
					results[i].append(l)
				# except:
				# 	print "Failed on query"
		
		# print "Finished with {} results".format(len(results))
		print "There are {} results".format(len(results[0]))
		return intersect(results)

def extract(results, keys):
	categories = []
	cat_nums = []
	with open('treasury.csv', 'r') as f:
		lines = f.readlines()
		categories = lines[0].split(',')
		for key in keys:
			for i, category in enumerate(categories):
				if key == category:
					cat_nums.append(i)

	json_dict = {}
	# print "Extracting {} results".format(len(results))
	for i, result in enumerate(results):
		json_dict[str(i)] = {}
		for c in range(len(cat_nums)):
			json_dict[str(i)][categories[cat_nums[c]]] = result[cat_nums[c]]

	# with open('templates/data.json', 'w') as outfile:
	# 	json.dump(json_dict, outfile, indent=2)
	return json.dumps(json_dict, indent=2)

def filter_and_extract(query, keys, limit=1000):
	r = filter(query, limit)
	return extract(r, keys)
