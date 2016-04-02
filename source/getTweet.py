import sqlite3 as lite
import sys
import json

with lite.connect("twitter.db") as con:

    cur_in=con.cursor()

    # Retrieve session data
    session_id=sys.argv[1]
    tweet_id=sys.argv[2]
        
    # Retrieve all tweets related to that session and that are unprocessed
    cur_in.execute("SELECT Json FROM FetchedTweets WHERE Session=? and TwId=?",(session_id,tweet_id))

    row=cur_in.fetchone()
    tweet=json.loads(row[0])
    print(json.dumps(tweet,indent=4))

