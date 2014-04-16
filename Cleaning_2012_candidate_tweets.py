# -*- coding: utf-8 -*-
"""
@author: Iulia Cioroianu (contractions and shorthand dictionaries from Duncan)  
Last modified: April 15, 2014
Purpose: Clean candidate tweets 

Input data1: Candidate raw tweets, one .csv per candidate, one tweet per line 
Output data: 1. Candidate tweets cleaned, one .txt per candidate

Input data1: Candidate raw tweets per week, one .csv per week, one tweet per line
Output data: 2. Candidate tweets per week cleaned, one .txt per week

"""

import nltk, re, csv
import glob, os, sys

####################################################################
# Clean short tweets
####################################################################

#Included special characters here: 
shorthand_trans = {
    "&amp": "and",
    "w/ ": "with",
    "w/o ": "without",
    "thx": "thank",
    "btw": "by the way",
    "’": "'",
    "`": "'",
    "$": "dollar",
    "\xe2\x80\x90": "-",
    "\xe2\x80\x91": "-",
    "\xe2\x80\x92": "-",
    "\xe2\x80\x93": "-",
    "\xe2\x80\x94": "-",
    "\xe2\x80\x95": "-",
    "\xe2\x80\xa6": " ",
    "\xe2\x80\x98": "'",
    "\xe2\x80\x99": "'",
    "\xe2\x80\x9a": "'",
    "\xe2\x80\x9b": "'",
    "\xe2\x80\x9c": " ",
    "\xe2\x80\x9d": " ",
    "\xe2\x80\x9e": " ",
    "\xe2\x80\x9f": " ",
    "\xe2\x81\x84": "/",
    "\x80\x9d": " "
    }


extra_punctuation_trans = {
    ".": " ",
    ",": " ",
    ";": " ",
    ":": " ",
    "#": " ",
    "@": " ",
    "�": " ",
    "?": " ",
    "!": " ",
    "(": " ",
    ")": " ",
    "-": " ",
    "&": " ",
    "*": " ",
    "$": " ",
    "#": " ",
    "/": " ",
    "<": " ",
    ">": " ",
    "+": " ",
    "_": " ",
    "%": " percent ",
    " u ": " us ",
    " ha ": " has ",
    " wa ": " was ",
    " tcot ": " republican ",
    " dem ": " democrat ",
    " rep ": " representative ",
    " 1st ": " first ",  
    "``": " ", 
    "''": " ",   
    "|": " ",
    '€"': " ",
    '"': " ",    
    "`": " ",
    "’": " ",
    "`": " ",
    "’’": " ",
    "'": " ",    
    }


contraction_trans = {
    "’":"'",
    "ain't": "am not", # are not; is not; has not; have not
    "aren't": "are not", # am not
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "gonna": "going to",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    #"he'd": "he had / he would",
    "he'd've": "he would have",
    "he'll": "he will", # he shall
    "he'll've": "he will have", # he shall have
    #"he's": "he has / he is",
    "here's": "here is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    #"how's": "how has / how is / how does",
    #"i'd": "i had / i would",
    "i'd've": "i would have",
    "i'll": "i will", # i shall
    "i'll've": "i will have", # i shall have
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would", # it had
    "it'd've": "it would have",
    "it'll": "it will", # it shall
    "it'll've": "it will have", # it shall have
    #"it's": "it has / it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    #"she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she will", # she shall
    "she'll've": "she will have", # she shall have
    #"she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    #"so's": "so as / so is",
    #"that'd": "that would / that had",
    "that'd've": "that would have",
    #"that's": "that has / that is",
    #"there'd": "there had / there would",
    "there'd've": "there would have",
    #"there's": "there has / there is",
    #"they'd": "they had / they would",
    "they'd've": "they would have",
    "they'll": "they will", # they shall
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    #"we'd": "we had / we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    #"what'll": "what shall / what will",
    #"what'll've": "what shall have / what will have",
    "what're": "what are",
    #"what's": "what has / what is",
    "what've": "what have",
    #"when's": "when has / when is",
    "when've": "when have",
    "where'd": "where did",
    #"where's": "where has / where is",
    "where've": "where have",
    #"who'll": "who shall / who will",
    #"who'll've": "who shall have / who will have",
    #"who's": "who has / who is",
    "who've": "who have",
    #"why's": "why has / why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    #"you'd": "you had / you would",
    "you'd've": "you would have",
    "you'll": "you will", # you shall
    "you'll've": "you will have", # you shall have
    "you're": "you are",
    "you've": "you have",
    "’": "'"
}

