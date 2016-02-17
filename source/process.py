#!/usr/bin/python3

import json
import sqlite3 as lite
import sys

############################################################################## 

# Session name
session_name="test session"

# Initial score
initial_score=100

# Bonus score when an optional keyword is present
bonus_optional_keyword=5

# Malus score when no photo is present
malus_no_photo=10

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
    None
  
  if num_photos==0:
    score=score-malus_no_photo

  # If it is a retweet, force score to zero
  if('retweeted_status' in tweet.keys()):
    return(0)

  # Improve score by number of retweets
  score=score+int(tweet['retweet_count'])
 
  return(score)  

############################################################################## 

with lite.connect("twitter.db") as con:

    cur_in=con.cursor()
    cur_out=con.cursor()

    # Retrieve the session id
    cur_in.execute("SELECT rowid,* FROM Sessions WHERE Name=?",(session_name,))

    row=cur_in.fetchone()
    if row == None:
        print("No Such session as",session_name)
        sys.exit(1)

    session=row

    # Retrieve all tweets related to that session
    cur_in.execute("SELECT Json FROM FetchedTweets WHERE Session=?",(session[0],))

    row=cur_in.fetchone()
    while row != None:
      score=scoreTweet(json.loads(row[0]),session)
      cur_out.execute("INSERT INTO KeptTweets VALUES (?,?,?)",(session[0],row[0],score))
      row=cur_in.fetchone()
    
