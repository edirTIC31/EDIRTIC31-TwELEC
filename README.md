# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement un prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...).

Le principe est simple : on fourni des mots clés (ex: "Bordeaux" et "inondation") et TwELEC fait une recherche des tweets
contenant ces termes. Ensuite, il va appliquer un algorithme de scoring (cf [l'explication](./source/scoring.md) dans le répetoire source) pour classer les tweets par ordre d'importance. Et enfin, il affiche le résultat.

## Pré-requis

Python 3.x avec les modules *Twitter*, *Flask* et *pytz*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*, *json*,...)

## Format de distribution

Plusieurs fichiers Python à éxécuter en application web via Flask

## Mode d'emploi

Configurer le mot de passe de session et les droits d'accès à Twitter dans *twelec_globals.py*

      # Session password
      s_password="password"

      # Keys to access the twitter API
      c_key = ''
      c_secret = ''
      a_token = ''
      a_secret = ''
    
    
Eventuellement, ajuster les autres paramètres dans *twelec_globals.py*

      # Define the number of search hits to aim to
      global_hits=80

      # Define the number of search hits to ask per API call
      hits_page_size=20

      # Language option for Twitter search
      language_string="fr"

      # How often should we see a keyword
      # from the fav list to promote it as mandatory keywords
      faved_frequency_threshold=3

      # How often should we see a keyword
      # from the tweet list to promote it as mandatory keywords hint it
      hint_frequency_threshold=2

      # Minimum score expected from a tweet
      minimum_eligible_score=10

      # List of stop words
      stop_words=["-elle",

Avant tout usage, il faut initialiser la base de données en invoquant l'URL '.../createDB'

Pour tester en local : <code>python3 mainWeb.py</code> en utilisant le serveur web intégré de Flask
L'URL '/' est routée sur la page d'entrée.

Enfin, pour l'explication de l'intégration entre Flask, *mod_wsgi* et Apache2, c'est ici : http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
