#!/usr/bin/python3

import sqlite3 as lite
import sys

con = None

with lite.connect('twitter.db') as con:

  cur=con.cursor()

  # Create the kept tweets table
  cur.execute("DROP TABLE IF EXISTS KeptTweets")
  cur.execute("CREATE TABLE KeptTweets(Session INT, Json TEXT, Score INT)")

  
if con:
  con.close()
