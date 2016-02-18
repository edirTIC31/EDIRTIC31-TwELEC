# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement un prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...).

Le principe est simple : on fourni des mots clés (ex: "Bordeaux" et "inondation") et TwELEC fait une recherche des tweets
contenant ces termes. Ensuite, il va appliquer un algorithme de scoring (cf [l'explication](./source/scoring.md) dans le répetoire source) pour classer les tweets par ordre d'importance. Et enfin, il affiche le résultat.

## Pré-requis

Python 3.x avec le module *Twitter*, *Flask* et *pytz*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*,*json*,...)

## Format de distribution

Plusieurs fichiers Python à éxécuter soit en ligne de commande soit 
en application web

## Mode d'emploi

### Pour la ligne de commande

Configurer les paramètres de recherche dans *main.py* ainsi que les 
droits d'accès pour l'API Twitter

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

Configurer le mot de passe de session et les droits d'accès à Twitter dans *mainWeb.py*

      # Session password
      s_password="password"

      # Keys to access the twitter API
      c_key = ''
      c_secret = ''
      a_token = ''
      a_secret = ''
    

Pour tester en local : <code>python3 mainWeb.py</code> en utilisant le serveur web intégré de Flask
L'URL '/' est routée sur la page d'entrée.

Enfin, pour l'explication de l'intégration entre Flask, *mod_wsgi* et Apache2, c'est ici : http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
