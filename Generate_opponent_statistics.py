# -*- coding: utf-8 -*-
"""
@author: Iulia Cioroianu
Last modified: April 15, 2014
Purpose: Generate frequencies for key competition terms (oppoenent names, parties, obana, romney)
Input data: Candidate cleaned tweets, one .txt per candidate 
Output data: .csv dataset, rows: candidates, columns: percentage mentionings
"""

import glob, os, csv
import nltk

####################################################################
#Generate opponents and other political actors mentions
###################################################################

thepath=glob.glob('C:/Data/Candidate_tweets/Processing_tweets/Text_files_candidates_2/*.txt')
for i in thepath:
    base=os.path.basename(i)    
    file_name=os.path.splitext(base)[0]
    with open(i,'rU') as text_input:
        with open('C:/Data/Candidate_tweets/Test_tweets/Opponent_variables.csv','rU') as variables_input:
            with open('C:/Data/Candidate_tweets/Processing_tweets/Covariates/Opp_covariates_2.csv', 'ab+') as opponent_output:
                writer = csv.writer(opponent_output, lineterminator='\n')
                raw=text_input.read()
                tokens=nltk.word_tokenize(raw)
                text=nltk.Text(tokens)
                var_reader=csv.reader(variables_input)
                for row in var_reader:
                    if row[8]==file_name:
                        president=100*text.count('president')/len(text)
                        opponent=100*text.count('opponent')/len(text)
                        obama=100*text.count('obama')/len(text)
                        romney=100*text.count('romney')/len(text)
                        barack=100*text.count('barack')/len(text)
                        mitt=100*text.count('mitt')/len(text)
                        democrat=100*text.count('democrat')/len(text)
                        republican=100*text.count('republican')/len(text)
                        opponent_names=nltk.word_tokenize(row[10])
                        opponent_user=nltk.word_tokenize(row[12])
                        opp_add=0                        
                        for name in opponent_names:
                            opp_count=100*text.count(name.lower())/len(text)
                            opp_add=opp_add+opp_count
                        if len(opponent_names)>0: 
                            opp_mean=opp_add/len(opponent_names)
                        else:
                            opp_mean=9999
                        user_opp_add=0                        
                        for user in opponent_user:
                            user_opp_count=100*text.count(user.lower())/len(text)
                            user_opp_add=user_opp_add+user_opp_count
                        if len(opponent_names)>0: 
                            user_opp_mean=user_opp_add/len(opponent_names)
                        else:
                            user_opp_mean=9999
                        writer.writerow([file_name]+[opponent]+[obama]+[barack]+[romney]+[mitt]+[president]+[democrat]+[republican]+[opp_add]+[opp_mean]+[user_opp_add]+[user_opp_mean])

########################################################################


