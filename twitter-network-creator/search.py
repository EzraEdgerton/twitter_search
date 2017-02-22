# All this created by Ezra Edgerton June-September 2016 for the University of Cincinnati. Copyright etc. to me.
#
#
import sys
import os
import json
import allinitialformat
import secondaryformat
import twitter_folder_change

start_day =  int(sys.argv[1])
end_day = int(sys.argv[2])

search_term = sys.argv[3]

search_type = sys.argv[4]

argument_len = len(sys.argv)

additional_terms = []

filename = search_term

if argument_len > 5: 
	for i in range(5, argument_len - 1):
		additional_terms.append(sys.argv[i])
sub_search_type = sys.argv[argument_len - 1]

for i in additional_terms:
	filename = filename + i

print filename

search_term = allinitialformat.typecheck(search_type,search_term)


twitter_folder_change.network_directory_parent()


for day in range(start_day, end_day):
	tweets=[]
	if day < 10:
		daystring='0' + str(day)
	else:
		daystring=str(day)
	for hour in range(0, 24):
		if hour < 10:
				hourstring='0'+str(hour)
		else:
			hourstring=str(hour)
		for minute in os.listdir(daystring+'/'+hourstring):
			if minute.startswith('.'):
				continue
			if minute < 10:
				minutestring='0'+str(minute)
			else:
				minutestring=str(minute)
			print str(day)+'/'+hourstring+'/'+minutestring
			for line in open(daystring+'/'+hourstring+'/'+minutestring, 'r'):
				tweet = json.loads(line)
				if search_type == 'username':
					if 'user' not in tweet:
						continue
					if tweet['user']['screen_name'].find(search_term) != -1:
						print tweet["text"]
						print tweet['user']['screen_name']
						tweets.append(tweet)
				else:
					if "text" not in tweet:
						continue
					if tweet["text"].find(search_term) != -1:
						print tweet["text"]
						tweets.append(tweet)


	with open('twitter-network-creator/filtered_data/'+str(day)+filename + '.json', 'w') as outfile:
		json.dump(tweets, outfile, indent=4)
search_terms = [search_term]
for i in additional_terms:
	search_terms.append(i)
allinitialformat.firstformat(start_day, end_day, search_terms, filename, sub_search_type)


