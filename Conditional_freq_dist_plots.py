# -*- coding: utf-8 -*-
"""
@author: Iulia Cioroianu
Last modified: April 15, 2014
Purpose: Plot conditional frequency distributions for key words
Input data: Candidate cleaned tweets, one .txt per week 
Output data: Graph. 
"""

import nltk
wnl = nltk.WordNetLemmatizer()

from nltk.corpus import PlaintextCorpusReader
from nltk import ConditionalFreqDist

corpus = PlaintextCorpusReader('C:/Data/Candidate_tweets/Processing_tweets/By_week_tweets/Cleaned_by_week/', '.*')
corpus.fileids()[0:3]
print len(corpus.words())

cfd = ConditionalFreqDist(
    (target, fileid)
    for fileid in corpus.fileids()
    for w in corpus.words(fileid)
    for target in ['obama', 'romney', 'opponent']
    if w==target)
        
cfd.plot()


cfd = nltk.ConditionalFreqDist(
    (target, fileid)
    for fileid in corpus.fileids()
    for w in corpus.words(fileid)
    for target in ['democrat', 'republican', 'independent']
    if w==target)
        
cfd.plot()


