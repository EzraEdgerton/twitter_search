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

def additional_group(value, additional_terms):
	terms_number = len(additional_terms)
	group = 1
	if terms_number < 1:
		return group

	term_type = additional_terms[terms_number - 1]
	if term_type == 'text':
		for i in range(0, terms_number - 1):
			if value['text'].find(additional_terms[i]) != -1:
				if group == 1:
					group =  i + 2
				else:
					group = group + i
	if term_type == 'username':
		for i in range(0, terms_number - 1):
			if value['user']['screen_name'].find(additional_terms[i]) != -1:
				if group == 1:
					group =  i + 2
				else:
					group = group + i
	return group

#	if value['text'].find('#AllLivesMatter') != -1:
#		return 2
#	if value['text'].find('#ICantBreathe') != -1:
#		return 3
#	if value['text'].find('#HandsUpDontShoot') != -1:
#		return 4
#	else:
#		return 1

def firstformat(start_day, end_day, search_term, additional_terms, filename):
	day_user_data=[]
	index = 0
	for day in range(start_day, end_day):
		with open('twitter-network-creator/filtered_data/'+str(day)+filename+'.json') as data_file:    
		    data = json.load(data_file)
		    for d in data:

		    	searchval=search(day_user_data, d['user']['screen_name'])
		    	if searchval != -1:
		    		if 'retweeted_status' in d:
		    			searchval['links'].append(d['retweeted_status']['user']['screen_name'])
					searchval['score'] = searchval['score'] + 1
					searchval['text'].append(d['text'])
					searchval['group'] = additional_group(d, additional_terms)
		    	else:
		    		if 'retweeted_status' not in d:
			    		thing={
				    		'text' : [d['text']],
			    			'name': d['user']['screen_name'],
			    			'score': 1,
			    			'links': [],
			    			'group' : additional_group(d, additional_terms),
			    			'url' : d['id'],
			    			'index' : index,
			    			'retweets' : 0
			    			}
			    	else:
			    		thing={
			    			'text' : [d['text']],
			    			'name': d['user']['screen_name'],
			    			'score': 1,
			    			'links': [d['retweeted_status']['user']['screen_name']],
			    			'group' : additional_group(d, additional_terms),
			    			'url' : d['id'],
			    			'index' : index,
			    			'retweets' : 0
			    			}
			    		addnode=search(day_user_data, d['retweeted_status']['user']['screen_name'])
			    		if addnode == -1:
			    			index = index + 1
			    			newnode={
				    			'text' : [d['text']],
				    			'name': d['retweeted_status']['user']['screen_name'],
				    			'score': 1,
				    			'links': [],
				    			'group' : additional_group(d, additional_terms),
				    			'url' : d['retweeted_status']['id'],
				    			'index' : index,
			    				'retweets' : 0
			    				}
			    			day_user_data.append(newnode)
			    	index = index + 1
		    		day_user_data.append(thing)

		    print day
	with open('twitter-network-creator/half_formatted_data/half_formatted'+ str(start_day) + '-' + str(end_day) + '-' + filename +'.json', 'w') as outfile:
		json.dump(day_user_data, outfile)
	secondaryformat.secondformat(start_day, end_day, search_term, filename)


	   # for x in day_user_data:
	    #	if len(x['links']) > 1:
	    #		print x['links']


