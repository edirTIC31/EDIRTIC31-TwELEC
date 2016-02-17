#!/usr/bin/python3

import json
import sqlite3 as lite
import sys
import cgi

############################################

# Session name
session_name="test session"

# Keep tweets with a zero score
keep_zero_score = False

############################################


def printHeader() :
  print("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\
         \"http://www.w3.org/TR/html4/loose.dtd\">\
         <html>\
         <head>\
         <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">\
	     <title>Tweet results</title>\
         </head>\
         <body>\
        <table style=\"width:100%\" border=1>\
        <tr>\
        <th>Score</th><th>Lieu</th><th>Heure et date</th><th>Text</th><th>Image</th>")
    
def printTrailer() :
  print("</table>\
         </body>\
         </html>")
  
    
def printTweet(score,tweet):
  print("<tr>")

  # Print score
  print("<td>"+str(score)+"</td>")
  
  # Print place if any
  print("<td>")
  tweet_place=tweet['place']
  if tweet_place!=None:
    print("<A HREF=\"http://maps.google.com?q="+cgi.escape(tweet_place['full_name'])+"\" TARGET=_new>"+tweet_place['full_name']+"</A>")
  else:
    print("Aucun")
  print("</td>")


  # Print date & hour
  print("<td>")
  print(tweet['created_at'])
  print("</td>")

  # print text
  print("<td>")
  print("<A HREF=\"http://www.twitter.com/statuses/"+str(tweet['id'])+"\" TARGET=_new>>"+tweet['text']+"</A>")
  print("</td>")

 # Print images if any
  print("<td align=center>")
  try :
    tweet_medias=tweet['entities']['media']
    for tweet_media in tweet_medias:
      if tweet_media['type']=="photo":
        print("<a href=\""+tweet_media['media_url_https']+"\" TARGET=_new><img src=\""+tweet_media['media_url_https']+"\" width=100></A>")
  except KeyError as e:
    print("Aucune")
  finally:
    print("</td>")
 
  print("</tr>")

  
############################################


with lite.connect("twitter.db") as con:

  cur=con.cursor()

  # Retrieve the session id
  cur.execute("SELECT rowid,* FROM Sessions WHERE Name=?",(session_name,))

  row=cur.fetchone()
  if row == None:
    print("No Such session as %s",session_name)
    sys.exit(1)

  session_id=row[0]

  # Print HTML headers
  printHeader()
    
  # Retrieve all tweets related to that session
  cur.execute("SELECT Json,Score FROM KeptTweets WHERE Session=? ORDER BY Score DESC",(session_id,))

  row=cur.fetchone()
  while row != None:
    if row[1]!=0 or keep_zero_score:
      printTweet(row[1],json.loads(row[0]))
    row=cur.fetchone()
    
  printTrailer()
