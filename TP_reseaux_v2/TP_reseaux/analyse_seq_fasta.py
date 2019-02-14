#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Projet Réseaux 4BIM
#                                                             Analyse de sequences fasta
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import recuperation_sequence_fasta as rs
import analyse_ADN as an
import analyse_proteine as ap
import creation_seq_aleatoires as csa
import os
import socket

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
plot_dispo=False # à gérer PLUS TARD
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def resultat_ADN(des,seq,con, compo=-1,keys=-1,plot_dispo=-1): 
    # Permet d'obtenir les tableaux de resultats et les graphiques correspondants de l'annalyse de la sequence ADN.
    "Pour fonctionner ce module fait appel a cinq autres modules qui doivent se trouver dans le meme repertoire courant que lui : recuperation_sequence_fasta, lire_fasta, analyse_ADN, analyse_proteine, et creation_seq_aleatoires. Cette procedure permet d'effectuer une etude de sequence nucleique. Cette etude consiste en un calcul du pourcentage de C+G et de CpG dans la sequence entiere, et en un calcule du rapport CpG, du pourcentage de C+G, et du nombre de CpG par fenetre glissante de deux cents nucleotides ainsi qu'une conclsion sur la presence ou non d'ilots CpG. La procedure cree un a deux fichiers de sortie : un fichier tabule (pouvant etre ouvert avec un editeur de texte ou un tableur comme Excel) et une image des graphiques qu'elle engendre sous certaines conditions. Elle prend en arguments une description et la sequence correspondante au minimum. En troisieme argument elle prend la composition de la sequence (compo=) sous forme de dictionnaire, par defaut cette composition est calculee dans la procedure. De meme en quatrieme argument elle prend la liste des caracteres composants la sequence (keys=) (chacun ecrit entre guillemets), par defaut cette liste est calculee par la procedure. En dernier argument elle prend le boleen plot_dispo qui par defaut vaut True si le poste de tavail dispose de l'installation du module 'matplotlib' et False sinon, si l'utilisateur choisit d'entree plot_dispo=True en argument il doit lui meme s'assurere de cette installation au prealable, si au contraire il rentre plot_dispo=False, les graphiques ne seront pas generes."  
    if compo==-1: # Permet une utilisation dans un cas plus general dans lequel l'utilisateur ne disposerait pas de la composition de la sequnece.
        compo=an.composition(seq,con)
    if keys==-1: # Permet une utilisation dans un cas plus general dans lequel l'utilisateur ne disposerait pas d'une liste des caractères composants la sequnece.
        keys=[]
        for key in compo.keys():
            keys.append(key)
    if plot_dispo==-1: # Permet une utilisation plus generale pour laquelle l'utilisateur n'aurait pas a choisir s'il souhaite ou non tracer les graphiques.
        plot_dispo=plt_dispo
    nom_fichier="Analyse_seq_nucl"+des           
    fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
    numero_fichier=0
    while fichier_existe: # Tant que le fichier "nom_fichier.py" existe le nom change.
        try: 
            sortie=open(nom_fichier+"(%i).py" % numero_fichier,'r') # Test si le fichier "nom.py" existe.
        except FileNotFoundError: 
            fichier_existe=False # Le fichier n'existe pas on peut donc le creer sans prendre le risque d'en ecraser un preexistant.
        else:
            sortie.close()
            numero_fichier+=1
            nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier) # Si le fichier "nom_fichier.py" existe on change de nom pour ne pas l'ecraser.
    sortie=open(nom_fichier+"(%i).py" % numero_fichier,'a')
    CG,pourcentCpG=an.contenu_C_et_G_et_nb_CpG(seq,con, comp=compo) # Recuperation du pourcentage de C+G dans la sequence.
    pourcentCpG=pourcentCpG[0]/len(seq)*100 # Recuperation  de nombre de "CG" dans la sequence.
    num_fenetre=[]
    sortie.write("\tC+G(%)\tCpG(%)") # Redaction des entetes du tableau resultat consernant l'etude de la sequence entiere.
    resultats="\n sequence entiere\t%.3f" % CG[0] + "\t%.3f" % pourcentCpG # Puis des resultats correspondants.
    for ele in keys:
        sortie.write("\t"+str(ele))
        resultats+="\t"+str(compo[str(ele)])
    resultats=resultats.replace(".",",")
    sortie.write(resultats)
    if len(seq)>=200: # Si la longueur de la sequence est inferieure a 200 nucleotides, cette partie de l'annalyse n'a pas pu etre effectuee car elle necessite des fenetres glissantes de 200 nucleotides.
        sortie.write("\n \n \nFenetres\tC+G(%)\tCpG\tRapport CpG\tIlot CpG\n") # Redaction des entetes du tableau resultat consernant l'etude de la sequence par fenetres glissantes. 
        rapportCpG,CpGfenetre,CGfenetre=an.rapport_CpG_nb_CpG_contenu_C_et_G(seq,200,con)# Recuperation du porcentage de C+G dans chaque fenetre, du nombre de "CG" et du rapport CpG.
        ilot_CpG=False
        plt_rapportCpG=True
        for i,ele in enumerate(CGfenetre): # On parcours l'une des liste de resultat de l'annalyse par fenetre, elles ont toutes la meme taille.
            num_fenetre.append(i+1)
            if rapportCpG[i]!="NA":
                if rapportCpG[i]>=0.6 and CGfenetre[i]>=50: # Permet de verifier la presence d'ilot CpG.
                    ilot_CpG=True
                    resultatsfenetres=str(i+1)+"\t%.3f" % CGfenetre[i] +"\t"+str(CpGfenetre[i])+"\t%.3f" % rapportCpG[i] +"\tOui\n" # Redaction des resultats obtenus pour la fenetre i (si presence d'un ilot CpG,cf "else" sinon)
                    if plot_dispo:
                        plt.subplot(222) # Ensemble de commande permettant de faire apparaitre les ilots CpG en rouge sur les graphiques.
                        plt.plot([i+1],[rapportCpG[i]],'.r')
                        plt.subplot(224)
                        plt.plot([i+1],[CGfenetre[i]],'.r')
                else:
                    resultatsfenetres=str(i+1)+"\t%.3f" % CGfenetre[i] +"\t"+str(CpGfenetre[i])+"\t%.3f" % rapportCpG[i] +"\tNon\n"
            else:
                resultatsfenetres=str(i+1)+"\t%.3f" % CGfenetre[i] +"\t"+str(CpGfenetre[i])+"\t%s" % rapportCpG[i] +"\tNon\n"
                plt_rapportCpG=False
            resultatsfenetres=resultatsfenetres.replace(".",",") # On remplace les points par des virgules pour que les valeurs soient reconnus comme des nombres par Excel
            sortie.write(resultatsfenetres)
        sortie.close()
        if plot_dispo :
            if plt_rapportCpG: # Pour ne pas afficher le graph CpG si certaine valeur de rapportCpG valent "NA".
                plt.subplot(222) # Ensemble de commandes permettants de tracer les graphiques resultats. Ici pour determiner la place du graphique dasn la fenetre surgissante.
                plt.title("Analyse de la presence d'ilots CpG\npour chaque fenetres glissantes de 200 nucleotides\nde la sequence") # Pour ajouter un titre.
                plt.grid() # Pour que la grille soit apparente.
                plt.plot(num_fenetre,rapportCpG,color='b')
                plt.axhline(0.6, linestyle=':', color='r')
                plt.ylabel("Rapports CpG") # Pour choisir le titre de l'axe des ordonnees.
                if ilot_CpG:
                    plt.text(0,max(rapportCpG)-0.1, "Ilot CpG", fontsize=10,color='b',bbox=dict(boxstyle="square,pad=0.3",fc="r",ec="w", lw=2)) # Pour faire apparaitre du texte en bleu dans un cadre blanc sur fond rouge.
                plt.subplot(224)
            else:
                plt.subplot(222)
            plt.grid()
            plt.plot(num_fenetre,CGfenetre,color='b')
            plt.axhline(50, linestyle=':', color='r')
            plt.xlabel("Numero des fenetres glissantes") # Permet de choisir le titre de l'axe des abcisses.
            plt.ylabel("Pourcentages de C+G")
            if ilot_CpG:
                plt.text(0,max(CGfenetre)-5, "Ilot CpG", fontsize=10,color='b',bbox=dict(boxstyle="square,pad=0.3",fc="r",ec="w", lw=2))
            fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
            numero_fichier=0
            while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
                try: 
                    sortie=open(nom_fichier+"(%i).png" % numero_fichier,'r') # Test si le fichier "nom_fichier.py" existe.
                except FileNotFoundError: 
                    fichier_existe=False
                else:
                    sortie.close()
                    numero_fichier+=1
                    nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier) # Si le fichier "nom_fichier.png" existe on change de nom pour ne pas l'ecraser.
            plt.savefig(nom_fichier+"(%i).png" % numero_fichier,format='png')
            plt.show()
    else:
        con.sendall("---------------\nAttention : Execution incomplete du programme.\n\nSeule l'annalyse sur la sequence entiere a pu etre effectuee.\nLes analyses par fenetre requierent une sequence de longueur minimum 200 nucleotides.\n---------------\n".encode())
        sortie.close()

        

    
