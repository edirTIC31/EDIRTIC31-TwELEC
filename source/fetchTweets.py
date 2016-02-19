from twitter import *
import json
from datetime import date
from datetime import timedelta
import sqlite3 as lite
import sys

import twelec_globals

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

def fetchTweets(a_token,
                a_secret,
                c_key,
                c_secret,
                session_id):

    #Setting up access to the Twitter API
    session_auth=OAuth(a_token,a_secret, c_key, c_secret)
    session=Twitter(auth=session_auth)

    # Connect to the DB
    with lite.connect('twitter.db') as con:
        cur=con.cursor()       

        # Retrieve session data
        cur.execute("SELECT * FROM Sessions WHERE rowid==?",(session_id,))
        row=cur.fetchone()

        mandatory_keywords=json.loads(row[2])
        optional_keywords=json.loads(row[3])
        hours_before=row[4]
        language_string=json.loads(row[5])
        max_search_hits=row[6]
         
    # No search hits so far, starting from
    # the "first" tweet
    search_hits=0
    max_id_str=""

    # Build the query string for the twitter search API
    query_string=buildQuery(mandatory_keywords)+" "+buildSince(hours_before)
        
    
    # Start filling the DB with tweets 
    early_finish=False
    while (search_hits < max_search_hits) and not early_finish:

        # Get next search results 
        # max_id is set to "" for the first iteration
        result=session.search.tweets(q=query_string,
                                    lang=language_string,
                                    count=str(twelec_globals.hits_page_size),
                                    max_id=max_id_str)
        
      
        # If any
        if len(result['statuses'])>0 :
            search_hits+=len(result['statuses'])
      
            # add each tweet to the DB
            for status in result['statuses']:
                # Id the tweet already exists, this part is ignored
                cur.execute("INSERT INTO FetchedTweets VALUES(?,?,?,?)",
                            (session_id,
                             status['id'],
                             json.dumps(status),
                             twelec_globals.tweet_states['unprocessed']))

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
    
