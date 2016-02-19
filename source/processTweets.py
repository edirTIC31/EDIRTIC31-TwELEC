import json
import sqlite3 as lite
import sys
from datetime import *
import pytz
import math

import twelec_globals

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

    # If an optional keywords are present
    # increase score by 5
    for o_kw in json.loads(session[4]):
        if o_kw in tweet['text']:
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
    max_hours=session[5]
    if max_hours==-1:
        max_hours=360

    # Compute the score malus according to age, using an exp function
    # with a parametrized steepness (the lower the steepness, the later the curve knee)
    malus_delta=(math.exp((delta_hours/max_hours)*malus_age_steepness)/math.exp(malus_age_steepness))*malus_max_age
    
    score=score-int(malus_delta)
    
    return(score)  

############################################################################## 

def processTweets(session_id) :
    with lite.connect("twitter.db") as con:

        cur_in=con.cursor()
        cur_out=con.cursor()
        cur_update=con.cursor()
        
        # Retrieve the session id
        cur_in.execute("SELECT rowid,* FROM Sessions WHERE rowid=?",(session_id,))

        row=cur_in.fetchone()
        if row == None:
            print("No Such session as ",repr(session_id))
            sys.exit(1)

        session=row

        # Retrieve all tweets related to that session and that are unprocessed
        cur_in.execute("SELECT TwId,Json FROM FetchedTweets WHERE Session=? and State=?",(session[0],twelec_globals.tweet_states['unprocessed']))

        row=cur_in.fetchone()
        while row != None:
            score=scoreTweet(json.loads(row[1]),session)
            cur_out.execute("INSERT INTO KeptTweets VALUES (?,?,?,?)",(session[0],row[0],row[1],score))
            cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['processed'],row[0]))
            row=cur_in.fetchone()
                
