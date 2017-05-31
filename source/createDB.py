import sqlite3 as lite
import sys
import os
import twelec_globals

def createDB():
    con = None

    with lite.connect('twitter.db') as con:

        cur=con.cursor()

        # Create the session table
        cur.execute("DROP TABLE IF EXISTS Sessions")
        cur.execute("CREATE TABLE Sessions(Name TEXT, State INTEGER, MKeyw TEXT, OKeyw TEXT, BKeyw TEXT, Since INTEGER, Lang TEXT, MaxHits INTEGER, MinimumScore INTEGER)")
  
        # Create the fetched tweets table
        cur.execute("DROP TABLE IF EXISTS FetchedTweets")
        cur.execute("CREATE TABLE FetchedTweets(Session INTEGER, TwID INTEGER, Json TEXT, State INTEGER, PRIMARY KEY(TwID,Session))")

        # Create the kept tweets table
        cur.execute("DROP TABLE IF EXISTS KeptTweets")
        cur.execute("CREATE TABLE KeptTweets(Session INTEGER, TwID INTEGER, Score INTEGER)")

    if con:
        con.close()

    # Clean image files
    os.system("rm static/hta_*.png static/htk_*.png")