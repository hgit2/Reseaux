Read me
-> Projet Python L3 BIM, GSELL Louise

Fonctionnement du script :

Ce script est compos� de sept modules (fichiers ��.py��) : recuperation_sequence_fasta, lire_fasta, anayle_ADN, analyse_proteine, creation_seq_aleatoires, analyse_sequence_fasta, et module_de_lancement.  
Il permet d?analyser des s�quences fasta prot�iques ou nucl�iques.
Il peut g�rer aussi bien des fichiers fasta stock�s sur la machine que des fiches fasta en ligne. 
Lors de son fonctionnement, il r�cup�re la s�quence fasta souhait�e et cr�e des fichiers r�sultats tabul�s (fichiers ��.py��) pouvant �tre ouvert en .txt ou avec un tableur comme Excel. Il cr�e �galement dans ce dossier des graphiques (fichiers ��.png��) si l?utilisateur le souhaite, en se basant sur son analyse (� condition que la machine soit �quip�e du module matplotlib, dans le cas contraire il ne cr�e que les fichiers tabul�s). Ces donn�es sont cr��es de mani�re automatique et sont class�es dans un dossier portant comme nom ��Analyse_�� suivit de la description de la s�quence �tudi�e. Ce dossier sera automatiquement export� dans le r�pertoire courant (celui o� se trouve le script).
Ce script offre la possibilit� d?approfondir l?analyse en la r�p�tant sur une ou plusieurs s�quences al�atoires de m�me longueur et de m�me type que la s�quence de r�f�rence et/ou sur une ou plusieurs s�quences al�atoires de m�me composition. Si l?utilisateur fait le choix d?effectuer un ou plusieurs des approfondissements pr�alablement cit�s, tous les fichiers et graphiques g�n�r�s au cours de ces approfondissements seront class�s dans le m�me dossier que la s�quence de r�f�rence. Toutes les pr�cautions n�cessaires sont prises lors de la cr�ation des r�sultats par le script pour ne pas �craser d?�ventuels r�sultats pr�existants. 
Lors de chaque analyse le graphique cr�� s?affiche automatiquement, il n?est pas n�cessaire de l?enregistrer il se trouve d?ores et d�j� dans le dossier appropri�. Cette fen�tre surgissante est simplement l� pour donner un aper�u des r�sultats �tablis, et ainsi aider l?utilisateur � d�cider s?il souhaite approfondir ou non son �tude. L?apparition de cette fen�tre interrompt le programme, pour continuer il suffit de la fermer.

Pr�cautions � prendre :

Ce programme fonctionne sur les syst�me d?exploitations Windows, Linux et OS X.
Pour que le script fonctionne il est imp�ratif que les sept modules (recuperation_sequence_fasta, lire_fasta, anayle_ADN, analyse_proteine, creation_seq_aleatoires, analyse_sequence_fasta, et module_de_lancement) soient regroup�s dans un m�me dossier (le r�pertoire courant).
Si l?�tude porte sur un fichier fasta il doit imp�rativement se trouver dans le m�me r�pertoire que l?ensemble des modules.

Pour lancer le script :

Ouvrir le module module_de_lancement en choisissant ��ouvrir avec��, puis ��IDLE (3.6.0)��. Pour lancer le programme cliquer sur l?onglet ��Run�� (du menu IDLE) puis choisir ��Run module��.
Le script d�roulera alors un menu permettant � l?utilisateur de choisir le type de s�quence qu?il souhaite �tudier (prot�ique ou nucl�ique) puis dans un deuxi�me temps un nom de fichier ou un identifiant permettant d?acc�der � la s�quence qu?il souhaite �tudier. Apr�s quoi l?�tude s?effectuera automatiquement si les entr�es ont �t� correctement donn�es. L?utilisateur aura ensuite le choix entre quitter le programme, commencer l?�tude d?une nouvelle s�quence ou approfondir son �tude en cours.
