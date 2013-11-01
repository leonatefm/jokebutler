# Jester Dateset reference:
# http://eigentaste.berkeley.edu/dataset/
# Eigentaste: A Constant Time Collaborative Filtering Algorithm. Ken Goldberg, Theresa Roeder, Dhruv Gupta, and Chris Perkins. Information Retrieval, 4(2), 133-151. July 2001.

# Jester Dataset Description
# 
# Over 1.7 million continuous ratings (-10.00 to +10.00) of 150 jokes from 59,132 users: collected between November 2006 - May 2009
# 
# Save to disk, then unzip: jester_dataset_2.zip (7.7MB)
# 
# Format:
# 
# jester_ratings.dat: Each row is formatted as [User ID] [Item ID] [Rating]
# jester_items.dat: Maps item ID's to jokes
# Note that the ratings are real values ranging from -10.00 to +10.00. As of May 2009, the jokes {7, 8, 13, 15, 16, 17, 18, 19} are the "gauge set" (as discussed in the Eigentaste paper) and the jokes {1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 14, 20, 27, 31, 43, 51, 52, 61, 73, 80, 100, 116} have been removed (i.e. they are never displayed or rated).

#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import recommendations

# Read rating data from jester_ratings.dat

with open('jester_ratings.dat','rU') as rating_data:
    rating_list = list()
    for line in rating_data:
      rating_list.append(line.strip().split('\t\t'));

# format rating data into critics

rating_critics = dict()

for line in rating_list:
    userid = int(line[0])
    jokeid = int(line[1])
    rating = float(line[2])
    
    if rating_critics.has_key(userid):
        rating_critics[userid][jokeid] = rating
    else:
        rating_critics[userid] = {}
        rating_critics[userid][jokeid] = rating


# Build the Item Comparison Dataset for item-based recommendation       
similarjokes = recommendations.calculateSimilarItems(rating_critics, n=10)
print similarjokes



# Read joke data from jester_ratings.dat

with open('jester_items.dat','rU') as joke_data:
    joke_set = dict()
    joke_list = joke_data.read().split('\n\n')
    for joke in joke_list[0:150]:
        joke = joke.replace('\n','')
        result = re.search(r'(\d*?):(.*)', joke)
        joke_set[int(result.group(1))] = result.group(2)
        
print joke_set 
      
      
      