import createDB
import fetchTweets
import processTweets
import displayToStr

from flask import Flask, render_template, request

#####################################################

# Session name
session_name="test session"

# Mandatory keywords
mandatory_keywords=["inondation"]

# Optional keywords
optional_keywords=["urgence"]

# Number of hours to look up before now (< 168h)
hours_before=100

# Language to look for in the tweets
language_string="fr"

# Number of hits per request
hits_page_size=8

# Maximum number of search hits
# may be more depending on
# next multiple of hits_page_size
max_search_hits=35

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
           if passd != "password":
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
    else:
        return(render_template("error.html",cause="Wrong method"))
        
    createDB.createDB()
    fetchTweets.fetchTweets(session_name,
                        mandatory_keywords,
                        optional_keywords,
                        hours_before,
                        language_string,
                        hits_page_size,
                        max_search_hits)
    processTweets.processTweets()
    return(displayToStr.displayToStr())

if __name__ == '__main__':
    app.run(debug=True)
