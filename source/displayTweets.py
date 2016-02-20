import json
import sqlite3 as lite
import sys
import cgi
import io
from flask import render_template, url_for
import os

import twelec_globals
import sessions
import tweets

############################################


def strHeader(session_id,session) :
    return("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\
    \"http://www.w3.org/TR/html4/loose.dtd\">\
    <html>\
    <head>\
    <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">\
    <title>Tweet results</title>"+
    "<H1>Résultats</H1>Recherche des mots-clé "+repr(json.loads(session[2]))+" et "+repr(json.loads(session[3]))+" depuis "+str(session[4])+" heures<BR><BR>"+
    "</head>\
    <body>"+
    "<form name=\"feedback_form\" action=\"/feedback\" method=\"post\">\n"+
    "<INPUT TYPE=\"HIDDEN\" NAME=\"session_id\" VALUE=\""+str(session_id)+"\">"+  
    "<table style=\"width:100%\" border=1>\
    <tr><th>Score</th><th>Lieu</th><th>Heure et date</th><th>Text</th><th>Image</th><th>J\'aime</th><th>Bannir</th>")
    
def strTrailer() :
    return("</table><BR><BR><center><input type=\"submit\" value=\"envoyer\"></center>\
    </form>\
    </body>\
    </html>")
        
        
def strTweet(tweet_row,score):

    tweet_id=tweet_row[1]
    tweet=json.loads(tweet_row[2])
    
    output=io.StringIO()
    output.write("<tr>")
    
    # Print score
    output.write("<td>"+str(score)+"</td>\n")

    # Print place if any
    output.write("<td>\n")
    tweet_place=tweet['place']
    if tweet_place!=None:
        output.write("<A HREF=\"http://maps.google.com?q="+cgi.escape(tweet_place['full_name'])+"\" TARGET=_new>"+tweet_place['full_name']+"</A>\n")
    else:
        output.write("Aucun\n")
        output.write("</td>\n")


    # Print date & hour
    output.write("<td>\n")
    output.write(tweet['created_at']+"\n")
    output.write("</td>\n")

    # print text
    output.write("<td>\n")
    output.write("<A HREF=\"http://www.twitter.com/statuses/"+str(tweet['id'])+"\" TARGET=_new>>"+tweet['text']+"</A>\n")
    output.write("</td>\n")

    # Print images if any
    output.write("<td align=center>")
    try :
        tweet_medias=tweet['entities']['media']
        for tweet_media in tweet_medias:
            if tweet_media['type']=="photo":
                output.write("<a href=\""+tweet_media['media_url_https']+"\" TARGET=_new><img src=\""+tweet_media['media_url_https']+"\" width=100></A>\n")
    except KeyError as e:
        output.write("Aucune\n")
    finally:
        output.write("</td>\n")

    output.write("<td VALIGN=\"MIDDLE\"><IMG SRC=\""+url_for('static', filename='fav_icon.png')+"\" WIDTH=16><INPUT TYPE=\"checkbox\" NAME=\"fav_"+str(tweet_id)+"\"></td>\n")
    output.write("<td VALIGN=\"MIDDLE\"><IMG SRC=\""+url_for('static', filename='ban_icon.png')+"\" WIDTH=16><INPUT TYPE=\"checkbox\" NAME=\"ban_"+str(tweet_id)+"\"></td>\n")
    content=output.getvalue()
    output.close()
    return(content)
  
############################################
    
def displayToStr(session_id):
    with lite.connect("twitter.db") as con:

        output=""
        cur=con.cursor()

        session=sessions.getSessionByID(session_id)
        if session == None:
            return(render_template("error.html",cause="Session inexistante"))
        
        # Print HTML headers
        output=output+strHeader(session_id,session)

        # Retrieve all tweets related to that session
        cur.execute("SELECT TwId, Score FROM KeptTweets WHERE Session=? ORDER BY Score DESC",(session_id,))

        row=cur.fetchone()
        while row != None:
            if row[1]!=0 or twelec_globals.keep_zero_score:
                tweet=tweets.getTweetByID(row[0])
                output=output+strTweet(tweet,row[1])
            row=cur.fetchone()
                    
        output=output+strTrailer()
        return(output)
