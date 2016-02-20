import sqlite3 as lite
import sys
import twelec_globals

def createDB():
    con = None

    with lite.connect('twitter.db') as con:

        cur=con.cursor()

        # Create the session table
        cur.execute("DROP TABLE IF EXISTS Sessions")
        cur.execute("CREATE TABLE Sessions(Name TEXT, State INTEGER, Mkeyw TEXT, OKeyw TEXT, Since INTEGER, Lang TEXT, MaxHits INTEGER)")
  
        # Create the fetched tweets table
        cur.execute("DROP TABLE IF EXISTS FetchedTweets")
        cur.execute("CREATE TABLE FetchedTweets(Session INTEGER, TwID INTEGER PRIMARY KEY, Json TEXT, State INTEGER)")

        # Create the kept tweets table
        cur.execute("DROP TABLE IF EXISTS KeptTweets")
        cur.execute("CREATE TABLE KeptTweets(Session INTEGER, TwID INTEGER, Json TEXT, Score INTEGER)")

  
    if con:
        con.close()