def resultat_prot(des,seq,compo,keys,con, plot_dispo=-1): # Permet d'obtenir les tableaux de resultats et les graphiques correspondants de l'annalyse de la sequence proteique. (Fonctionnement tres similaire a "resultat_ADN")
    "Pour fonctionner ce module fait appel a cinq autres modules qui doivent se trouver dans le meme repertoire courant que lui : recuperation_sequence_fasta, lire_fasta, analyse_ADN, analyse_proteine, et creation_seq_aleatoires. Cette procedure permet d'effectuer une etude de sequence proteique. Cette etude consiste en un calcul du nombre d'acide amines hydrophobe presents, du nombre d'acide amines charges presents, et de la charge net de la sequence entriere, et en un calcul de l'hydrophobicite moyenne dans chaque fenetre glissante de neuf acides amines. La procedure cree un a deux fichiers de sortie : un fichier tabule (pouvant etre ouvert avec un editeur de texte ou un tableur comme Excel) et une image des graphiques qu'elle engendre sous certaines conditions. Elle prend en arguments une description et la sequence correspondante au minimum. En troisieme argument elle prend la composition de la sequence (compo=) sous forme de dictionnaire, par defaut cette composition est calculee dans la procedure. De meme en quatrieme argument elle prend la liste des caracteres composants la sequence (keys=) (chacun ecrit entre guillemets), par defaut cette liste est calculee par la procedure. En dernier argument elle prend le boleen plot_dispo qui par defaut vaut True si le poste de tavail dispose de l'installation du module 'matplotlib' et False sinon, si l'utilisateur choisit d'entree plot_dispo=True en argument il doit lui meme s'assurere de cette installation au prealable, si au contraire il rentre plot_dispo=False, les graphiques ne seront pas generes." 
    if compo==-1: 
        compo=an.composition(seq,con)
    if keys==-1: 
        keys=[]
        for key in compo.keys():
            keys.append(key)
    if plot_dispo==-1:
        plot_dispo=plt_dispo
    nom_fichier="Annalyse_seq_prot"+des
    fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
    numero_fichier=0
    while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
        try: 
            sortie=open(nom_fichier+"(%i).py" % numero_fichier,'r') # Test si le fichier "nom_fichier.py" existe.
        except FileNotFoundError: 
            fichier_existe=False
        else:
            sortie.close()
            numero_fichier+=1
            nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier)
    sortie=open(nom_fichier+"(%i).py" % numero_fichier,'a') # Ouverture du fichier resultat.
    nb_aa_hydrophobe,aa_charges,charge=ap.nb_residus_hydrophobes_et_residus_charges_et_chage_net(seq,compo) # Recuperation les resultats de l'etude de la sequence entiere.
    num_fenetre=[]
    sortie.write("\taa hydrophobes\taa charges (%)\tcharge net") # Redaction du tableau de resultat de l'etude sur la sequence entiere (sur cette ligne et les 5 suivantes).
    resultats="\n srquence entiere\t"+str(nb_aa_hydrophobe)+"\t%.3f" % aa_charges +"\t"+str(charge)
    for ele in keys:
        sortie.write("\t"+str(ele))
        resultats+="\t"+str(compo[str(ele)])
    resultats=resultats.replace(".",",")
    sortie.write(resultats)
    if len(seq)>=9: # Dans ce "if" recuperation et traitement des resultats par fenetre glissante de 9 acide amines.
        hydrophobicite=ap.hydrophobicite_moyenne(seq,9,con)
        sortie.write("\n \n \nFenetres\thydrophobicite moyenne\n")
        for i,ele in enumerate(hydrophobicite):
            num_fenetre.append(i+1)
            resultatsfenetres=str(i+1)+"\t%.3f" % hydrophobicite[i] +"\n"
            resultatsfenetres=resultatsfenetres.replace(".",",") # On remplace les points par des virgules pour que les valeurs soient reconnus comme des nombres par Excel
            sortie.write(resultatsfenetres)
        sortie.close()
        if plot_dispo: # Seulement si le module matplotlib est installe sur le poste de traville utilise.
            plt.subplot(212)
            plt.title("Hydrophobicite moyennes de chaque fenetre glissante de 9 acides amines de la sequence")
            plt.grid()
            plt.axhline(0, linestyle=':', color='k')
            plt.plot(num_fenetre,hydrophobicite)
            plt.xlabel("Numero des fenetres glissantes")
            plt.ylabel("hydrophobicite (Echelle de Fauchere et Peliska)")
            if max(hydrophobicite)>0:
                plt.annotate("",xy=(0.5,0), xycoords='data',xytext=(0.5,max(hydrophobicite)), textcoords='data',arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color='r'), )
                plt.text(-max(num_fenetre)/50,max(hydrophobicite)-0.2, "Partie hydrophobe", fontsize=8,color='r',rotation=85)
            if min(hydrophobicite)<0:
                plt.annotate("",xy=(0.5,0), xycoords='data',xytext=(0.5,min(hydrophobicite)), textcoords='data',arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color='b'), )
                plt.text(-max(num_fenetre)/50,0, "Partie hydrophile", fontsize=8,color='b',rotation=85)
            fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
            numero_fichier=0
            while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
                try: 
                    sortie=open(nom_fichier+"(%i).png" % numero_fichier,'r') # Test si le fichier "nom.py" existe.
                except FileNotFoundError: 
                    fichier_existe=False
                else:
                    sortie.close()
                    numero_fichier+=1
                    nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier) # Si le fichier "nom_fichier.png" existe on change de nom pour ne pas l'ecraser.
            plt.savefig(nom_fichier+"(%i).png" % numero_fichier,format='png')
            plt.show()
    else:
        con.sendall("---------------\nAttention : Execution incomplete du programme.\n\nSeule l'analyse sur la sequence entiere a pu etre effectuee.\nLes annalyses par fenetre requierent une sequence de longueur minimum 9 acides amines.\n---------------\n".encode())
        sortie.close()