pol_terms = [
    (re.compile(r"^AK\s|\sAK\s|\sAK$"),  "Alaska "),
    (re.compile(r"^AL\s|\sAL\s|\sAL$"), " Alabama "),
    (re.compile(r"^AR\s|\sAR\s|\sAR$"), " Arkansas "),
    (re.compile(r"^AS\s|\sAS\s|\sAS$"), " American Samoa "),
    (re.compile(r"^AZ\s|\sAZ\s|\sAZ$"), " Arizona "),
    (re.compile(r"^CA\s|\sCA\s|\sCA$"), " California "),
    (re.compile(r"^CO\s|\sCO\s|\sCO$"), " Colorado "),
    (re.compile(r"^CT\s|\sCT\s|\sCT$"), " Connecticut "),
    (re.compile(r"^DC\s|\sDC\s|\sDC$"), " District of Columbia "),
    (re.compile(r"^DE\s|\sDE\s|\sDE$"), " Delaware "),
    (re.compile(r"^FL\s|\sFL\s|\sFL$"), " Florida "),
    (re.compile(r"^GA\s|\sGA\s|\sGA$"), " Georgia "),
    (re.compile(r"^GU\s|\sGU\s|\sGU$"), " Guam "),
    (re.compile(r"^HI\s|\sHI\s|\sHI$"), " Hawaii "),
    (re.compile(r"^IA\s|\sIA\s|\sIA$"), " Iowa "),
    (re.compile(r"^ID\s|\sID\s|\sID$"), " Idaho "),
    (re.compile(r"^IL\s|\sIL\s|\sIL$"), " Illinois "),
    (re.compile(r"^IN\s|\sIN\s|\sIN$"), " Indiana "),
    (re.compile(r"^KS\s|\sKS\s|\sKS$"), " Kansas "),
    (re.compile(r"^KY\s|\sKY\s|\sKY$"), " Kentucky "),
    (re.compile(r"^LA\s|\sLA\s|\sLA$"), " Louisiana "),
    (re.compile(r"^MA\s|\sMA\s|\sMA$"), " Massachusetts "),
    (re.compile(r"^MD\s|\sMD\s|\sMD$"), " Maryland "),
    (re.compile(r"^ME\s|\sME\s|\sME$"), " Maine "),
    (re.compile(r"^MI\s|\sMI\s|\sMI$"), " Michigan "),
    (re.compile(r"^MN\s|\sMN\s|\sMN$"), " Minnesota "),
    (re.compile(r"^MO\s|\sMO\s|\sMO$"), " Missouri "),
    (re.compile(r"^MP\s|\sMP\s|\sMP$"), " Northern Mariana Islands "),
    (re.compile(r"^MS\s|\sMS\s|\sMS$"), " Mississippi "),
    (re.compile(r"^MT\s|\sMT\s|\sMT$"), " Montana "),
    (re.compile(r"^NA\s|\sNA\s|\sNA$"), " National "),
    (re.compile(r"^NC\s|\sNC\s|\sNC$"), " North Carolina "),
    (re.compile(r"^ND\s|\sND\s|\sND$"), " North Dakota "),
    (re.compile(r"^NE\s|\sNE\s|\sNE$"), " Nebraska "),
    (re.compile(r"^NH\s|\sNH\s|\sNH$"), " New Hampshire "),
    (re.compile(r"^NJ\s|\sNJ\s|\sNJ$"), " New Jersey "),
    (re.compile(r"^NM\s|\sNM\s|\sNM$"), " New Mexico "),
    (re.compile(r"^NV\s|\sNV\s|\sNV$"), " Nevada "),
    (re.compile(r"^NY\s|\sNY\s|\sNY$"), " New York "),
    (re.compile(r"^OH\s|\sOH\s|\sOH$"), " Ohio "),
    (re.compile(r"^OK\s|\sOK\s|\sOK$"), " Oklahoma "),
    (re.compile(r"^OR\s|\sOR\s|\sOR$"), " Oregon "),
    (re.compile(r"^PA\s|\sPA\s|\sPA$"), " Pennsylvania "),
    (re.compile(r"^PR\s|\sPR\s|\sPR$"), " Puerto Rico "),
    (re.compile(r"^RI\s|\sRI\s|\sRI$"), " Rhode Island "),
    (re.compile(r"^SC\s|\sSC\s|\sSC$"), " South Carolina "),
    (re.compile(r"^SD\s|\sSD\s|\sSD$"), " South Dakota "),
    (re.compile(r"^TN\s|\sTN\s|\sTN$"), " Tennessee "),
    (re.compile(r"^TX\s|\sTX\s|\sTX$"), " Texas "),
    (re.compile(r"^UT\s|\sUT\s|\sUT$"), " Utah "),
    (re.compile(r"^VA\s|\sVA\s|\sVA$"), " Virginia "),
    (re.compile(r"^VI\s|\sVI\s|\sVI$"), " Virgin Islands "),
    (re.compile(r"^VT\s|\sVT\s|\sVT$"), " Vermont "),
    (re.compile(r"^WA\s|\sWA\s|\sWA$"), " Washington "),
    (re.compile(r"^WI\s|\sWI\s|\sWI$"), " Wisconsin "),
    (re.compile(r"^WV\s|\sWV\s|\sWV$"), " West Virginia "),
    (re.compile(r"^WY\s|\sWY\s|\sWY$"), " Wyoming "),
    (re.compile(r"^US\s|\sUS\s|\sUS$"), " United States "),
    (re.compile(r"^USA\s|\sUSA\s|\sUSA$"), " United States of America "),
    (re.compile(r"^EU\s|\sEU\s|\sEU$"), " European Union "),
    (re.compile(r"^UK\s|\sUK,\s|\sUK$"), " United Kingdom "),
    (re.compile(r"^US,\s|\sUS,\s|\sUS,$"), " United States "),
    (re.compile(r"^USA,\s|\sUSA,\s|\sUSA,$"), " United States of America "),
    (re.compile(r"^EU,\s|\sEU,\s|\sEU,$"), " European Union "),
    (re.compile(r"^UK,\s|\sUK,\s|\sUK,$"), " United Kingdom "),
    (re.compile(r"^REP\s|\sREP\s|\sREP$"), " representative "),
    (re.compile(r"^SEN\s|\sSEN\s|\sSEN$"), " senator "),
    (re.compile(r"^DEM\s|\sDEM\s|\sDEM$"), " democrat "),
    (re.compile(r"^GOP\s|\sGOP\s|\sGOP$"), " republican "),
    (re.compile(r"^Rep\s|\sRep\s|\sRep $"), " representative "),
    (re.compile(r"^Sen\s|\sSen\s|\sSen $"), " senator "),
    (re.compile(r"^Dem\s|\sDem\s|\sDem$"), " democrat "),
    (re.compile(r"^Gop\s|\sGop\s|\sGop$"), " republican "),
    (re.compile(r"^REP.\s|\sREP.\s|\sREP.$"), " representative "),
    (re.compile(r"^SEN.\s|\sSEN.\s|\sSEN.$"), " senator "),
    (re.compile(r"^DEM.\s|\sDEM.\s|\sDEM.$"), " democrat "),
    (re.compile(r"^GOP.\s|\sGOP.\s|\sGOP.$"), " republican "),
    (re.compile(r"^rep\s|\srep\s|\srep$"), " representative "),
    (re.compile(r"^sen\s|\ssen\s|\ssen$"), " senator "),
    (re.compile(r"^dem\s|\sdem\s|\sdem$"), " democrat "),
    (re.compile(r"^gop\s|\sgop\s|\sgop$"), " republican "),
    (re.compile(r"^Rep.\s|\sRep.\s|\sRep.$"), " representative "),
    (re.compile(r"^Sen.\s|\sSen.\s|\sSen.$"), " senator "),
    (re.compile(r"^Dem.\s|\sDem.\s|\sDem.$"), " democrat "),
    (re.compile(r"^Gop.\s|\sGop.\s|\sGop.$"), " republican "),
    (re.compile(r"^rep.\s|\srep.\s|\srep.$"), " representative "),
    (re.compile(r"^sen.\s|\ssen.\s|\ssen.$"), " senator "),
    (re.compile(r"^dem.\s|\sdem.\s|\sdem.$"), " democrat "),
    (re.compile(r"^gop.\s|\sgop.\s|\sgop.$"), " republican "),
    ]


