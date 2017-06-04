# Architecture du code

Le code est architecturé autour de trois catégories de module Python
  - Un module de point d'entrée de Flask : *mainWeb.py* 
  
  - Des modules de gestion des données : 
    * *createDB.py* : création de la DB sqlite
    * *sessions.py* : accès aux sessions dans la DB
    * *tweets.py* : accès aux tweets de la DB
    * *twelec_globals* : variables globales de Twelec
    * *getTweet.py* : programme ligne de commande utilisé à des fins de debugging qui affiche un tweet d'une session
    * *cleanKept.py* : module de debugging pour vider la table *KeptTweets*
    
  - Des modules de gestion de données :
    * *fetchTweets.py* : recherche de tweets sur Twitter en fonction des mots clés et mise à jour des tables *FetchedTweets*. Application du scoring sur 
    ces tweets (en utilisant *processTweets.py*- et mise à jour de la table *KeptTweets*
    * *processTweets.py* : calcul du score d'un tweet 
    * *feedback.py* : mise à jour des score de tweets en fonction 
    * *displayTweets.py* : affichage des tweets trouvés et rappels des paramètres de la session 
    * *displayTweetStats.py* : affichage de quelques statistiques sur les tweets trouvés et présentant un score intéressant pour l'utilisateur
    
  A cela s'ajoute les templates HTML (répertoire *templates*) pour générer les différentes pages web (cf. documentation Flask pour la syntaxe des templates).
  
  ## Schéma typique d'usage/appel des modules
  
   - *mainWeb.py* lorsque l'URL "/" est invoqué
   - *mainWeb.py* --> *fetchTweets.py* --> *processTweets.py* --> *displayTweets.py* pour la première recherche
   - *mainWeb.py* --> *feedback.py* --> *processTweets.py* --> *fetchTweets.py* --> *processTweets.py* --> *displayTweets.py* pour l'intégration du feedback utilisateur 
   - *mainWeb.py* --> *displayTweetStats* pour l'affichage des statistiques (dans un onglet navigateur séparé)