def resultats_analyse_seq(con, addr): # Permet d'optenir les resultats de l'annalyse d'une sequence ADN ou proteique sous forme de tableaux et de graphiques  
    "Pour fonctionner ce module fait appel a cinq autres modules qui doivent se trouver dans le meme repertoire courant que lui : recuperation_sequence_fasta, lire_fasta, analyse_ADN, analyse_proteine, et creation_seq_aleatoires. Cette procedure permet de realiser une etude de sequence nucleique ou proteique au format fasta, cette etude constiste dans les deux cas en une evalusation de la composition de la sequence puis en une etude plus specifique au type de la sequence (se referer a resultat_prot.__doc__ pour plus de deatils sur l'etude des sequences proteique et a resultat_ADN.__doc__ pour les sequences nucleique). Cette procedure ne prend aucun argument en entree. Elle genere un a deux fichiers de sortie : un fichier tabule (pouvant etre ouvert avec un editeur de texte ou un tableur comme Excel) et une image des graphiques qu'elle cree si l'utilisateur le souhaite et que le module 'matplotlib' est installe sur le poste de travail." 
    reponse="Initialisation" # Condition utile pour commencer l'etude d'une nouvelle fonction.
    type_seq=""
    premiere_analyse=True # variable servant a ne pas refaire l'annalyse d'une sequence deja effectuee. 
    while reponse!="4":
        keys=[]
        valeurs=[]
        if type_seq=="": # Seulement si c'est la premiere annalyse ou que l'utilisateur a demander a en commencer une nouvelle.
            des,seq,type_seq=rs.entree(con,addr)
            print("sortie de entree")
            des=des.replace(",","_") # Ensemble de commande permettant de creer un nom de fichier sans caracteres compromettants.
            des=des.replace(".","")
            des=des.replace(" ","_")
            des=des.replace("/","")
            des=des.replace("\\","")
            des=des.replace("|","_")
            if type_seq=="": # Cette condition mene a l'arret du programme.
                reponse="4"
                continue # Permet de passer au tour de boucle while suivant, or reponse="4" donc le programme s'arrete.
            print("ecriture d'un fichier")
