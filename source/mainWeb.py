import createDB
import fetchTweets
import processTweets
import displayToStr
import sessions
import twelec_globals

from flask import Flask, render_template, request

#####################################################


def validateSearch(m_kw) :
    return(len(m_kw)<=9)

#####################################################

    
app = Flask(__name__)

@app.route('/')
def TwELECForm():
    return(render_template("start.html"))

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
        return(render_template("error.html",cause="Wrong method"))

    # Check whether request contrains too many operators
    if not validateSearch(mandatory_keywords):
        return(render_template("error.html",cause="Too many keywords for the Twitter API, up to 9 allowed"))


    createDB.createDB()
    session_id=sessions.createSession(twelec_globals.session_name,
                            mandatory_keywords,
                            optional_keywords,
                            hours_before,
                            twelec_globals.language_string,
                            max_search_hits)
    if session_id==-1 :
        return(render_template("error.html",cause="Database error (session creation)"))        
    
    fetchTweets.fetchTweets(twelec_globals.a_token,
                            twelec_globals.a_secret,
                            twelec_globals.c_key,
                            twelec_globals.c_secret,
                            session_id)
    
    processTweets.processTweets(session_id)
    
    return(displayToStr.displayToStr(session_id))

if __name__ == '__main__':
    app.run(debug=True)
