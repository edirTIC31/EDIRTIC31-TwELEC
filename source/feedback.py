from flask import request
import sqlite3 as lite

import displayTweets
import twelec_globals

def feedback(request):

    session_id=int(request.form['session_id'])
    for key in request.form.keys():    
        print(key)

    # Browse all kept tweets and check wether
    # some are marked as to ban
    with lite.connect("twitter.db") as con:

        cur=con.cursor()
        cur_update=con.cursor()
        
        # Retrieve all tweets related to that session that are kept
        cur.execute("SELECT TwId FROM KeptTweets WHERE Session=?",(session_id,))

        row=cur.fetchone()
        while row != None:
            try:
                if request.form['ban_'+str(row[0])]:                
                    cur_update.execute("DELETE FROM KeptTweets WHERE TwId=?",(row[0],))
                    cur_update.execute("UPDATE FetchedTweets SET State=? WHERE TwID=?",(twelec_globals.tweet_states['banned'],row[0]))
            except KeyError:
                pass
            
            row=cur.fetchone()
            
    return(displayTweets.displayToStr(session_id))
