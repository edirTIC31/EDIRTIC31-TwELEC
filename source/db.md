# Structure de données de la DB

(à compléter) 

La base de données (Sqlite 3) contient trois tables : 
  * Sessions : éléments décrivant une session (mots clés utilisés, bannis, ...)
  * FetchTweets : tous les tweets récupérés, qu'ils soient intéressants ou non
  * KeptTweets : les tweets qui ne sont pas bannis
  
  ## Sessions
  
 Une session est créée quand un utilisateur s'authentifie et remplit le formulaire initial de recherche.
 
 Une description de session contient des éléments de ce formulaire :
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
  
  ## KeptTweets
  
  
