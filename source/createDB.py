import sqlite3 as lite
import sys

def createDB():
    con = None

    with lite.connect('twitter.db') as con:

        cur=con.cursor()

        # Create the session table
        cur.execute("DROP TABLE IF EXISTS Sessions")
        cur.execute("CREATE TABLE Sessions(Name TEXT, State INT, Mkeyw TEXT, OKeyw TEXT, Since INT, Lang TEXT)")
  
        # Create the fetched tweets table
        cur.execute("DROP TABLE IF EXISTS FetchedTweets")
        cur.execute("CREATE TABLE FetchedTweets(Session INT, Json TEXT)")

        # Create the kept tweets table
        cur.execute("DROP TABLE IF EXISTS KeptTweets")
        cur.execute("CREATE TABLE KeptTweets(Session INT, Json TEXT, Score INT)")

  
    if con:
        con.close()
