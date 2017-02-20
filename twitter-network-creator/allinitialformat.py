import sys
import json
import os
import secondaryformat
import twitter_folder_change

def typecheck(term_type, term):
	if term_type == 'hashtag':
		return '#' + term
	elif term_type == 'username' or term_type == 'text':
		return term
	else:
		sys.exit('USAGE: use either "hashtag", "handle", or "text" for type of term')

def search(values, searchFor):
	for k in values:
		if k['name'] == searchFor:
			return k
	return -1

def additional_group(value, additional_terms,term_type):
	terms_number = len(additional_terms)
	group = 0
	finder = ''
	group_list = []
	terms_list = []
	for i in range(0, terms_number):
		if term_type == 'text' or term_type == 'hashtag':
			val = value['text'].find(additional_terms[i])
			if val!= -1:
				group = group + i
				finder = value['text'][val: val + 2]
				group_list.append(i)
				terms_list.append(additional_terms[i])
				#print finder
		if term_type == 'username':
			if value['user']['screen_name'].find(additional_terms[i]) != -1:
				group = i
	print terms_list
	return [group_list, terms_list]

def create_circle_lists(groups, list_of_terms):
	print groups
	ratio = (float(1)/float(len(groups))) * len(list_of_terms)
	angles = []
	#print ratio
	for i in range(0, len(groups)):
		angles.append([i * ratio, (i + 1) * ratio, groups[i], 1])
	return angles

def combine_no_duplicates(first, second):
	for val1 in first:
		for val2 in second:
			if val1 == val2:
				second.remove(val2)
	return first + second

def firstformat(start_day, end_day, search_terms, filename, search_type):
	search_term = search_terms[0]
	additional_terms = search_terms
	day_user_data=[]
	index = 0
	for day in range(start_day, end_day):
		with open('twitter-network-creator/filtered_data/all'+str(day)+filename+'.json') as data_file:
		#with open('filtered_data/all10BlackLivesMatterAllLivesMatterMichaelBrownFergusonPolice.json') as data_file:	 
			data = json.load(data_file)
			for d in data:
				searchval=search(day_user_data, d['user']['screen_name'])
				sub_searched = additional_group(d, additional_terms, search_type)
				groups_in_tweet = sub_searched[0]
				terms_in_tweet = sub_searched[1]
				angles =  create_circle_lists(groups_in_tweet, search_terms)
				if searchval != -1:
					if 'retweeted_status' in d:
						searchval['links'].append(d['retweeted_status']['user']['screen_name'])
					searchval['score'] = searchval['score'] + 1
					searchval['text'].append(d['text'])
					searchval['tweets_in_text'] = combine_no_duplicates(searchval['tweets_in_text'], terms_in_tweet)#list(set(searchval['tweets_in_text']) - set(terms_in_tweet))
					searchval['group'] = combine_no_duplicates(searchval['group'], groups_in_tweet)
					searchval['angles'] = create_circle_lists(searchval['group'], search_terms)
					for angle in searchval['angles']:
						angle[3] = searchval['score']
				else:
					if 'retweeted_status' not in d:
						thing={
							'text' : [d['text']],
							'name': d['user']['screen_name'],
							'score': 1,
							'links': [],
							'group' : groups_in_tweet,#additional_group(d, additional_terms, search_type),
							'url' : d['id'],
							'index' : index,
							'retweets' : 0,
							'angles' : angles,
							'tweets_in_text': terms_in_tweet
							}
					else:
						thing={
							'text' : [d['text']],
							'name': d['user']['screen_name'],
							'score': 1,
							'links': [d['retweeted_status']['user']['screen_name']],
							'group' : groups_in_tweet,#additional_group(d, additional_terms, search_type),
							'url' : d['id'],
							'index' : index,
							'retweets' : 0,
							'angles' : angles,
							'tweets_in_text': terms_in_tweet
							}
						addnode=search(day_user_data, d['retweeted_status']['user']['screen_name'])
						if addnode == -1:
							index = index + 1
							newnode={
								'text' : [d['text']],
								'name': d['retweeted_status']['user']['screen_name'],
								'score': 1,
								'links': [],
								'group' : groups_in_tweet,#additional_group(d, additional_terms, search_type),
								'url' : d['retweeted_status']['id'],
								'index' : index,
								'retweets' : 0,
								'angles' : angles,
								'tweets_in_text': terms_in_tweet
								}
							day_user_data.append(newnode)
					index = index + 1
					day_user_data.append(thing)
		print day
	filename = 'all' + filename
	#with open('half_formatted_data/half_formatted'+ str(start_day) + '-' + str(end_day) + '-' + filename +'.json', 'w') as outfile:
	with open('twitter-network-creator/half_formatted_data/half_formatted'+ str(start_day) + '-' + str(end_day) + '-' + filename +'.json', 'w') as outfile:
		json.dump(day_user_data, outfile)
	secondaryformat.secondformat(start_day, end_day, search_terms, filename)

#firstformat(10, 11, ['BlackLivesMatter', 'AllLivesMatter', 'MichaelBrown', 'FergusonPolice'], 'BlackLivesMatterAllLivesMatterMichaelBrownFergusonPolice', 'hashtag')

	   # for x in day_user_data:
		#	if len(x['links']) > 1:
		#		print x['links']


