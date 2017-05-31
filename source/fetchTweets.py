from twitter import *
import json
from datetime import date
from datetime import timedelta
import sqlite3 as lite
import sys

import twelec_globals
import sessions
import processTweets

#####################################################


def buildQuery(m_kw):
    q_string=m_kw[0]
    # Add all mandatory keywords 
    for kw in m_kw[1:]:
      q_string=q_string+" "+kw

    return q_string

def buildSince(h_bf):

    if h_bf==-1:
      return ""
    
    # Cap number of hours before to max. 168 h (=1 week)
    if h_bf>168:
      h_bf=168

    # Compute since date based on today & number of hours
    s_string="since:"
    since_date=date.today()-timedelta(hours=h_bf)
    s_string=s_string+date.isoformat(since_date)
    
    return s_string


#####################################################

def fetchAndProcessTweets(a_token,
                a_secret,
                c_key,
                c_secret,
                session_id):

    #Setting up access to the Twitter API
    session_auth=OAuth(a_token,a_secret, c_key, c_secret)
    tw_session=Twitter(auth=session_auth)

    # Connect to the DB
    with lite.connect('twitter.db') as con:
        cur=con.cursor()  
        cur_update=con.cursor()     

        # Retrieve session data
        session=sessions.getSessionByID(session_id)

        mandatory_keywords=json.loads(session['MKeyw'])
        optional_keywords=json.loads(session['OKeyw'])
        banned_keywords=json.loads(session['BKeyw'])
        hours_before=session['Since']
        language_string=json.loads(session['Lang'])
         

    max_id_str=""

    # Build the query string for the twitter search API
    query_string=buildQuery(mandatory_keywords)+" "+buildSince(hours_before)
        
    
    # Start filling the DB with tweets 
    early_finish=False

    # Initialise search hits to the number of Tweets that 
    # are complying with the selection criteria so far
    search_hits=processTweets.countKeptTweets(session_id, session['MinimumScore'])
    while (search_hits < session['MaxHits']) and not early_finish:

        # Get next search results 
        # max_id is set to "" for the first iteration
        result=tw_session.search.tweets(q=query_string,
                                    lang=language_string,
                                    count=str(twelec_globals.hits_page_size),
                                    max_id=max_id_str)
        
      
        # If any
        if len(result['statuses'])>0 :
      
            # add each tweet to the DB
            for status in result['statuses']:
                try:

                    # If the tweet already exists, this part is ignored
                    cur.execute("INSERT INTO FetchedTweets VALUES(?,?,?,?)",
                                (session_id,
                                status['id'],
                                json.dumps(status),
                                twelec_globals.tweet_states['processed_new']))

                    # Compute the score ##
                    score=processTweets.scoreTweet(status,session)

                    # If the score is above a certain threshold, update search hits
                    if(score >= session['MinimumScore']):
                       search_hits=search_hits+1 

                    # Update kept table
                    cur_update.execute("INSERT INTO KeptTweets VALUES (?,?,?)",(session_id,status['id'],score))

                    
                except lite.IntegrityError:
                    # This exception is triggered in case a tweet already
                    # saved in a prior instance of the session is inserted
                    # again
                    pass

            # Get max_id from search_metadata: next_results:
            # Example : "next_results": "?max_id=697099148768763903&q=inondation%          # 20AND%20 ...."
            try:
                max_id_str=result['search_metadata']['next_results']
                # The max id field is the first token enclosed between '?' and '&'
                # Careful : this method is not robust to changes of 
                # the URL format 
                max_id_str=(max_id_str.split('&')[0])
                # Remove the "?max_id=" header
                max_id_str=max_id_str[8:]
            except KeyError:
                early_finish=True
        else:
            early_finish=True
      
    # Gracefully the DB connection
    con.commit()

    
