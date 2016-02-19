import sqlite3 as lite
import twelec_globals
import json

def createSession(session_name,
                  mandatory_keywords,
                  optional_keywords,
                  hours_before,
                  language_string,
                  max_hits):

        # Connect to the DB
    with lite.connect('twitter.db') as con:
        cur=con.cursor()       

        # Create a new session
        cur.execute("INSERT INTO Sessions VALUES(?,?,?,?,?,?,?)",
                    (session_name,
                    twelec_globals.session_states['running'],
                    json.dumps(mandatory_keywords),
                    json.dumps(optional_keywords),
                    hours_before,
                    json.dumps(language_string),
                    max_hits))

        # Get the ID of the session added as it
        # will be used later for adding tweets
        session_id=cur.lastrowid

        return(session_id)