def translate_contractions(text):
    """Translates contractions with expanded forms. Returns translated string"""
    for c in contraction_trans:
        text = text.replace(c, contraction_trans[c])
    return text

def translate_shorthand(text):
    """Translate common shorthand terms into long form. Returns translated string"""
    for s in shorthand_trans:
        text = text.replace(s, shorthand_trans[s])
    return text


def translate_pol_terms(text):
    for a in pol_terms:
        text = a[0].sub(a[1], text)
    return text

    
def remove_extra_punctuation(text):
    """Translates some punctuation (not apostrophes) from text. Returns cleaned string"""
    for p in extra_punctuation_trans:
        text = text.replace(p, extra_punctuation_trans[p])
    return text


test_tweet="Adam’s wife Melody speaks with a voter in Dumfries. | dem us US rep  Believe us when we tell you she is *very* persuasive. #adamcook2012 http://t.co/0Hp28gki US USA, EU us EURO .USA Rep. REP. US EU Europe Europe Deomcratic democratic GOP. Senator. Representative '"
translate_pol_terms(test_tweet)
translate_pol_terms(translate_contractions(translate_shorthand((test_tweet)))) 


########################################################
#Generate one clean .txt file with all the tweets in the time frame for each candidate
#######################################################

wnl = nltk.WordNetLemmatizer()
from nltk.corpus import stopwords

