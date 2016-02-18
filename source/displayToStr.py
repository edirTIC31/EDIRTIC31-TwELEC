import json
import sqlite3 as lite
import sys
import cgi
import io
############################################

# Session name
session_name="test session"

# Keep tweets with a zero score
keep_zero_score = False

############################################


def strHeader(session) :
    return("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\
    \"http://www.w3.org/TR/html4/loose.dtd\">\
    <html>\
    <head>\
    <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">\
    <title>Tweet results</title>"+
    "<H1>Résultats</H1>Recherche des mots-clé "+repr(session[3])+" et "+repr(session[4])+" depuis "+str(session[5])+" heures<BR><BR>"+
    "</head>\
    <body>\
    <table style=\"width:100%\" border=1>\
    <tr>\
    <th>Score</th><th>Lieu</th><th>Heure et date</th><th>Text</th><th>Image</th>")
    
def strTrailer() :
    return("</table>\
        </body>\
        </html>")
        
        
def strTweet(id,tweet,score):
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

    output.write("</tr>\n")
    content=output.getvalue()
    output.close()
    return(content)
  
############################################
    
def displayToStr():
    with lite.connect("twitter.db") as con:

        output=""
        cur=con.cursor()

        # Retrieve the session id
        cur.execute("SELECT rowid,* FROM Sessions WHERE Name=?",(session_name,))

        row=cur.fetchone()
        if row == None:
            print("No Such session as %s",session_name)
            sys.exit(1)

        session_id=row[0]
        
        # Print HTML headers
        output=output+strHeader(row)

        # Retrieve all tweets related to that session
        cur.execute("SELECT TwId, Json,Score FROM KeptTweets WHERE Session=? ORDER BY Score DESC",(session_id,))

        row=cur.fetchone()
        while row != None:
            if row[2]!=0 or keep_zero_score:
                output=output+strTweet(row[0],json.loads(row[1]),row[2])
            row=cur.fetchone()
                    
        output=output+strTrailer()
        return(output)
