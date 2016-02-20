from flask import request

import displayTweets

def feedback(request):

    session_id=int(request.form['session_id'])
    
    return(displayTweets.displayToStr(session_id))
