import json
import sqlite3 as lite
from collections import Counter
from io import BytesIO
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
from flask import render_template

import feedback



def drawHistoKeywords(session_id):

    # Get kept tweets associated to sessions
    tweet_ids=[]
    
    # Browse all kept tweets and check wether
    # some are marked as to ban or faved
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))

        row=cur.fetchone()
        while row != None:
            # Add the tweet to the hint list 
            tweet_ids.append(row[0])
            row=cur.fetchone()

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
               all_words=all_words+feedback.splitTweetInWords(tweet_text)

    # Compute frequency of the 15 most common words
    word_hist=Counter(all_words).most_common(15)          

    # Get X & Y data from the Counter object
    words=[]
    frequencies=[]
    for tuple in word_hist:
        words.append(tuple[0])
        frequencies.append(tuple[1])

    y_pos = np.arange(len(words))
    plt.barh(y_pos, frequencies, align='center', alpha=1)
    plt.yticks(y_pos, words,size="x-small",wrap=True)
    plt.xlabel("Nombre d'occurrences")
    plt.title("Fréquence des mots clés")
    
    # Draw the histogram
    img=BytesIO()
    plt.savefig(img, format='png')
            
    # Set see pointer to beginning of the file
    img.seek(0)
    return(img)

def displayTweetsStats(session_id):

    return(render_template("view_tweets_stats.html",session_id=session_id))
