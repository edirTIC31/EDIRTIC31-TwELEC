########################## Configuration ##########################



# Session password
session_password="password"

# Keys to access the twitter API
c_key = ''
c_secret = ''
a_token = ''
a_secret = ''

# Define the number of search hits to ask per API call
hits_page_size=8

language_string="fr"

session_name="test_session"

# Keep tweets with a zero score
keep_zero_score = False


##################### Do not edit past this line #####################


########################## Type definitions ##########################

# Define session state codes
session_states = { 'running' : 0  }

# Define tweet state codes
tweet_states = { 'unprocessed' : 0, 'processed' : 1, 'pinned' : 2 , 'trashed' : 3 }
