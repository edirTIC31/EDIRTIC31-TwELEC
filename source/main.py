import createDB
import fetchTweets
import processTweets
import displayToHTML


#####################################################

# Session name
session_name="test session"

# Mandatory keywords
mandatory_keywords=["inondation","bordeaux"]

# Optional keywords
optional_keywords=[]

# Number of hours to look up before now (< 168h)
hours_before=72

# Language to look for in the tweets
language_string="fr"

# Number of hits per request
hits_page_size=8

# Maximum number of search hits
# may be more depending on
# next multiple of hits_page_size
max_search_hits=35


# Keys to access the twitter API
c_key = ''
c_secret = ''
a_token = ''
a_secret = ''


#####################################################

createDB.createDB()
fetchTweets.fetchTweets(a_token,
                        a_secret,
                        c_key,
                        c_secret,
                        session_name,
                        mandatory_keywords,
                        optional_keywords,
                        hours_before,
                        language_string,
                        hits_page_size,
                        max_search_hits)

processTweets.processTweets()
displayToHTML.displayToHTML()
