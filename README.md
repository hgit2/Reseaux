Read me
-> Projet Python L3 BIM, GSELL Louise

Fonctionnement du script :

Ce script est composé de sept modules (fichiers « .py ») : recuperation_sequence_fasta, lire_fasta, anayle_ADN, analyse_proteine, creation_seq_aleatoires, analyse_sequence_fasta, et module_de_lancement.  
Il permet d?analyser des séquences fasta protéiques ou nucléiques.
Il peut gérer aussi bien des fichiers fasta stockés sur la machine que des fiches fasta en ligne. 
Lors de son fonctionnement, il récupère la séquence fasta souhaitée et crée des fichiers résultats tabulés (fichiers « .py ») pouvant être ouvert en .txt ou avec un tableur comme Excel. Il crée également dans ce dossier des graphiques (fichiers « .png ») si l?utilisateur le souhaite, en se basant sur son analyse (à condition que la machine soit équipée du module matplotlib, dans le cas contraire il ne crée que les fichiers tabulés). Ces données sont créées de manière automatique et sont classées dans un dossier portant comme nom « Analyse_ » suivit de la description de la séquence étudiée. Ce dossier sera automatiquement exporté dans le répertoire courant (celui où se trouve le script).
Ce script offre la possibilité d?approfondir l?analyse en la répétant sur une ou plusieurs séquences aléatoires de même longueur et de même type que la séquence de référence et/ou sur une ou plusieurs séquences aléatoires de même composition. Si l?utilisateur fait le choix d?effectuer un ou plusieurs des approfondissements préalablement cités, tous les fichiers et graphiques générés au cours de ces approfondissements seront classés dans le même dossier que la séquence de référence. Toutes les précautions nécessaires sont prises lors de la création des résultats par le script pour ne pas écraser d?éventuels résultats préexistants. 
Lors de chaque analyse le graphique créé s?affiche automatiquement, il n?est pas nécessaire de l?enregistrer il se trouve d?ores et déjà dans le dossier approprié. Cette fenêtre surgissante est simplement là pour donner un aperçu des résultats établis, et ainsi aider l?utilisateur à décider s?il souhaite approfondir ou non son étude. L?apparition de cette fenêtre interrompt le programme, pour continuer il suffit de la fermer.

Précautions à prendre :

Ce programme fonctionne sur les système d?exploitations Windows, Linux et OS X.
Pour que le script fonctionne il est impératif que les sept modules (recuperation_sequence_fasta, lire_fasta, anayle_ADN, analyse_proteine, creation_seq_aleatoires, analyse_sequence_fasta, et module_de_lancement) soient regroupés dans un même dossier (le répertoire courant).
Si l?étude porte sur un fichier fasta il doit impérativement se trouver dans le même répertoire que l?ensemble des modules.

Pour lancer le script :

Ouvrir le module module_de_lancement en choisissant « ouvrir avec », puis « IDLE (3.6.0) ». Pour lancer le programme cliquer sur l?onglet « Run » (du menu IDLE) puis choisir « Run module ».
Le script déroulera alors un menu permettant à l?utilisateur de choisir le type de séquence qu?il souhaite étudier (protéique ou nucléique) puis dans un deuxième temps un nom de fichier ou un identifiant permettant d?accéder à la séquence qu?il souhaite étudier. Après quoi l?étude s?effectuera automatiquement si les entrées ont été correctement données. L?utilisateur aura ensuite le choix entre quitter le programme, commencer l?étude d?une nouvelle séquence ou approfondir son étude en cours.