thepath=glob.glob('C:/Data/Candidate_tweets/Processing_tweets/Shortened_candidates/*.csv')

for i in thepath:
    base=os.path.basename(i)
    filename=os.path.splitext(base)[0]
    with open(i,'rU') as cand_input:
        with open('C:/Data/Candidate_tweets/Processing_tweets/Text_files_candidates_2/%s.txt' %filename,'ab+') as tweets_by_cand:
            for row in csv.reader(cand_input):
                try:
                    t=translate_pol_terms(row[2]).lower()
                    text=(translate_contractions(translate_shorthand(t)))
                    tweet=[wnl.lemmatize(w.lower()) for w in nltk.wordpunct_tokenize(text) if len(w) >= 2]
                    filtered_tweet = [w for w in tweet if not w in stopwords.words('english') and not w in ['://', 'co', 'http://', 'rt', '.#', '-@','htt', '...', '--', '.@', 'http', 'com', 're', 'via', '``', "''", '|', '\x80\x9d', '€"', '"', "'", '\"', '\``']]
                    clean_tweet=remove_extra_punctuation(" ".join(filtered_tweet))                
                    if row[1]!="created_at": tweets_by_cand.write(clean_tweet)
                except: 
                    e = sys.exc_info()[0]
                    tweets_by_cand.write(" ")


########################################################
#Generate one clean .txt file per week
#######################################################

wnl = nltk.WordNetLemmatizer()
from nltk.corpus import stopwords

thepath=glob.glob('C:/Data/Candidate_tweets/Processing_tweets/By_week_tweets/*.csv')

for i in thepath:
    base=os.path.basename(i)
    filename=os.path.splitext(base)[0]
    with open(i,'rU') as cand_input:
        with open('C:/Data/Candidate_tweets/Processing_tweets/By_week_tweets/Cleaned_by_week/%s.txt' %filename,'ab+') as tweets_by_cand:
            for row in csv.reader(cand_input):
                try:
                    t=translate_pol_terms(row[2]).lower()
                    text=(translate_contractions(translate_shorthand(t)))
                    tweet=[wnl.lemmatize(w.lower()) for w in nltk.wordpunct_tokenize(text) if len(w) >= 2]
                    filtered_tweet = [w for w in tweet if not w in stopwords.words('english') and not w in ['://', 'co', 'http://', 'rt', '.#', '-@','htt', '...', '--', '.@', 'http', 'com', 're', 'via', '``', "''", '|', '\x80\x9d', '€"', '"',  "'", '\"']]
                    clean_tweet=remove_extra_punctuation(" ".join(filtered_tweet))                
                    if row[1]!="created_at": tweets_by_cand.write(clean_tweet)
                except: 
                    e = sys.exc_info()[0]
                    tweets_by_cand.write(" ")





