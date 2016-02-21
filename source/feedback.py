from flask import request
import sqlite3 as lite
import json
import re
from collections import Counter

import displayTweets
import processTweets
import fetchTweets
import twelec_globals

def splitTweetInWords(tweet_text):

    # Tokenize text using ' ' as separator
    tweet_words=tweet_text.lower().split(" ")
    filtered_words=[]

    # First pass: get rid of URLs
    for tweet_word in tweet_words:
    
        if "http://" not in tweet_word and "https://" not in tweet_word :
            filtered_words.append(tweet_word)

    tweet_words=filtered_words

    # Re-build a tweet text without the URLs
    tweet_text=" "
    tweet_text=tweet_text.join(filtered_words)

    # Tokenize text based on multiple separators
    tweet_words=re.split(' |\:|\'|\+|\-|\*|\/|\\|\;|\.|\,|\=|\'|\>|\<',tweet_text)
    filtered_words=[]
    
    for tweet_word in tweet_words:
        
        keep=True

        if tweet_word=='':
            keep=False
                       
        # Remove all stop words
        if keep and tweet_word in twelec_globals.stop_words :
            keep=False    

        if keep and len(tweet_word) < 3:
            keep=False
            
        if keep:
            filtered_words.append(tweet_word)

    return filtered_words

def suggestNewKeywords(session_id,tweet_words):

    print(tweet_words)

    # Compute the 10 most common words
    word_hist=Counter(tweet_words).most_common(10)
    new_keywords=[]
    
    # Get the list of current session keywords
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur.execute("SELECT Mkeyw FROM SESSIONS WHERE rowid=?",(session_id,))
        row=cur.fetchone()
        old_keywords=json.loads(row[0])

    # For new keywords found more than two time and not yet in the
    # the existing keyword list, add                     
    for (keyword,freq) in word_hist:
        if freq<3:
            break
        if keyword not in old_keywords:
            new_keywords.append(keyword)
        
    print(new_keywords)
    return new_keywords

def processFavedTweets(session_id,tweet_ids):

    all_words=[]
    # For each tweet texts
    # Split words and remove stop words
    for tweet_id in tweet_ids:
       with lite.connect("twitter.db") as con:
           cur=con.cursor()
           cur.execute("SELECT Json FROM FetchedTweets WHERE TwID=? AND Session=?",(tweet_id,session_id))

           row=cur.fetchone()
           if row != None :
               tweet_text=(json.loads(row[0]))['text']
               # Append the remaining words to the list of words
               # to process later
               all_words=all_words+splitTweetInWords(tweet_text)
        
    new_keywords=suggestNewKeywords(session_id,all_words)
    
    return new_keywords
    
def feedback(request):

    session_id=int(request.form['session_id'])
    faved_tweet_ids=[]

    # Browse all kept tweets and check wether
    # some are marked as to ban or faved
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur_update=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))

        row=cur.fetchone()
        while row != None:
            # If the tweet is banned, remove it from the kept table and tag it as banned in the fetched table
            try:
                if request.form['ban_'+str(row[0])]=="on" and 'fav_'+str(row[0]) not in (request.form).keys():                
                    cur_update.execute("DELETE FROM KeptTweets WHERE TwId=?",(row[0],))
                    cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['banned'],row[0]))
            except KeyError:
                pass

            # If the tweet is faved, add it to the faved list
            try:
                if request.form['fav_'+str(row[0])]=="on" and 'ban_'+str(row[0]) not in (request.form).keys():
                    cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['faved'],row[0]))               
                    faved_tweet_ids.append(row[0])
            except KeyError:
                pass               
            
            row=cur.fetchone()
            
    # Suggest new keywords based on faved tweets
    if len(faved_tweet_ids)!=0 :
        new_keywords=processFavedTweets(session_id,faved_tweet_ids)

        if new_keywords != []:
            # Add these keywords to the session keywords
            with lite.connect("twitter.db") as con:

                cur=con.cursor()
                cur.execute("SELECT Mkeyw FROM SESSIONS WHERE rowid=?",(session_id,))
                row=cur.fetchone()
                old_keywords=json.loads(row[0])
                old_keywords=old_keywords+new_keywords
                cur.execute("UPDATE Sessions SET Mkeyw=? WHERE rowid=?",(json.dumps(old_keywords),session_id,))
                        
            fetchTweets.fetchTweets(twelec_globals.a_token,
                                    twelec_globals.a_secret,
                                    twelec_globals.c_key,
                                    twelec_globals.c_secret,
                                    session_id)
    
            processTweets.processTweets(session_id)
    
    return(displayTweets.displayToStr(session_id))
