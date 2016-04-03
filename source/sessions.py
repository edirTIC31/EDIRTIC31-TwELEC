import sqlite3 as lite
import twelec_globals
import json

# Row factory for returning sessions as dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Creates a new session, returns a session_id
def createSession(session_name,
                  mandatory_keywords,
                  optional_keywords,
                  banned_keywords,
                  hours_before,
                  language_string,
                  max_hits):

        # Connect to the DB
    with lite.connect('twitter.db') as con:
        cur=con.cursor()       

        # Create a new session
        cur.execute("INSERT INTO Sessions VALUES(?,?,?,?,?,?,?,?)",
                    (json.dumps(session_name),
                    twelec_globals.session_states['running'],
                    json.dumps(mandatory_keywords),
                    json.dumps(optional_keywords),
                    json.dumps(banned_keywords),
                    hours_before,
                    json.dumps(language_string),
                    max_hits))

        # Get the ID of the session added as it
        # will be used later for adding tweets
        session_id=cur.lastrowid

        return(session_id)


def getSessionByID(session_id):

        # Connect to the DB
    with lite.connect('twitter.db') as con:
        con.row_factory=dict_factory
        cur=con.cursor()

    cur.execute("SELECT * FROM Sessions WHERE rowid=?",(session_id,))

    row=cur.fetchone()
    return(row)

        
