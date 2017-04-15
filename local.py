import json
# Processing
# with open('treasury.csv', 'r') as f:
# 	lines = f.readlines()
# 	with open('treasury1.csv', 'w+') as f1:
# 		l = 100000
# 		for i in range(l):
# 			print "{} out of {} complete".format(i, l)
# 			f1.write(lines[i])

# Analysis
# query = {'zipcode' : '03244'}
# keys = ['zipcode', 'dollarsobligated', 'fundingrequestingagencyid', 'effectivedate', 
# 		'contractactiontype', 'descriptionofcontractrequirement', 'vendorname', 'streetaddress',
# 		'city', 'state', 'productorservicecode', 'numberofemployees', 'unique_transaction_id']
# LIMIT = 1000

def filter(query, limit):
	with open('treasury1.csv', 'r') as f:
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
		print cat_nums
		assert len(cat_names) == len(cat_nums)

		for i in range(len(cat_names)):
			cat_name = cat_names[i]
			cat_num = cat_nums[i]
			# print "Filtering by {}".format(cat_name)
			for line in lines:
				try:
					l = line.split(',')
					cur_val = l[cat_num]
					search_val = query[cat_name]
					if cur_val == search_val:
						results.append(l)
					elif cat_name == 'zipcode':
						if len(str(cur_val)) < 9 and not len(str(cur_val)) == 5:
							cur_val = '0' + str(cur_val)
						if str(search_val) == cur_val[0:5]:
							results.append(l)

				except:
					print "Failed on query", l
		
		# print "Finished with {} results".format(len(results))
		return results

def extract(results, keys):
	categories = []
	cat_nums = []
	with open('treasury1.csv', 'r') as f:
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
