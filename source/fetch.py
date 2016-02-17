from twitter import *
import json
from datetime import date
from datetime import timedelta
import sqlite3 as lite
import sys

# Keys to accessitter API
c_key = ''
c_secret = ''
a_token = ''
a_secret = ''


#####################################################

# Session name
session_name="test session"

# Mandatory keywords
mandatory_keywords=["inondation"]

# Optional keywords
optional_keywords=["urgence"]

# Number of hours to look up before now (< 168h)
hours_before=100

# Language to look for in the tweets
language_string="fr"

# Number of hits per request
hits_page_size=8

# Maximum number of search hits
# may be more depending on
# next multiple of hits_page_size
max_search_hits=35

#####################################################

def validateSearch(m_kw) :
    return(len(m_kw)<=9)

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
  
#Setting up access to thz Twitter API
session_auth=OAuth(a_token,a_secret, c_key, c_secret)
session=Twitter(auth=session_auth)

# Check whether request contrains too many operators
if not validateSearch(mandatory_keywords):
  print("Query too complex for Twitter Search API")
  sys.exit(1)

# Connect to the DB
with lite.connect('twitter.db') as con:
  cur=con.cursor()

  # Create a new session
  cur.execute("INSERT INTO Sessions VALUES(?,0,?,?,?,?)",
              (session_name,
               json.dumps(mandatory_keywords),
               json.dumps(optional_keywords),
               buildSince(hours_before),
               language_string))

  # Get the ID of the session added as it
  # will be used later for adding tweets
  session_id=cur.lastrowid            

  # Not searc hists so far, starting from
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
                                 count=str(hits_page_size),
                                 max_id=max_id_str)
      
    # If any
    if len(result['statuses'])>0 :
      search_hits+=len(result['statuses'])
      
      # add each tweet to the DB
      for status in result['statuses']:
        cur.execute("INSERT INTO FetchedTweets VALUES(?,?)",
                    (session_id,
                    json.dumps(status)))

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
    
