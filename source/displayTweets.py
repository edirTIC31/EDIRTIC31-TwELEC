import json
import sqlite3 as lite
import sys
import cgi
import io
from flask import render_template, url_for
import os

import twelec_globals
import sessions
import tweets


# ** TODO ** handle error case
def displayToStr(session_id):

    with lite.connect("twitter.db") as con:

        cur=con.cursor()

        # Get the session data
        session=sessions.getSessionByID(session_id)
        if session == None:
            return(render_template("error.html",cause="Session inexistante"))

        # Build input field value based on mandatory keywords
        mkwords=json.loads(session['MKeyw'])

        mkw_field=mkwords[0]
        for mkw in mkwords[1:]:
            mkw_field=mkw_field+" "+mkw

        # Build input field value based on optional keywords
        okwords=json.loads(session['OKeyw'])
            
        if len(okwords) > 0 :
            okw_field=okwords[0]
            for okw in okwords[1:]:
                okw_field=okw_field+" "+okw
        else:
            okw_field=""

       # Build input field value based on optional keywords
        bkwords=json.loads(session['BKeyw'])
            
        if len(bkwords) > 0 :
            bkw_field=bkwords[0]
            for bkw in bkwords[1:]:
                bkw_field=bkw_field+" "+bkw
        else:
            bkw_field=""


        since_field=session['Since']

        minimum_score=session['MinimumScore']
            
        # Retrieve all tweets related to that session
        cur.execute("SELECT TwId, Score FROM KeptTweets WHERE Session=? ORDER BY Score DESC LIMIT ?",(session_id,session['MaxHits']))

        tweets_set=[]
        row=cur.fetchone()
        while row != None:
            # Get tweet data
            tweet_row=tweets.getTweetByID(row[0],session_id)
            # tweet_row[0] is the session id, tweet_row[1] is the tweet id
            # tweet_row{2] is the structure storing the tweet
            tweet=json.loads(tweet_row[2])
            
            tweet_elm={}
            tweet_elm['score']=row[1]

            tweet_elm['user']=tweet['user']['name']
            if tweet['place'] != None:
                tweet_elm['place']=tweet['place']['full_name']
                
            tweet_elm['created_at']=tweet['created_at']

            if tweet_row[3] == twelec_globals.tweet_states['processed_new']:
                tweet_elm['new']=True

            tweet_elm['text']=tweet['text']
                
            tweet_elm['id']=row[0]

            # Create a media entry if any
            medias=[]
            try :
                tweet_medias=tweet['entities']['media']
                for tweet_media in tweet_medias:
                    if tweet_media['type']=="photo":
                        medias.append(tweet_media['media_url_https'])
            except KeyError:
                pass
            if len(medias)>0:
                tweet_elm['medias']=medias

            if tweet_elm['score']>=minimum_score:
                tweets_set.append(tweet_elm)

            row=cur.fetchone()

        # Switch tweets from the Kept table from 'processed_new' to 'processed'
        cur.execute("UPDATE FetchedTweets SET State=? WHERE Session=? and State=?",(twelec_globals.tweet_states['processed'],session_id,\
                                                                                    twelec_globals.tweet_states['processed_new']))
        display_params={}
        display_params['session_id']=session_id
        display_params['since_field']=since_field
        display_params['mkw_field']=mkw_field
        display_params['okw_field']=okw_field
        display_params['bkw_field']=bkw_field
        display_params['minimum_score']=minimum_score
        display_params['tweets_set']=tweets_set

        cur.execute("SELECT * FROM FetchedTweets WHERE Session=?",(session_id,))
        display_params['num_fetched']=len(cur.fetchall())

        cur.execute("SELECT * FROM KeptTweets WHERE Session=?",(session_id,))
        display_params['num_kept']=len(cur.fetchall())

        display_params['num_displayed']=len(tweets_set)        

        # And we're done
        return(render_template("view_tweets.html",display_params=display_params))
