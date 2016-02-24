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

# Default number of search hits
default_search_hits=35

language_string="fr"

# Keep tweets with a zero score
keep_zero_score = False

# How often should we see a keyword
# from the fav list to promote it as mandatory keywords
faved_frequency_threshold=3

# How often should we see a keyword
# from the tweet list to promote it as mandatory keywords hint it
hint_frequency_threshold=2


# List of stop words
stop_words=["-elle","-il","10ème","1er","1ère","2ème","3ème","4ème","5ème","6ème","7ème","8ème","9ème","a","afin","ai","ainsi","ais","ait","alors","après","as","assez","au","aucun","aucune","auprès","auquel","auquelles","auquels","auraient","aurais","aurait","aurez","auriez","aurions","aurons","auront","aussi","aussitôt","autre","autres","aux","avaient","avais","avait","avant","avec","avez","aviez","avoir","avons","ayant","beaucoup","c'","car","ce","ceci","cela","celle","celles","celui","cependant","certes","ces","cet","cette","ceux","chacun","chacune","chaque","chez","cinq","comme","d'","d'abord","dans","de","dehors","delà","depuis","des","dessous","dessus","deux","deça","dix","doit","donc","dont","du","durant","dès","déjà","elle","elles","en","encore","enfin","entre","er","est","est-ce","et","etc","eu","eurent","eut","faut","fur","hormis","hors","huit","il","ils","j'","je","jusqu'","l'","la","laquelle","le","lequel","les","lesquels","leur","leurs","lors","lorsque","lui","là","m'","mais","malgré","me","melle","mes","mm","mme","moi","moins","mon","mr","même","mêmes","n'","neuf","ni","non-","nos","notamment","notre","nous","néanmoins","nôtres","on","ont","ou","où","par","parce","parfois","parmi","partout","pas","pendant","peu","peut","peut-être","plus","plutôt","pour","pourquoi","près","puisqu'","puisque","qu'","quand","quant","quatre","que","quel","quelle","quelles","quelqu'","quelque","quelquefois","quelques","quels","qui","quoi","quot","s'","sa","sans","se","sept","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","si","sien","siennes","siens","sitôt","six","soi","sommes","son","sont","sous","souvent","suis","sur","t'","toi","ton","toujours","tous","tout","toutefois","toutes","troiw","tu","un","une","unes","uns","voici","voilà","vos","votre","vous","vôtres","y","à","ème","étaient","étais","était","étant","étiez","étions","êtes","être","afin","ainsi","alors","après","aucun","aucune","auprès","auquel","aussi","autant","aux","avec","car","ceci","cela","celle","celles","celui","cependant","ces","cet","cette","ceux","chacun","chacune","chaque","chez","comme","comment","dans","des","donc","donné","dont","duquel","dès","déjà","elle","elles","encore","entre","étant","etc","été","eux","furent","grâce","hors","ici","ils","jusqu","les","leur","leurs","lors","lui","mais","malgré","mes","mien","mienne","miennes","miens","moins","moment","mon","même","mêmes","non","nos","notre","notres","nous","notre","oui","par","parce","parmi","plus","pour","près","puis","puisque","quand","quant","que","quel","quelle","quelque","quelquun","quelques","quels","qui","quoi","sans","sauf","selon","ses","sien","sienne","siennes","siens","soi","soit","sont","sous","suis","sur","tandis","tant","tes","tienne","tiennes","tiens","toi","ton","tous","tout","toute","toutes","trop","très","une","vos","votre","vous","étaient","était","étant","être"]

##################### Do not edit past this line #####################


########################## Type definitions ##########################

# Define session state codes
session_states = { 'running' : 0  }

# Define tweet state codes
tweet_states = { 'unprocessed' : 0, 'processed' : 1, 'processed_new':2, 'faved' : 3 , 'banned' : 4 }
