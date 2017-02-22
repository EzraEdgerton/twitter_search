PART 1 - Setup and unzip

1. Download file for the month you wish to explore. 

2. Unzip the tarball and copy the entire twitter-network-creator folder into the month folder. So if the month you downloaded is November 2014, then put it in the 11 folder that is within the 14 folder.

!!!!!!DO NOT change the name of the 'twitter-network-creator' folder.!!!!!!

3. Open terminal and make your working folder the one you just copied. (using 'cd *foldername*' to change and 'pwd' to see your current working directory. A helpful usage description is at the following link under 'File and Directory Commands' https://help.ubuntu.com/community/UsingTheTerminal )

4. input 'bash unzipper' into the terminal. This will take a minute as it unzips each of the individual data files for each minute in that month.


Part 2 - Filter the right range and format the json files.

1. Now that everything is set up and unzipped, choose your range of days and choose your search term.


2. To get the filtered and formatted data, run allsearch.py:

 	the first argument as the start day in the range you wish to search

 	the second argument as the end day in the range you wish to search  (inclusive)

 	the third term is an optional '-a' or '-all' which if included would run the search treating each of the subsequent search terms equally, rather than filtering out only tweets containing the first term.

 	the next arguments are the search terms you are looking for. If the search terms are hashtags (e.g. #BlackLivesMatter) include the hashtag with a preceding \, if it is a username or plain text just leave it as such. If this term includes spaces, every space must have a backslash immediately preceding it.

 	!!!! 
 	Remember, spaces  and special characters in terminal must be written with a preceding '\' otherwise they will be interpreted as seperate arguments.
 	If you wish to search for 'black lives matter,' then the proper input would be 'black\ lives\ matter'
 	!!!!

 	If you did not include the '-all' tag the first search term will be the main search term and each of the following search terms will be looking within tweets containing the main search term.

 	Otherwise, if the  '-all' tag is included, all tweets containing any of the search terms will be included

 	the final argument informs the program whether or not the search term is a hashtag, plain text in the tweet, or a username . If the search term is a hashtag or in the text, then the fourth argument should be 'text'. If the search term is a username then this argument should be 'username' 



EXAMPLES:

If I wanted to look at '#BlackLivesMatter' tweets from the third to the tenth of the month I would run:

	'python search.py 3 11 \#BlackLivesMatter text'

for only the fifth of the month I would run:

	'python search.py 5 6 \#BlackLivesMatter text'

If I wanted to look at tweets containing the phrase 'interesting find' in the first two weeks of a month I would run:

	'python search.py 1 15 interesting\ find text'

If I wanted to look at tweets by user '#BlackLivesMatter' for the first two weeks of a month, while changing node colors for tweets that also contain the tweets '#AllLivesMatter' and 'hello world' I would run:

	'python search.py 1 15 \#BlackLivesMatter \#AllLivesMatter hello\ world text'

And if I wanted to look at tweets for the first eight days of the month while changing node colors for tweets that contain '#BlackLivesMatter', '#AllLivesMatter,' '#ICantBreathe,' and '#HandsUpDontShoot' I would run:

	'python search.py 1 9 -a \#BlackLivesMatter \#AllLivesMatter 
	#ICantBreathe \#HandsUpDontShoot text'



!!!!If you want to use the older version, you still can use search.py unaltered, that readme is at searchREADME.txt


After this, your data will be filtered, formatted and stored in the 'formatted_data' folder with a name beginning with 'formatted' and followed by the date range and each by each of the search terms and the type.

Part 3 – Create Visualization

	1. Now that you've got the data file(s) formatted properly, you will need to copy 'twitter.html' which is in the 'twitter-network-creator' folder, rename it(without spaces in the name), and open it with a text editor. Keep this new file in the 'twitter-network-creator' folder.

	You can change the settings on TextEdit to open the file and see the html encoding with this tutorial (http://osxdaily.com/2013/01/14/view-html-source-code-textedit-mac-os-x/) or you can download an outside text editor like Sublime Text (my preferred text editor).

	2. After opening this file, go to line 82 (in TextEdit you can do this by hitting command+l and entering the line number) and change the filepath from "formatted_data/formatted.json" to "formatted_data/" + the name of the file you just created in Part 2. (e.g I would make this new filepath "formatted_data/formatted1-2-#BlackLivesMatter.json")

	3. It is time to create a simple server for this web page to run on. Back in terminal (making sure you are still in the 'twitter-network-creator' folder), run the command 'python -m SimpleHTTPServer'. This will start a local server running on port 8000 (most likely). It will tell you what port it is running on.

	4. Go to your favorite web browser and navigate to 'localhost:8000/twitter.html', replacing the 8000 with the port that you are running on and the twitter.html with what you named your new .html file. 

	5. Tweak it! To tweak the size of the enclosing box, size of the nodes, and distance between the nodes, go to lines 41-44 in the .html file. You will something like this:

			var width = 700,	-->	changes width of enclosing box
    			height = 700,	-->	changes height of enclosing box
    			radius = 10,	--> does something unimportant	
    			charge = -100,	-->	changes distance between nodes
    								and how much the nodes move. The closer to 0 the closer they are together. Once positive the nodes stop standing still. Keep negative if you enjoy your visual sanity.
    			linkDistance =30;--> does something unimportant
    			noderadius = 2; --> changes the size of the nodes.

    Play around with these numbers until you get the visualization that works best for you!