#            try:
#                os.mkdir("Analyse_"+des) # Permet de tester si le dossier '"Analyse_"+des' existe.
#            except FileExistsError:
#                premiere_analyse=False # Si le dossier existe deja alors l'analyse de la sequence entree existe deja, on ne souhaite pas la refaire inutilement.
#                print(" \nL'analyse de cette sequence a deja ete effectuee, vous pouvez \napprofondir cette analyse ou effectuer une annalyse sur une nouvelle sequence. \n")
#            os.chdir("./Analyse_"+des) # Si le dossier existe deja il n'est pas cree et on rentre simplement dedans, sinon il a deja ete creer dans le 'try' et donc on rentre dedans.
            sequence=seq # Permet de garder en memoire la sequence de reference de chaque analyse dans la variable 'seq'.
            description=""
        elif type_seq!="":
            if reponse=="Initialisation":
                if premiere_analyse: # Si une analyse identique a deja ete effectuee on ne la refait pas.
#                    if plt_dispo: # Pour permettre a l'utilisateur de choisir s'il veut creer des graphiques ou non seulement dans le cas ou le module matplotlib est disponible et donc la creation de graphiques possible.
#                        plot_dispo=input(" \nSi vous souhaitez que le programme trace des graphiques en se basant \nsur l'analyse par fenetre (l'analyse sera plus longue), tapez 1 \nsinon, tapez 2 : ")
#                        while plot_dispo!="1" and plot_dispo!="2":
#                            print("\n---------------\nAttention : votre reponse ne correspond a aucune des propositions.\n\nVeuillez reconsiderer votre reponse.\n\nAttention : Relance du programme\n--------------\n")
#                            plot_dispo=input(" \nSi vous souhaitez que le programme trace des graphiques en se basant \nsur l'analyse par fenetre (l'analyse sera plus longue), tapez 1 \nsinon, tapez 2 : ")
#                        if plot_dispo=="1":
#                            plot_dispo=True
#                        else:
#                            plot_dispo=False
#                    else:
#                        plot_dipo=True
                    seq=ap.code3aa1(sequence) # Permet de passer du code d'acide amines 3 lettres au code 1 lettre si besoin (si 'sequence' est nucleotidique ou deja en code 1 lettre rien ne change.)
                    compo=ap.composition(sequence)
                    for key in compo.keys():
                        keys.append(key)
                        valeurs.append(compo[str(key)])
