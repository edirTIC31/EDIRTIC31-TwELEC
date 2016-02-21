# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement un prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...).

Le principe est simple : on fourni des mots clés (ex: "Bordeaux" et "inondation") et TwELEC fait une recherche des tweets
contenant ces termes. Ensuite, il va appliquer un algorithme de scoring (cf [l'explication](./source/scoring.md) dans le répertoire source) pour classer les tweets par ordre d'importance. Et enfin, il affiche le résultat.

Note : cette branche de TwELEC est en cours de développement. Si vous cherchez une version stable --> branche *master*

## Pré-requis

Python 3.x avec les modules *Twitter*, *Flask* et *pytz*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*, *json*,...)

## Format de distribution

Plusieurs fichiers Python à éxécuter en application web (Flask)

## Installation


Configurer le mot de passe de session et les droits d'accès à Twitter dans *twelec_globals.py*

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

## Usage

Deux URL sont disponibles :
  * */createDB* pour créer, réinitialiser la DB (! pour le moment cette fonctionnalité n'est pas protégée par un mot de passe)
  * */* pour démarrer une session de TwELEC

### Démarrage d'une session

(to be completed)


## Les évolutions prévues du code 


  * Gestion des erreurs (un peu meilleure)
  * Evolution de la page d'entrée HTML avec (a) création d'une nouvelle session, (b) ouverture d'une session existante et (c) admin
