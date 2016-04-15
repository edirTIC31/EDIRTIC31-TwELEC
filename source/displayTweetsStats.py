import json
import sqlite3 as lite
from datetime import *
import pytz
from collections import Counter
from io import BytesIO

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.rcdefaults()

import numpy as np

from flask import render_template, make_response

import filelock

import os

import feedback
import sessions
from mpflock import *



def drawHistoTweetAge(session_id):

    global mplib_lock
    
    # Get kept tweets associated to sessions
    tweet_ids=[]
    session=sessions.getSessionByID(session_id)
    
    # Browse all kept tweets and check wether
    # some are marked as to ban or faved
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        if session['DisplayZero']==1:
            cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))
        else:
            cur.execute("SELECT TwId FROM KeptTweets WHERE Session=? and Score!=0",(session_id,))

        row=cur.fetchone()
        while row != None:
            # Add the tweet to the hint list 
            tweet_ids.append(row[0])
            row=cur.fetchone()

    all_ages=[]
    # For each tweet texts
    # Split words and remove stop words
    for tweet_id in tweet_ids:
        with lite.connect("twitter.db") as con:
            cur=con.cursor()
            cur.execute("SELECT Json FROM FetchedTweets WHERE TwID=? AND Session=?",(tweet_id,session_id))

            row=cur.fetchone()
            if row != None :
                tweet_age=(json.loads(row[0]))['created_at']
                # Compute age in hours
                try:
                    birth_date=datetime.strptime(tweet_age,"%a %b %d %H:%M:%S %z %Y")
                except ValueError:
                    birth_date=datetime.today()
        
                # Make the today date take into account localization
                # (see the discussion about aware and naive date in the datetime module)
                now=datetime.today()
                now = pytz.utc.localize(now)
    
                delta=now-birth_date
                # Compute the age in fractional hours
                delta_hours=int(delta.days*24+(delta.seconds/3600))
                all_ages.append(delta_hours)
                row=cur.fetchone()

    # Compute historgram
    (ages,bins)=np.histogram(all_ages)

    bins_legend=[]
    # Build legend text for bins interval
    prior_bin=bins[0]
    for bin in bins[1:]:
        bins_legend.append(str(prior_bin)+" - "+str(bin))
        prior_bin=bin

    done=False
    while not done:
        try:
            # A file-based lock is used to prevent
            # multi-threaded access to matplot lib
            # (which is not mthread-safe)
            with mplib_lock.acquire(timeout = 10):
        
                y_pos = np.arange(len(bins_legend))
                plt.barh(y_pos, ages, alpha=1,align="center")
                plt.yticks(y_pos, bins_legend, size="x-small")
                plt.xlabel("Nombre de tweets de cet âge")
                plt.title("Age (en heures) des tweets")
    
                # Draw the histogram
                #img=BytesIO()
                plt.savefig('static/hta_'+str(session_id)+'.png', format='png')
                plt.close()
            
                # Set see pointer to beginning of the file
                #img.flush()
                #img.seek(0)
                done=True
                
        except filelock.Timeout:
            pass
        
    return
    

def drawHistoKeywords(session_id):

    global mplib_lock
    
    # Get kept tweets associated to sessions
    tweet_ids=[]
    session=sessions.getSessionByID(session_id)
    
    # Browse all kept tweets and check wether
    # some are marked as to ban or faved
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        if session['DisplayZero']==1:
            cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))
        else:
            cur.execute("SELECT TwId FROM KeptTweets WHERE Session=? and Score!=0",(session_id,))


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

    done=False
    while not done:
        try:
            # A file-based lock is used to prevent
            # multi-threaded access to matplot lib
            # (which is not mthread-safe)           
            with mplib_lock.acquire(timeout = 10):
 
                plt.barh(y_pos, frequencies, alpha=1, align="center")
                plt.yticks(y_pos, words, size="x-small")
                plt.xlabel("Nombre de tweets avec ce mot clé")
                plt.title("Fréquence des mots clés")
    
                # Draw the histogram
                #img=BytesIO()
                plt.savefig('static/htk_'+str(session_id)+'.png', format='png')
                plt.close()
            
                # Set see pointer to beginning of the file
                #img.flush()
                #img.seek(0)

                done=True
        except filelock.Timeout:
            pass
              
    return

    

def displayTweetsStats(session_id):

    drawHistoTweetAge(session_id)
    drawHistoKeywords(session_id)
    return(render_template("view_tweets_stats.html",session_id=session_id,unique_token=str(datetime.now())))

