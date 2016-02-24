import sqlite3 as lite

# Get a tweet by ID in the FetchedTweets table
def getTweetByID(tweet_id,session_id):

        # Connect to the DB
    with lite.connect('twitter.db') as con:
        cur=con.cursor()

    cur.execute("SELECT * FROM FetchedTweets WHERE TwID=? and Session=?",(tweet_id,session_id))

    row=cur.fetchone()
    return(row)

        
