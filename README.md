# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...)

## Pré-requis

Python 3.x avec le module *Twitter*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*,*json*,...)

## Format de distribution

Plusieurs fichier Python à éxécuter en ligne de commande. Le résultat de la chaîne est un page HTML. 
L'intégration web reste à faire (wsgi ? Django ?)

## Mode d'emploi

> Créer la DB : <code>python3 createDB.py</code>

> Configurer les paramètres de recherche dans *fetch.py*

      # Keys to access the twitter API (see http://apps.twitter.com)
      c_key = ''
      c_secret = ''
      a_token = ''
      a_secret = ''


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

> Peupler la base de données avec les résultats de recherche Twitter
    <code>python3 fetch.py</code>
    
> Faire un scoring des résultats
    <code>python3 process.py</code>
    
> Construire une page HTML avec les résultats
    <code>python3 displayToHtml.py > page.html</code>
    
> *createDB.py* permet de re-créer la DB from scratch et *cleanKept.py*
> permet de ré-itérer la phase *process.py* sans perdre les résultats
> bruts de la recherche
    
