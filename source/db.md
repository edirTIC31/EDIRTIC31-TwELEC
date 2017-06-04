# Structure de données de la DB


La base de données (Sqlite 3) contient trois tables : 
  * Sessions : éléments décrivant une session (mots clés utilisés, bannis, ...)
  * FetchTweets : tous les tweets récupérés, qu'ils soient intéressants ou non
  * KeptTweets : les tweets qui ne sont pas bannis
  
  ## Sessions
  
 Une session est créée quand un utilisateur s'authentifie et remplit le formulaire initial de recherche.
 
 Une description de session contient des éléments de ce formulaire :
   * Un id : généré automatiquement, c'est la clé primaire.
   * Un nom : généré aléatoirement et de format alphanumérique. 
   * Un état : l'état de la session (à ce jour seul l'état *running* est défini).
   * Des mots clés obligatoires dans la recherche : chaîne de caractères, les mots clés sont séparés par des espaces.
   * Des mots clés optionnels : chaîne de caractères, les mots clés sont séparés par des espaces.
   * Des mots clés bannis : chaîne de caractères, les mots clés sont séparés par des espaces.
   * Un horizon temporel pour effectuer la recerche de tweets : cet horizon permet de remonter dans le passé par rapport au temps présent.
   * La langue dans laquelle il faut effectuer la recherche de tweets.
   * Le nombre maximum de tweets à trouver.
   * Le score minimum d'un tweet pour être comptabilisé dans la liste des résultats. 
   
  ## FetchTweets
  
  FetchedTweets contient tous les tweets récupérés durant les recherches associées aux sessions. 
  
  La table contient un tweet par ligne, une ligne contient les champs suivants :
    * Un ID de session : l'ID de la session se référant à ce Tweet.
    * Un ID de tweet : l'ID (fourni par Twitter) du tweet stocké dans cette ligne
    * Le tweet : le tweet encodé en JSON
    * L'état de ce tweet : de quelle manière est-il pris en compte
      * *unprocessed* : n'a pas encore été traité (=scoré)
      * *processed* : a été traité (=scoré)
      * *processed_new* : a été traité lors de la dernière itération
      * *faved* : marqué comme "favorit" par l'utilisateur
      * *banned* : marqué comme "banni" par l'utilisateur
      
   La clé primaire de cette table est composée de la combinaison de l'ID de session et de tweet.
 
  ## KeptTweets
  
  KeptTweets contient tous les tweets qui ne sont pas bannis pour une session, c'est-à-dire qui 
  contribuent potentiellement aux résultats affichés à l'utilisateur. 
  
  La table contient un tweet par ligne, une ligne contient les champs suivants :
    * Un ID de session : l'ID de la session se référant à ce Tweet.
    * Un ID de tweet : l'ID (fourni par Twitter) du tweet référé par cette ligne
    * Score : le score du tweet
    
  L'objectif de cette table est d'optimisé l'accès .. on pourrait intégrer cette table à *FetchedTweets* 
  mais l'accès serait probablement moins optimisé (tous les champs de cette table ont une longueur fixe).
