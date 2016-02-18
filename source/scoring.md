# Scoring

Le scoring est pour le moment assez simple et fonctionne sur une base bonus/malus.

Il est implanté dans la fonction *scoreTweet() / processTweets.py*

On part d'un score initial de 100. 

  * Si le tweet est un retweet, le score est forcé à 0 (on a déjà matché sur le tweet original)
  * Si le tweet contient un ou plusieurs mots clés optionnels, on bonus de 5 par mot clé présent.
  * S'il n'y a pas de photo, on malus de 10
  * Si le tweet a été re-tweeté, on bonus du nombre de retweets
  * Enfin, on applique un malus exponentiel en fonction de l'age du Tweet. L'âge est normalisé par rapport
    à la profondeur temporelle de recherche. Le malus peut être paramétré pour avoir
    un début plus ou moins plat et ensuite un coude (ce qui ne malus que les tweets 
    proches de la profondeur de recherche). C'est l'objet du paramètre * steepness *
  
Les valeurs des différents bonus/malus sont paramétrables en debut de fichier.
  
    
    # Initial score
    initial_score=100

    # Bonus score when an optional keyword is present
    bonus_optional_keyword=5

    # Malus score when no photo is present
    malus_no_photo=10

    # Max malus for age
    malus_max_age=30

    # Age malus "steepness" [5,10]
    malus_age_steepness=5
    
    ## Les évolutions du scoring
    
Pour le moment, le scoring est presque trivial. On peut envisager imaginer des variantes :
  * Bonus si le tweet contient de l'information de géolocalisation (et s'il avait déjà un bon score précédemment)
  * Bonus en fonction du nombre de mots à fort contenu sémantique : on retire tous les articles, verbes auxiliaires, et
  pourquoi pas des termes *blacklistés* et on "pèse" le tweet

Ce scoring tel qu'il est implanté n'est qu'une première phase d'un algorithme recherche plus évolué qui se déroulerait de la manière suivante :
* Première étape de scoring à partir de mots clés (ce qui est implanté actuellement)
* Feeback de l'utilisateur : celui-ci va épingler les tweets qu'il juge les plus intéressants et éventuellement supprimer ceux qui ne sont pas intéressants
* En fonction du contenu des tweets jugés intéressants, on modifie les règles de scoring; voire les termes de recherche (en prenant en compte les hashtags présents dans les tweets prometteurs) et on relance une recherche
* Pour une information en temps réel, en plus de la recherche, on peut créer une stream qui filtre les tweets en fonction des résultats des étapes précédentes. 
