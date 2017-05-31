# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement un prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...).

Le principe est simple : on fourni des mots clés (ex: "Bordeaux" et "inondation") et TwELEC fait une recherche des tweets
contenant ces termes. Ensuite, il va appliquer un algorithme de scoring (cf [l'explication](./source/scoring.md) dans le répertoire source) pour classer les tweets par ordre d'importance. Et enfin, il affiche le résultat.


## Pré-requis

Python 3.x avec les modules *Twitter*, *Flask*, *matplotlib*, *filelock* et *pytz*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*, *json*,...)

Note : *httplib2* qui est utilisé par Flask peut faire face à un problème de certificats expirés. Le *github* dédié à *httplib2* possède des versions à jour.
Note(2) : sous *Debian/Jessie* l'installation par *pip* de *matplotlib* est un peu délicate et demande un certain nombre de dépendance qu'il faut installer avec *apt* : *libfreetype6-dev* et *libpng12-dev*. 

## Format de distribution

Plusieurs fichiers Python à éxécuter en application web (Flask)

## Documentation

A part ce fichier, il y a deux autres documents : 
  * [Explication du scoring](./source/scoring.md)
  * [Explication de la structure de la DB](./source/db.md)


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
  
Un URL supplémentaire */sessions* est disponible pour visualiser les tweets résultats d'une session. C'est surtout utile à des fins de debugging.

### Démarrage d'une session

La page de démarrage demande de founir :
  * Un mot de passe ... (/no comment/)
  * Des mots clés obligatoires (séparés par des espaces). Ils seront utilisés pour rechercher des Tweets. **Attention** : lorsque Twitter ne trouve pas beaucoup de tweets liés à ces mots clés, il n'honore pas toulours complètement la liste. Ce champ ne peut être laissé vide
  * Des mots clés optionnels : ils sont ... optionnels 
  * Des mots clés à bannir : les tweets contenant ces mots clés auront un score forcé à 0
  * Le nombre d'heures à remonter dans le passé : Twitter limite cette capacité à environ 1 semaines (168 heures). Ceci étant, en mettant '-1', vous demandez à Twitter d'aller aussi loin que possible dans le passé. Une remarque en passant : quand on utilise la fonction *search* de l'application officielle Twitter, il n'y a pas cette limite.
  * Le nombre de tweets à trouver

### L'affichage des résultats

La page des résultats est structurée comme suit :
  * Des informations sur le nombre de tweets trouvés, conservés et affichés.
  * Un lien vers une page qui montre les statistiques des tweets. Pour le moment, ces statistiques se résument à un histogramme de fréquence des mots clés et un autre histogramme sur l'âge des tweets trouvés.
  * Une ligne qui rappelle les mots clés utilisés. A noter que les mots clés peuvent être modifiés.
  * Un case qui permet de spécifier le score minimum qu'un tweet doit avoir pour être éligible à l'affichage
  * Une case à cocher qui permet de demander une suggestion de mots clés (cf plus bas).
  * Un bouton pour rafraîchir les résultats.
  * Un tableau avec une ligne par tweet trouvé. Les informations suivantes sont affichées :
    1. Le score du Tweet. TwELEC calcule un 'score' pour chaque tweet. Les tweets avec les score les plus élevés sont affichés en premier lieu. Le calcul du score est calculé en fonction de plusieurs paramètres (présence d'une image, présence des mots clés optionnels, ...)
    2. L'endroit d'où le tweet a été envoyé (si l'utilisateur le précise). Si c'est le cas, un lien vers *Google Maps* est fourni
    3. L'heure d'envoi du tweet (au format international)
    4. L'utilisateur auteur du tweet (du moins son nickname) 
    5. Le texte du tweet avec un lien vers le tweet original et une icone *new* si ce tweet apparaît pour la première fois dans la liste des résultats
    6. L'image (ou les images) incluses dans le tweet
    7. Un bouton *j'aime* et un bouton *bannir* (voir ci-dessous)

*Bannir un tweet* : celui-ci disparaît de la liste (et dans une même session, il ne va plus réapparaître).

*Aimer un tweet* : les contenus des tweets 'aimés' sont utilisés pour "deviner" des mots clés pertinents ... et la recherche est mise à jour avec ces nouveaux mots clés lors qu'on clique sur le bouton *rafraîchir* (bouton à coté de la liste des mots clés). 

Tous les autres tweets qui ne sont ni bannis, ni aimés sont conservés tels quels. 

Enfin, on peut à la fois aimer et bannir ... mais dans ce cas, il ne se passe rien !

*Suggérer des mots clés optionnels* : à partir de tous tweets affichés, coup de pouce va suggérer des mots clés qu'il rajoutera aux mots clés optionnels. 


## Troubleshooting

L'affichage des statistiques peut être capricieux, surtout s'il n'y a pas de concordance entre (a) l'endroit où sont stockés les fichiers PNG créés (cf. /displayTweetStats.py/) et le code HTML les affichant cf. (/templates//view_tweet_stats.html/).

## Les évolutions prévues du code 


  * Gestion des erreurs (un peu meilleure)
  * Evolution de la page d'entrée HTML avec (a) création d'une nouvelle session, (b) ouverture d'une session existante et (c) admin
