import createDB
import fetchTweets
import processTweets
import displayTweets
import displayTweetsStats
import sessions
import twelec_globals
import feedback

from flask import Flask, render_template, request, send_file, make_response
from random import choice
from string import ascii_uppercase

#####################################################


def validateSearch(m_kw) :
    return(len(m_kw)<=9)

#####################################################

    
app = Flask(__name__)

# Start page for keyword input & other parameters
@app.route('/')
def TwELECForm():
    return(render_template("start.html"))

# Feedback script for processing favs and banned tweets
@app.route('/feedback',methods=['POST'])
def TwELECFeedback():
    return(feedback.feedback(request))

# Utility script for creating the DB
# The routing can be renamed to add a little bit of secrecy
@app.route('/createDB')
def TwELECCreateDB():
    createDB.createDB()
    return(render_template("createDB.html"))
    
@app.route('/displayTweetsStats',methods=['GET'])
def TwELECDisplayTweetsStats():
    try:
        session_id=request.args['session_id']
    except KeyError:
        return(render_template("error.html",cause="Paramètres GET mal formatés"))

    return(displayTweetsStats.displayTweetsStats(session_id))

@app.route('/fig/HistoKeywords/<session_id>')
def figHistoKeywords(session_id):
    img=displayTweetsStats.drawHistoKeywords(session_id)
    response = make_response(send_file(img, mimetype='image/png',attachment_filename='hkw.png'))
    response.headers['Pragma-directive'] = 'no-cache'
    response.headers['Cache-directive'] = 'no-cache'
    response.headers['Cache-control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/fig/HistoTweetAge/<session_id>')
def figHistoTweetAge(session_id):
    img=displayTweetsStats.drawHistoTweetAge(session_id)
    response = make_response(send_file(img, mimetype='image/png',attachment_filename='hta.png'))
    response.headers['Pragma-directive'] = 'no-cache'
    response.headers['Cache-directive'] = 'no-cache'
    response.headers['Cache-control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/sessions')
def TwELECsessions():
    return(render_template("view_session.html"))

@app.route('/viewSession',methods=['POST'])
def TwELECViewSession():

    # Authentification
    try:
        passd=request.form['mdp']
        if passd != twelec_globals.session_password:
            return(render_template("error.html",cause="Echec authentification"))
    except KeyError:
        return(render_template("error.html",cause="Echec authentification"))

    try:
         session_id=int(request.form['sid'])
    except KeyError:
        return(render_template("error.html",cause="Id de session absent"))
    except ValueError:
        return(render_template("error.html",cause="Id de session invalide"))
    
    
    return(displayTweets.displayToStr(session_id))
    
    
# Tweet search script from keywords proposed in '/'
@app.route('/fetch',methods=['POST'])
def TwELEC():

    # Fetch form values
    # and replace the default values
    if request.method == 'POST':

        # Parsing of the mandatory keywords
        try:
            # ** TODO ** : rajouter la suppresion d'espaces excedentaires
            mandatory_keywords=request.form['mkw'].split(" ")
        except KeyError:
            return(render_template("error.html",cause="Pas de mot clé obligatoire fourni"))

        # Authentification
        try:
           passd=request.form['mdp']
           if passd != twelec_globals.session_password:
              return(render_template("error.html",cause="Echec authentification"))
        except KeyError:
              return(render_template("error.html",cause="Echec authentification"))
        
        # Parsing od the optional keywords
        # ** TODO ** Rajouter la suppresion des espaces excedentaires
        try:
           optional_keywords=request.form['okw'].split(" ")
        except KeyError:
           optional_keywords=[]

        # Parsing of the banned keywords
        # ** TODO ** Rajouter la suppresion des espaces excedentaires
        try:
           banned_keywords=request.form['bkw'].split(" ")
        except KeyError:
           banned_keywords=[]

        # Parsing of the depth of search (in hours past now)
        # -1 means unspecified
        try:
            hours_before=request.form['hbf']
            if hours_before == '':
                hours_before=-1
            else:
                try:
                    hours_before=int(hours_before)
                except ValueError:
                    hours_before=-1
        except KeyError:
            hours_before=-1

        # Parsing of the number of hits to look for           
        try:
            max_search_hits=request.form['shts']
            if max_search_hits == '':
                max_search_hits=twelec_globals.default_search_hits
            else:
                try:
                    max_search_hits=int(max_search_hits)
                except ValueError:
                    max_search_hits=twelec_globals.default_search_hits
        except KeyError:
            max_search_hits=twelec_globals.default_search_hits
            
    else:
        return(render_template("error.html",cause="Erreur interne envoi formulaire"))

    # Check whether the request contrains too many operators
    if not validateSearch(mandatory_keywords):
        return(render_template("error.html",cause="Trop de mots clés, maximum 9 autorisés"))

    # Create a random session name
    session_name=''.join(choice(ascii_uppercase) for i in range(12))

    # Create the session in the DB
    session_id=sessions.createSession(session_name,
                            mandatory_keywords,
                            optional_keywords,
                            banned_keywords,
                            hours_before,
                            twelec_globals.language_string,
                            max_search_hits,
                            twelec_globals.keep_zero_score)
    if session_id==-1 :
        return(render_template("error.html",cause="Erreur de base de données (création de session)"))        

    # Fetch the tweets using the Twitter API
    fetchTweets.fetchTweets(twelec_globals.a_token,
                            twelec_globals.a_secret,
                            twelec_globals.c_key,
                            twelec_globals.c_secret,
                            session_id)
    # Score tweets
    processTweets.processTweets(session_id)

    # Display tweets
    return(displayTweets.displayToStr(session_id))

if __name__ == '__main__':
    app.run(debug=True)
