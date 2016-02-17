# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...)

## Pré-requis

Python 3.x avec le module *Twitter* et *Flask*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*,*json*,...)

## Format de distribution

Plusieurs fichiers Python à éxécuter soit en ligne de commande. Le résultat de la chaîne est un page HTML, soit 
en application web

## Mode d'emploi

### Pour la ligne de commande

Configurer les paramètres de recherche dans *main.py*

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

Configurer les paramètres d'accès à Twitter dans *fetch.py*

      # Keys to access the twitter API (see http://apps.twitter.com)
      c_key = ''
      c_secret = ''
      a_token = ''
      a_secret = ''


  
Construire une page HTML avec les résultats
    <code>python3 main.py > page.html</code>
    
*createDB.py* permet de re-créer la DB from scratch et *cleanKept.py*
permet de ré-itérer la phase *processTweets.py* sans perdre les résultats
bruts de la recherche

### Pour l'appli web

Configurer les paramètres d'accès à Twitter dans *fetch.py*

      # Keys to access the twitter API (see http://apps.twitter.com)
      c_key = ''
      c_secret = ''
      a_token = ''
      a_secret = ''
    
Pour tester en local : <code>python3 mainWeb.py</code> en utilisant le serveur web intégré de Flask
