# -*- coding: utf-8 -*-
"""
@author: Iulia Cioroianu
Last modified: April 15, 2014
Purpose: Aggregate all candidate tweets by week  
Input data: Candidate tweets between 5/7 and 11/6, one .csv per candidate, one twet per line 
Output data: Tweets aggregated by week, one .csv per week 
"""

import glob, os, csv

from datetime import datetime, timedelta


####################################################################
#Build tweet compilations by week
####################################################################
 
start_date1=datetime(2012,5,8)
start_date2=datetime(2012,5,14)

end_date1=datetime(2012,11,6)
end_date2=datetime(2012,11,7)

d = start_date1
delta = timedelta(days=7)
week_begin=[]
week_end=[]
week=0

while d < end_date1:
    week_begin.append(d)
    d += delta

e=start_date2

while e <= end_date2:
    week_end.append(e)
    e += delta

len(week_end)

for i in range(0,26):
    start_week=week_begin[i]
    end_week=week_end[i]
    print i, start_week, end_week
    

thepath=glob.glob('C:/Data/Candidate_tweets/Processing_tweets/Shortened_candidates/*.csv')

for i in range(0,26):
    start_week=week_begin[i]
    end_week=week_end[i]
    with open('C:/Data/Candidate_tweets/Processing_tweets/By_week_tweets/%s.csv' %i, 'w') as cand_output:
        writer = csv.writer(cand_output, lineterminator='\n')
        for i in thepath:
            base=os.path.basename(i)
            filename=os.path.splitext(base)[0]
            with open(i,'rU') as cand_input:
                for row in csv.reader(cand_input):
                    try:
                        date=datetime.strptime(row[1],'%Y-%m-%d %H:%M:%S')
                        if date>=start_week and date<=end_week: 
                            writer.writerow(row+[filename])
                    except: writer.writerow("")