#                    if plot_dispo :
#                        objets = np.arange(len(valeurs))
#                        plt.subplots(figsize=(12,7)) # Permet de choisir la taille de la fenetre surgissante contenants les graphiques.
#                        plt.subplot(231) # Permet de choisir la position du graphique au sein de la fenetre surgissante.
#                        plt.gca().yaxis.grid() # Permet de faire apparaitre une grille horizontale uniquement.(Pour une meilleur lisibilite.)
#                        plt.bar(objets, valeurs, align='center', alpha=0.5,color='b')
#                        plt.xticks(objets, keys) # Pour faire apparaitre les elements composant la sequence sur l'axe des abscisses.
#                        plt.ylabel('Nombre de nucleotides')
#                        plt.title('Composition de la sequence')
                    if type_seq=="prot":
                        #resultat_prot(description,sequence,compo,keys,plot_dispo, con)
                        print("resultat prot")
                    else :
#                        if plot_dispo :
#                            if "N" in compo:
#                                plt.text(-1,-len(seq)/5, "Attention il y a "+str(compo["N"])+" 'N' dans la sequence etudiee\n de longueur : "+str(len(seq))+" nucleotides." , fontsize=10,color='r' , bbox=dict(boxstyle="square,pad=0.3",fc="w",ec="r", lw=1))
#                            else:
#                                plt.text(-1,-len(seq)/5, "La sequence etudiee est composee de "+str(len(seq))+"\nnucleotides." , fontsize=10,color='b', bbox=dict(boxstyle="square,pad=0.3",fc="w",ec="b", lw=1))
                        print("resultat adn")
                        #resultat_ADN(description,sequence,compo,keys,plot_dispo)
            elif reponse=="1":
                reponse="Initialisation" # Permet de repartir dans la condition menant a l'analyse de la sequence.
                type_seq=""
                os.chdir("./..")
                premiere_analyse=True # On va passer a une nouvelle analyse on reinitialise donc la variable premiere_analyse.
                continue # Permet de passer au tour de boucle while suivant, pour retester les conditions sur la variable "reponse".
            elif reponse=="2":
                reponse="Initialisation"
                seq_meme_compo=csa.seq_meme_compo(seq) # Recupere une sequence de meme composition que "seq".
                description="_seq_meme_compo"
                sequence=seq_meme_compo # Ecrase "sequence" mais pas "seq" ce qui permet de garder en memoire la sequence de reference de chaque analyse dans la variable 'seq'.
                premiere_analyse=True # Pour les sequences aleatoire, la sequence change a chaque fois donc l'analyse est toujours nouvelle.
                continue
            elif reponse=="3":
                reponse="Initialisation"
                seq_al=csa.seq_aleatoire(seq,compo) # Recupere une sequence de composition aleatoire de meme type et de meme longueur que "seq".
                description="_seq_aleatoire"
                sequence=seq_al # Ecrase "sequence" mais pas "seq" ce qui permet de garder en memoire la sequence de reference de chaque analyse dans la variable 'seq'
                premiere_analyse=True
                continue
            else :
                con.sendall("\n---------------\nAttention : votre reponse ne correspond a aucune des propositions.\n\nVeuillez reconsiderer votre reponse.\n\nAttention : Relance du programme\n--------------\n \nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n".encode())
                reponse=con.recv(1024).decode()
                continue
            con.sendall((" \nL'analyse de votre sequence a ete effectuee avec succes. \n \nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n ".encode()))
            reponse=con.recv(1024).decode()
        if reponse=="4":
            con.sendall("\n---------------\nArret du programme\n---------------\n".encode())
            con.shutdown(1)
    
