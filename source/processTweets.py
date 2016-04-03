import json
import sqlite3 as lite
import sys
from datetime import *
import pytz
import math

import twelec_globals
import sessions
import tweets

############################################################################## 

# Session name
session_name="test session"

# Initial score
initial_score=100

# Bonus score when an optional keyword is present
bonus_optional_keyword=5

# Malus score when no photo is present
malus_no_photo=10

# Max malus for age
malus_max_age=30

# Age malus "steepness" [5,10]
malus_age_steepness=5

##############################################################################

def scoreTweet(tweet,session):

    global initial_score
    global bonus_optional_keyword
    global malus_no_photo
  
    score=initial_score
    num_photos=0

    # If banned keywords are present
    # force score to zero
    if json.loads(session['BKeyw']) != ['']:
        for b_kw in json.loads(session['BKeyw']):
            if b_kw.lower() in tweet['text'].lower():
                return(0)

    # If optional keywords are present
    # increase score by 5 for each keyword
    if json.loads(session['OKeyw']) != ['']: 
        for o_kw in json.loads(session['OKeyw']):
            if o_kw.lower() in tweet['text'].lower():
                score=score+bonus_optional_keyword


    # If no media/photo, subtract 10
    try :
        tweet_medias=tweet['entities']['media']
        for tweet_media in tweet_medias:
            if tweet_media['type']=="photo":
                num_photos=num_photos+1
    except KeyError as e:
        pass
            
    if num_photos==0:
        score=score-malus_no_photo

    # If it is a retweet, force score to zero
    if('retweeted_status' in tweet.keys()):
        return(0)

    # Improve score by number of retweets
    score=score+int(tweet['retweet_count'])
                

    # Compute age of the tweet
    try:
        birth_date=datetime.strptime(tweet['created_at'],"%a %b %d %H:%M:%S %z %Y")
    except ValueError:
        birth_date=datetime.today()
        
    # Make the today date take into account localization
    # (see the discussion about aware and naive date in the datetime module)
    now=datetime.today()
    now = pytz.utc.localize(now)
    
    delta=now-birth_date
    # Compute the age in fractional hours
    delta_hours=delta.days*24+(delta.seconds/3600)

    # Get the session "past depth"
    max_hours=session['Since']
    if max_hours==-1:
        max_hours=360

    # Compute the score malus according to age, using an exp function
    # with a parametrized steepness (the lower the steepness, the later the curve knee)
    malus_delta=(math.exp((delta_hours/max_hours)*malus_age_steepness)/math.exp(malus_age_steepness))*malus_max_age
    
    score=score-int(malus_delta)
    
    return(score)  

############################################################################## 



def rescoreKeptTweets(session_id) :

    with lite.connect("twitter.db") as con:

        cur_kt_r=con.cursor()
        cur_kt_u=con.cursor()
        cur_kt_r.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))

        session=sessions.getSessionByID(session_id)

        row=cur_kt_r.fetchone()
        while row != None:
            tweet=tweets.getTweetByID(row[0],session_id)
            score=scoreTweet(json.loads(tweet[2]),session)
            if score !=0 :
                cur_kt_u.execute("UPDATE KeptTweets SET Score= ? WHERE Session=? AND TwID=?",(score,session_id,row[0]))
            else :
                cur_kt_u.execute("DELETE FROM KeptTweets WHERE Session=? AND TwID=?",(session_id,row[0]))
            row=cur_kt_r.fetchone()

## ** TODO ** handle error case
def processTweets(session_id) :
    with lite.connect("twitter.db") as con:

        cur_in=con.cursor()
        cur_update=con.cursor()

        # Retrieve session data
        session=sessions.getSessionByID(session_id)
        
        # Retrieve all tweets related to that session and that are unprocessed
        cur_in.execute("SELECT TwId,Json FROM FetchedTweets WHERE Session=? and State=?",(session_id,twelec_globals.tweet_states['unprocessed']))

        row=cur_in.fetchone()
        while row != None:
            # Compute the tweet score
            score=scoreTweet(json.loads(row[1]),session)
        
            if score!=0 or twelec_globals.keep_zero_score==True:
                # Insert them in the kept table
                cur_update.execute("INSERT INTO KeptTweets VALUES (?,?,?)",(session_id,row[0],score))
                
            # And switch the state to 'processed new' in the Fetched tweet table
            cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['processed_new'],row[0]))
            row=cur_in.fetchone()
                
