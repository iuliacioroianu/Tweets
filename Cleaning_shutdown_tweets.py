# -*- coding: utf-8 -*-
"""
Clean Shutdown tweets

Remove punctuation
Turn to lower case
Remove stopwords (words that are very common in English, prepozitions, etc)
Lemmatize (get simplified common form of words)

TO DO: Create a list of slang words and abbreviations and replace them. Extract collocations. 

@author: Iulia
"""

import nltk, csv, glob, os

wnl = nltk.WordNetLemmatizer()
from nltk.corpus import stopwords


thepath=glob.glob('C:/Data/Shutdown/Tweets/*.csv')


for i in thepath:
    base=os.path.basename(i)
    file_name=os.path.splitext(base)[0]
    with open(i,'r') as day_input:
        with open('C:/Data/Shutdown/Tweets/Cleaned/%s_clean.csv' %file_name, 'w') as day_output:
            writer = csv.writer(day_output, lineterminator='\n')         
            for row in csv.reader(day_input):
                tweet=[wnl.lemmatize(w.lower()) for w in nltk.wordpunct_tokenize(row[4]) if len(w) >= 2]
                filtered_tweet = [w for w in tweet if not w in stopwords.words('english') and not w in ['://', 'co', 'that\xe2', 'http', 'rt', '\x80\xa6', '\x80\x98','i\xe2','.#', '-@','\x80\x93','\x80\x9c','htt\xe2', '\x80\x99', '...', '--', '.@']]
                text=nltk.Text(filtered_tweet)
                if row[0] == "tweet_id":
                    writer.writerow(row+["tweet_clean"])
                else:
                    writer.writerow(row+[filtered_tweet])

