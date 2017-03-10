"""
basicstats.py 
for formatting the appropriate filtered data generated from allsearch.py for use in general
visaulization using dc.js

USAGE:
first argument: 
		the filename(excluding the day at the beginning and the .json at the end)
		of the filtered data you wish to format

second through fourth (or fifth) from last argument:
		all of the terms you wish to create the formatted data for

fifth from last argument is an optional:
		if it is '-range' then allinitialformat will format the data in the day range as 
		one file.

		if not included then allinitialformat will create one formatted file for each 
		day in the range provided

fourth from last argument is an optional:
		'-info'
		will add the tweet text into the basic data



third from last argument:
		search type, either 'hashtag', 'text' or 'username'

second from last argument:
		first day in range

last argument: 
		last day in range (inclusive)

e.g.

if the data is stored in  files like 
	9allMondaysMondaysAreTheWorstBeginningOfTheWeekTwitterDays.json

and I want to format data for MondaysAreTheWorst and TwitterDays hashtags
from the 3rd to the 13th with each day stored in its own file I would run:

	python allinitialformat.py allMondaysMondaysAreTheWorstBeginningOfTheWeekTwitterDays MondaysAreTheWorst TwitterDays hashtag 3 14

If I wanted to do that same thing but store the entire range in one formatted file I would run:

	python allinitialformat.py allMondaysMondaysAreTheWorstBeginningOfTheWeekTwitterDays MondaysAreTheWorst TwitterDays -range hashtag 3 14

Stores data in the basic_stats folder

"""
import sys
import json
import os
import secondaryformat
import twitter_folder_change
import allinitialformat


arg_len = len(sys.argv)

day_range = False
subtractor = 3
if sys.argv[arg_len - 4] == '-range':
	day_range = True
	subtractor = 4

start_day =  int(sys.argv[arg_len - 2])
end_day = int(sys.argv[arg_len - 1])
searchtype = sys.argv[arg_len - 3]

filename = sys.argv[1]
terms = []


for t in range(1, arg_len - subtractor):
	terms.append(sys.argv[t])

print terms


def basicstats(start, end, terms, name, search_type):
	basic_data = []
	index = 0
	for day in range(start, end):
		with open('filtered_data/'+str(day)+filename+'.json') as data_file:
			data = json.load(data_file)
			for d in data:
				tags = allinitialformat.additional_group(d, terms, search_type)
				tag_groups = tags[0]
				tag_names = tags[1]
				retweeted = False
				if 'retweeted_status' in d:
					retweeted = True
				if 'created_at' in d:
					time_created = d['created_at']
				else:
					time_created = ''

				basic_data.append({
					'index': index,
					'name': d['user']['screen_name'],
					'time': time_created,
					'groups': tag_groups,
					'tags': tag_names,
					#'text': d['text'],
					'retweeted': retweeted
					})
				index = index + 1
	with open('basic_stats/'+ str(start_day) + '-' + str(end_day) + '-' + filename +'.json', 'w') as outfile:
		basic_stats_data = {
			'terms' : terms,
			'stats' : basic_data
		}
		json.dump(basic_stats_data, outfile)
		



if day_range:
	basicstats(start_day, end_day, terms, filename, searchtype)
else:
	for day in range(start_day, end_day):
		basicstats(day, day + 1, terms, filename, searchtype)