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

    # Build input field value based on mandatory keywords
    mkwords=json.loads(session[2])

    mkw_field=mkwords[0]
    for mkw in mkwords[1:]:
        mkw_field=mkw_field+" "+mkw

    # Build input field value based on optional keywords
    okwords=json.loads(session[3])

    if len(okwords) > 0 :
        okw_field=okwords[0]
        for okw in okwords[1:]:
            okw_field=okw_field+" "+okw
    else:
        okw_field=""
                
    output="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\
    \"http://www.w3.org/TR/html4/loose.dtd\">\
    <html>\
    <head>\
    <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">\
    <title>Tweet results</title>"
    output=output+"</head>\
    <body>\
    <form name=\"feedback_form\" action=\"/feedback\" method=\"post\">\n"

    output=output+"<H1>Résultats</H1>Recherche des mots-clé <INPUT TYPE=\"TEXT\" NAME=\"mkw\" VALUE=\""+ mkw_field+"\">"+\
    " (obligatoires) et <INPUT TYPE=\"TEXT\" NAME=\"okw\" VALUE=\""+\
    okw_field+"\">"+\
    " (optionnels) "
    if session[4] != -1 :
        output=output+"depuis "+\
        str(session[4])+" heures"
    output=output+\
    "<INPUT TYPE=\"HIDDEN\" NAME=\"session_id\" VALUE=\""+str(session_id)+"\">Coup de pouce <input type=\"checkbox\" name=\"cdp\"><input type=\"submit\" value=\"rafraichir\"><BR><BR>"+\
    "<table style=\"width:100%\" border=1>\
    <tr><th>Score</th><th>Lieu</th><th>Heure et date</th><th>Text</th><th>Image</th><th>J\'aime</th><th>Bannir</th>"

    return output
    
def strTrailer() :
    return("</table><BR><BR>\
    </form>\
    </body>\
    </html>")
        
        
def strTweet(tweet_row,score):

    # Get tweet id and tweet dictionary that will be often accessed
    tweet_id=tweet_row[1]
    tweet=json.loads(tweet_row[2])
    
    # Prepare a string to write to
    # (concatening string would have worked as well)
    output=io.StringIO()

    # The tweet will be print as an HTML table row
    output.write("<tr>")
    
    # Print score
    output.write("<td>"+str(score)+"</td>\n")

    # Print place if any and the related google maps links
    # This part can be improved using the coordinates entry in the tweet dict
    output.write("<td>\n")
    tweet_place=tweet['place']
    if tweet_place!=None:
        output.write("<A HREF=\"http://maps.google.com?q="+cgi.escape(tweet_place['full_name'])+"\" TARGET=_new>"+tweet_place['full_name']+"</A>\n")
    else:
        output.write("Aucun\n")
    output.write("</td>\n")


    # Print date & hour of tweet creation
    output.write("<td>\n")
    output.write(tweet['created_at']+"\n")
    output.write("</td>\n")

    # print text
    output.write("<td>\n")
    # If the tweet is new, display a new icon before the tweet text
    if tweet_row[3] == twelec_globals.tweet_states['processed_new']:
        output.write("<IMG SRC=\""+url_for('static', filename='new_icon.png')+"\" WIDTH=16><A HREF=\"http://www.twitter.com/statuses/"+str(tweet['id'])+\
                     "\" TARGET=_new>"+tweet['text']+"</A>\n")
    else:
        output.write("<A HREF=\"http://www.twitter.com/statuses/"+str(tweet['id'])+"\" TARGET=_new>"+tweet['text']+"</A>\n")
    output.write("</td>\n")

    # Print images - if any
    output.write("<td align=center>")
    try :
        tweet_medias=tweet['entities']['media']
        for tweet_media in tweet_medias:
            if tweet_media['type']=="photo":
                output.write("<a href=\""+tweet_media['media_url_https']+"\" TARGET=_new><img src=\""+tweet_media['media_url_https']+"\" width=100></A>\n")
    except KeyError as e:
        output.write("Aucune\n")

    output.write("</td>\n")

    output.write("<td VALIGN=\"MIDDLE\"><IMG SRC=\""+url_for('static', filename='fav_icon.png')+"\" WIDTH=16><INPUT TYPE=\"checkbox\" NAME=\"fav_"+\
                 str(tweet_id)+"\"></td>\n")
    output.write("<td VALIGN=\"MIDDLE\"><IMG SRC=\""+url_for('static', filename='ban_icon.png')+"\" WIDTH=16><INPUT TYPE=\"checkbox\" NAME=\"ban_"+\
                 str(tweet_id)+"\"></td>\n")
    content=output.getvalue()
    output.close()
    return(content)
  
############################################


# ** TODO ** handle error case
def displayToStr(session_id):

    with lite.connect("twitter.db") as con:

        cur=con.cursor()

        # Get the session data
        session=sessions.getSessionByID(session_id)
        if session == None:
            return(render_template("error.html",cause="Session inexistante"))

        # Build input field value based on mandatory keywords
        mkwords=json.loads(session[2])

        mkw_field=mkwords[0]
        for mkw in mkwords[1:]:
            mkw_field=mkw_field+" "+mkw

        # Build input field value based on optional keywords
        okwords=json.loads(session[3])
            
        if len(okwords) > 0 :
            okw_field=okwords[0]
            for okw in okwords[1:]:
                okw_field=okw_field+" "+okw
        else:
            okw_field=""

        since_field=session[4]
            
        # Retrieve all tweets related to that session
        cur.execute("SELECT TwId, Score FROM KeptTweets WHERE Session=? ORDER BY Score DESC",(session_id,))

        tweets_set=[]
        row=cur.fetchone()
        while row != None:
            # Get tweet data
            tweet_row=tweets.getTweetByID(row[0],session_id)
            # tweet_row[0] is the session id, tweet_row[1] is the tweet id
            # tweet_row{2] is the structure storing the tweet
            tweet=json.loads(tweet_row[2])
            
            tweet_elm={}
            tweet_elm['score']=row[1]
            if tweet['place'] != None:
                tweet_elm['place']=tweet['place']['full_name']
                
            tweet_elm['created_at']=tweet['created_at']

            if tweet_row[3] == twelec_globals.tweet_states['processed_new']:
                tweet_elm['new']=True

            tweet_elm['text']=tweet['text']
                
            tweet_elm['id']=row[0]

            # Create a media entry if any
            medias=[]
            try :
                tweet_medias=tweet['entities']['media']
                for tweet_media in tweet_medias:
                    if tweet_media['type']=="photo":
                        medias.append(tweet_media['media_url_https'])
            except KeyError:
                pass
            if len(medias)>0:
                tweet_elm['medias']=medias

            tweets_set.append(tweet_elm)

            row=cur.fetchone()

        # Switch tweets from the Kept table from 'processed_new' to 'processed'
        cur.execute("UPDATE FetchedTweets SET State=? WHERE Session=? and State=?",(twelec_globals.tweet_states['processed'],session_id,\
                                                                                    twelec_globals.tweet_states['processed_new']))
        
        # And we're done
        return(render_template("view_tweets.html",session_id=session_id,since_field=since_field,mkw_field=mkw_field,okw_field=okw_field,tweets_set=tweets_set))
