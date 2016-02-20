from flask import request
import sqlite3 as lite

import displayTweets
import twelec_globals

def feedback(request):

    session_id=int(request.form['session_id'])

    # Browse all kept tweets and check wether
    # some are marked as to ban or faved
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur_update=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))

        row=cur.fetchone()
        faved_tweets=[]
        while row != None:
            # If the tweet is banned, remove it from the kept table and tag it as banned in the fetched table
            try:
                if request.form['ban_'+str(row[0])]=="on" and 'fav_'+str(row[0]) not in (request.form).keys():                
                    cur_update.execute("DELETE FROM KeptTweets WHERE TwId=?",(row[0],))
                    cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['banned'],row[0]))
            except KeyError:
                pass

            # If the tweet is faved, add it to the faved list
            try:
                if request.form['fav_'+str(row[0])]=="on" and 'ban_'+str(row[0]) not in (request.form).keys():
                    cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['faved'],row[0]))               
                    faved_tweets.append(row[0])
            except KeyError:
                pass

            
            row=cur.fetchone()

        # Process faved tweets
                        
    return(displayTweets.displayToStr(session_id))
