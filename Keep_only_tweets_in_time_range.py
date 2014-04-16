# -*- coding: utf-8 -*-
"""
@author: Iulia Cioroianu
Last modified: April 15, 2014
Purpose: Only keep tweets between 05/06/2012 and 11/07/2012 
Input data: Candidate tweets, one .csv per candidate, one tweet per line 
Output data: Candidate tweets in time range, one .csv per candidate, one tweet per line
"""

import re
import csv
import glob, os

#############################################################                    
#Keep only relevant tweets
#############################################################

from datetime import datetime

# Only keep tweets between 2012-06-06 and 2012-11-07
start_date=datetime(2012,05,06)
end_date=datetime(2012,11,07)

thepath=glob.glob('C:/Data/Candidate_tweets/Processing_tweets/*.csv')
for i in thepath:
    base=os.path.basename(i)
    filename=os.path.splitext(base)[0]
    file_name=re.sub('_tweets','', filename)
    with open(i,'r') as cand_input:
        with open('C:/Data/Candidate_tweets/Processing_tweets/Shortened_candidates/%s.csv' %file_name, 'w') as cand_output:
            writer = csv.writer(cand_output, lineterminator='\n')         
            for row in csv.reader(cand_input):
                if row[1]!="created_at": 
                    date=datetime.strptime(row[1],'%Y-%m-%d %H:%M:%S')
                    if date>start_date and date<end_date: writer.writerow(row)


################################################################