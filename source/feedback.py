from flask import request
import sqlite3 as lite
import json
import re
from collections import Counter

import displayTweets
import processTweets
import fetchTweets
import twelec_globals
import sessions

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
    tweet_words=re.split(' |\:|\'|\+|\-|\*|\/|\\|\;|\.|\,|\=|\"|\«|\»|\|\>|\<|\…|\xa0',tweet_text)
    filtered_words=[]
    
    for tweet_word in tweet_words:
        
        keep=True

        if tweet_word=='' or tweet_word==' ':
            keep=False
                       
        # Remove all stop words
        if keep and tweet_word in twelec_globals.stop_words :
            keep=False    

        if keep and tweet_word[0] in ('\"','\'','\«','\»','(',')','[',']','{','}'):
            tweet_word=tweet_word[1:]
            if tweet_word=="":
                keep=False

        if keep and tweet_word[-1] in ('\"','\'','\«','\»','(',')','[',']','{','}'):
            tweet_word=tweet_word[:-1]
            if tweet_word=="":
                keep=False

           
        if keep and len(tweet_word) < 3:
            keep=False
            
        if keep:
            filtered_words.append(tweet_word)

    return filtered_words


# ** TODO ** HANDLE ERROR
def computeNewKeywords(session_id,tweet_words,frequency_threshold):


    # Compute the 10 most common words
    word_hist=Counter(tweet_words).most_common(10)
    new_keywords=[]
    
    # Get the list of current session keywords
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur.execute("SELECT MKeyw FROM SESSIONS WHERE rowid=?",(session_id,))
        row=cur.fetchone()
        old_keywords=json.loads(row[0])

    # For new keywords found more than two time and not yet in the
    # the existing keyword list, add                     
    for (keyword,freq) in word_hist:
        if freq<frequency_threshold:
            break
        if keyword not in old_keywords:
            new_keywords.append(keyword)
        
    return new_keywords

# ** TODO ** HANDLE ERROR
def suggestTweetKeywords(session_id,tweet_ids,frequency_threshold):

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
        
    new_keywords=computeNewKeywords(session_id,all_words,frequency_threshold)
    
    return new_keywords

# ** TODO ** HANDLE ERROR
def feedback(request):

    session_id=int(request.form['session_id'])
    session=sessions.getSessionByID(session_id)

    try:
        if request.form['dz']=="on" :
            display_zero=1
        else:
            display_zero=0
    except KeyError:
        display_zero=0
        

    faved_tweet_ids=[]
    hint_tweet_ids=[]
    
    # Browse all kept tweets and check wether
    # some are marked as to ban or faved
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur_update=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        if display_zero==1 :
            cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))
        else :
            cur.execute("SELECT TwId FROM KeptTweets WHERE Session=? AND Score!=0",(session_id,))

        row=cur.fetchone()
        while row != None:
            # Add the tweet is to the hint list (in case a hint is request - see below)
            hint_tweet_ids.append(row[0])
            
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
        faved_keywords=suggestTweetKeywords(session_id,faved_tweet_ids,twelec_globals.faved_frequency_threshold)
    else:
        faved_keywords=[]

    # If a hint is requested, compute the hint list
    try:
        hint_checkbox=request.form['cdp']
        hint_keywords=suggestTweetKeywords(session_id,hint_tweet_ids,twelec_globals.hint_frequency_threshold)
    except KeyError:
        hint_checkbox=""
        hint_keywords=[]
 
    # Get the old mandatory, optional & banned keywords
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur.execute("SELECT MKeyw,OKeyw,BKeyw FROM SESSIONS WHERE rowid=?",(session_id,))
        row=cur.fetchone()
        old_mkeywords=json.loads(row[0])
        old_okeywords=json.loads(row[1])
        old_bkeywords=json.loads(row[2])

        # Replace mandatory keywords with the ones from the form
        try:
            new_mkeywords=request.form['mkw'].split(" ")
        except KeyError:
            new_mkeywords=old_mkeywords

        # Add the new suggested keyword from the fav's - if any
        new_mkeywords=new_mkeywords+faved_keywords

            
        # Add to the optional keywords the hinted ones - if any
        try:
            new_okeywords=request.form['okw'].split(" ")
        except KeyError:
            new_okeywords=old_okeywords
        new_okeywords=new_okeywords+hint_keywords


        # Replace the banned keywords - if any
        try:
            new_bkeywords=request.form['bkw'].split(" ")
        except KeyError:
            new_bkeywords=bld_okeywords

            
        # Update session data
        cur.execute("UPDATE Sessions SET MKeyw=?,OKeyw=?,BKeyw=?,DisplayZero=? WHERE rowid=?",(json.dumps(new_mkeywords),json.dumps(new_okeywords),json.dumps(new_bkeywords),display_zero,session_id))



    # Re run tweet search    
    fetchTweets.fetchTweets(twelec_globals.a_token,
                            twelec_globals.a_secret,
                            twelec_globals.c_key,
                            twelec_globals.c_secret,
                            session_id)

    #with lite.connect("twitter.db") as con:
        # Re tag all processed tweets as un processed (except the banned tweets)
        # This gives the opportunity to ban tweets 
        #cur=con.cursor()
        #cur.execute("UPDATE FetchedTweets SET State=? WHERE Session=? AND State=?",(twelec_globals.tweet_states['unprocessed'],session_id,twelec_globals.tweet_states['processed']))    
        #cur.execute("DELETE FROM KeptTweets WHERE Session=?",(session_id,))

    # Do scoring
    processTweets.rescoreKeptTweets(session_id)
    processTweets.processTweets(session_id)

    # and display
    return(displayTweets.displayToStr(session_id))
