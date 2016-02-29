# EDIRTIC31-TwELEC
Projet TwELEC (ELEC par Twitter) de l'EDIR TIC 31

TwELEC est un outil (actuellement un prototype) de recherche de fils twitter par rapport à un évènement (accident, catastrophe, ...).

Le principe est simple : on fourni des mots clés (ex: "Bordeaux" et "inondation") et TwELEC fait une recherche des tweets
contenant ces termes. Ensuite, il va appliquer un algorithme de scoring (cf [l'explication](./source/scoring.md) dans le répertoire source) pour classer les tweets par ordre d'importance. Et enfin, il affiche le résultat.

Note : cette branche de TwELEC est en cours de développement. Si vous cherchez une version stable --> branche *master*

## Pré-requis

Python 3.x avec les modules *Twitter*, *Flask*, *matplotlib*, *filelock* et *pytz*, les autres modules sont normalement en standard avec Python 3.x (*sqlite3*, *json*,...)

Note : *httplib2* qui est utilisé par Flask peut faire face à un problème de certificats expirés. Le *github* dédié à *httplib2* possède des versions à jour.
Note(2) : sous *Debian/Jessie* l'installation par *pip* de *matplotlib* est un peu délicate et demande un certain nombre de dépendance qu'il faut installer avec *apt* : *libfreetype6-dev* et *libpng12-dev*. 

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
  
Un URL supplémentaire */sessions* est disponible pour visualiser les tweets résultats d'une session. C'est surtout utile à des fins de debugging.

### Démarrage d'une session

La page de démarrage demande de founir :
  * Un mot de passe ... (/no comment/)
  * Des mots clés obligatoires (séparés par des espaces). Ils seront utilisés pour rechercher des Tweets. **Attention** : lorsque Twitter ne trouve pas beaucoup de tweets liés à ces mots clés, il n'honore pas toulours complètement la liste. Ce champ ne peut être laissé vide
  * Des mots clés optionnels : ils sont ... optionnels 
  * Le nombre d'heures à remonter dans le passé : Twitter limite cette capacité à environ 1 semaines (168 heures). Ceci étant, en mettant '-1', vous demandez à Twitter d'aller aussi loin que possible dans le passé. Une remarque en passant : quand on utilise la fonction *search* de l'application officielle Twitter, il n'y a pas cette limite.
  * Le nombre de tweets à trouver

### L'affichage des résultats

La page des résultats est structurée comme suit :
  * Une ligne qui rappelle les mots clés utilisés et - si c'était précisé - le nombre d'heures à remonter dans le passé. A noter que les mots clés peuvent être modifiés. Un lien est fourni vers une page qui montre les statistiques des tweets. Pour le moment, ces statistiques se résument à un histogramme de fréquence des mots clés).
  * Une ligne avec un bouton *rafraîchir* et une case *coup de pouce* décrite ci-dessous.
  * Un tableau avec une ligne par tweet trouvé. Les informations suivantes sont affichées :
    1. Le score du Tweet. TwELEC calcule un 'score' pour chaque tweet. Les tweets avec les score les plus élevés sont affichés en premier lieu. Le calcul du score est calculé en fonction de plusieurs paramètres (présence d'une image, présence des mots clés optionnels, ...)
    2. L'endroit d'où le tweet a été envoyé (si l'utilisateur le précise). Si c'est le cas, un lien vers *Google Maps* est fourni
    3. L'heure d'envoi du tweet (au format international)
    4. Le texte du tweet avec un lien vers le tweet original et une icone *new* si ce tweet apparaît pour la première fois dans la liste des résultats
    5. L'image (ou les images) incluses dans le tweet
    6. Un bouton *j'aime* et un bouton *bannir* (voir ci-dessous)

*Bannir un tweet* : celui-ci disparaît de la liste (et dans une même session, il ne va plus réapparaître).

*Aimer un tweet* : le contenu du tweet 'aimés' est utilisé pour "deviner" des mots clés pertinents ... et la recherche est mise à jour avec ces nouveaux mots clés lors qu'on clique sur le bouton *rafraîchir* (bouton à coté de la liste des mots clés). 

Tous les autres tweets qui ne sont ni bannis, ni aimés sont conservés tels quels. 

Enfin, on peut à la fois aimer et bannir ... mais dans ce cas, il ne se passe rien !

*Coup de pouce* : à partir de tous tweets affichés, coup de pouce va suggérer des mots clés qu'il rajoutera aux mots clés optionnels. 



## Les évolutions prévues du code 


  * Gestion des erreurs (un peu meilleure)
  * Evolution de la page d'entrée HTML avec (a) création d'une nouvelle session, (b) ouverture d'une session existante et (c) admin
