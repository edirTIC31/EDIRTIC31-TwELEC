import createDB
import fetchTweets
import processTweets
import displayTweets
import sessions
import twelec_globals
import feedback

from flask import Flask, render_template, request
from random import choice
from string import ascii_uppercase

#####################################################


def validateSearch(m_kw) :
    return(len(m_kw)<=9)

#####################################################

    
app = Flask(__name__)

@app.route('/')
def TwELECForm():
    return(render_template("start.html"))

@app.route('/feedback',methods=['POST'])
def TwELECFeedback():
    return(feedback.feedback(request))

@app.route('/createDB')
def TwELECCreateDB():
    createDB.createDB()
    return(render_template("createDB.html"))
        
@app.route('/fetch',methods=['POST'])
def TwELEC():

    # Fetch form values
    # and replace the default values
    if request.method == 'POST':

        mandatory_keywords=request.form['mkw'].split(" ")

        try:
           passd=request.form['mdp']
           if passd != twelec_globals.session_password:
              return(render_template("error.html",cause="Echec authentification"))
        except KeyError:
              return(render_template("error.html",cause="Echec authentification"))
        
        try:
           optional_keywords=request.form['okw'].split(" ")
        except KeyError:
           optional_keywords=[]

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

        try:
            max_search_hits=request.form['shts']
            if max_search_hits == '':
                max_search_hits=35
            else:
                try:
                    max_search_hits=int(max_search_hits)
                except ValueError:
                    max_search_hits=35
        except KeyError:
            max_search_hits=35
            
    else:
        return(render_template("error.html",cause="Erreur interne envoi formulaire"))

    # Check whether request contrains too many operators
    if not validateSearch(mandatory_keywords):
        return(render_template("error.html",cause="Trop de mots clés, maximum 9 autorisés"))

    # Create a random session name
    session_name=''.join(choice(ascii_uppercase) for i in range(12))
    session_id=sessions.createSession(session_name,
                            mandatory_keywords,
                            optional_keywords,
                            hours_before,
                            twelec_globals.language_string,
                            max_search_hits)
    if session_id==-1 :
        return(render_template("error.html",cause="Erreur de base de données (création de session)"))        
    
    fetchTweets.fetchTweets(twelec_globals.a_token,
                            twelec_globals.a_secret,
                            twelec_globals.c_key,
                            twelec_globals.c_secret,
                            session_id)
    
    processTweets.processTweets(session_id)
    
    return(displayTweets.displayToStr(session_id))

if __name__ == '__main__':
    app.run(debug=True)
