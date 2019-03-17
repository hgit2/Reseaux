#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Projet Réseaux 4BIM
#                                                                    Code client
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Imports généraux :
import socket 
import select
import time
import sys
import os


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

try:
    import matplotlib.pyplot as plt # Permet de tester la presence du module matplotlib sur le poste.
except ImportError:
    print("---------------\nAttention : Votre poste de travail n'est pas equipe du module matplotlib,\npar consequent le programme ne pourra pas generer de resultats graphiques\nseuls les tableaux de resultats seront generes.\n---------------")
    plt_dispo=False # (Variable globale) Si le module matplotlib n'est pas insatlle sur le poste la variable plt_dispo prend la valeur False et les graphiques des resultats ne seront pas traces.
else:
    plt.rcdefaults() # Permet de reinitialiser les parametres par defaut de matplotlib au cas ou ils aient ete modifier
    import numpy as np
    plt_dispo=True # (Variable globale) Si le module matplotlib est insatlle sur le poste la variable plt_dispo prend la valeur True.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def creation_repertoire(des,s):
    premiere_analyse=True
    try:
        os.mkdir("Analyse_"+des) # Permet de tester si le dossier '"Analyse_"+des' existe.
    except FileExistsError:
        premiere_analyse=False # Si le dossier existe deja alors l'analyse de la sequence entree existe deja, on ne souhaite pas la refaire inutilement.
        print(" \nL'analyse de cette sequence a deja ete effectuee, vous pouvez \napprofondir cette analyse ou effectuer une annalyse sur une nouvelle sequence. \n")
    os.chdir("./Analyse_"+des) # Si le dossier existe deja il n'est pas cree et on rentre simplement dedans, sinon il a deja ete creer dans le 'try' et donc on rentre dedans.
    premiere_analyse=str(premiere_analyse)
    premiere_analyse=premiere_analyse.encode()
    s.sendall(premiere_analyse)
    s.recv(255).decode()


def creation_fichier(nom_fichier) :
    nom_fichier=nom_fichier.replace("\n","")
    fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
    numero_fichier=0
    while fichier_existe: # Tant que le fichier "nom_fichier.png" existe le nom change.
        try:
            sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Test si le fichier "nom_fichier.py" existe.
        except FileNotFoundError:
            fichier_existe=False
        else:
            sortie.close()
            numero_fichier+=1
            nom_fichier=nom_fichier.replace("(%i)" % (numero_fichier-1),"(%i)" % numero_fichier)  
    return(nom_fichier, numero_fichier)



def analyse_graph(nom_fichier, numero_fichier):
    if plt_dispo: # Pour permettre a l'utilisateur de choisir s'il veut creer des graphiques ou non seulement dans le cas ou le module matplotlib est disponible et donc la creation de graphiques possible.
        plot_dispo=input(" \nSi vous souhaitez que le programme trace des graphiques en se basant \nsur l'analyse par fenetre (l'analyse sera plus longue), tapez 1 \nsinon, tapez 2 : \n\n>> ")
        while plot_dispo!="1" and plot_dispo!="2":
            print("\n---------------\nAttention : votre reponse ne correspond a aucune des propositions.\n\nVeuillez reconsiderer votre reponse.\n\nAttention : Relance du programme\n--------------\n")
            plot_dispo=input(" \nSi vous souhaitez que le programme trace des graphiques en se basant \nsur l'analyse par fenetre (l'analyse sera plus longue), tapez 1 \nsinon, tapez 2 : \n\n>> ")
        if plot_dispo=="1":
            plot_dispo=True
        else:
            plot_dispo=False
    else:
        plot_dispo=False
    if plot_dispo==-1: # Permet une utilisation plus generale pour laquelle l'utilisateur n'aurait pas a choisir s'il souhaite ou non tracer les graphiques.
        plot_dispo=plt_dispo
    if plot_dispo :
        file=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Ouverture du fichier resultat en mode lecture.
        line=file.readline()[:-1].split("\t") #[:-1] pour ne pas prendre le "\n" en fin de ligne.
        if "Analyse_seq_prot" in nom_fichier:
            keys=line[4:]
            line=file.readline()[:-1].split("\t") 
            valeurs=line[4:] # Pour recuperer la liste des elements qui composent la sequence proteique.
        else :
            keys=line[3:]
            line=file.readline()[:-1].split("\t") 
            valeurs=line[3:] # Pour recuperer la liste des elements qui composent la sequence nucleique.
        valeurs=[int(i) for i in valeurs]
        objets = np.arange(len(valeurs))
        plt.subplots(figsize=(12,7)) # Permet de choisir la taille de la fenetre surgissante contenants les graphiques.
        plt.subplot(231) # Permet de choisir la position du graphique au sein de la fenetre surgissante.
        plt.gca().yaxis.grid() # Permet de faire apparaitre une grille horizontale uniquement.(Pour une meilleur lisibilite.)
        plt.bar(objets, valeurs, align='center', alpha=0.5 ,color='b')
        plt.xticks(objets, keys) # Pour faire apparaitre les elements composant la sequence sur l'axe des abscisses.
        plt.ylabel('Nombre de nucleotides')
        plt.title('Composition de la sequence')
        file.close()
    return(plot_dispo)


def analyse_graph_adn(nom_fichier, numero_fichier):
    file=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Ouverture du fichier resultat en mode lecture.
    line=file.readline()[:-1].split("\t")
    compo=line[3:]
    line=file.readline()[:-1].split("\t")
    compo_nb=line[3:]
    compo_nb=[int(i) for i in compo_nb]
    for i in range(len(compo)):
        if compo[i]=="N":
            plt.text(-1,-sum(compo_nb)/5, "Attention il y a "+str(compo_nb[i])+" 'N' dans la sequence etudiee\n de longueur : "+str(sum(compo_nb))+" nucleotides." , fontsize=10,color='r' , bbox=dict(boxstyle="square,pad=0.3",fc="w",ec="r", lw=1))
    else:
        plt.text(-1,-sum(compo_nb)/5, "La sequence etudiee est composee de "+str(sum(compo_nb))+"\nnucleotides." , fontsize=10,color='b', bbox=dict(boxstyle="square,pad=0.3",fc="w",ec="b", lw=1))
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    if "Fenetres" in line : # Si la longueur de la sequence est inferieure a 200 nucleotides, cette partie de l'annalyse n'a pas pu etre effectuee car elle necessite des fenetres glissantes de 200 nucleotides.
        ilot_CpG=False
        plt_rapportCpG=True
        num_fenetre=[]
        rapportCpG=[]
        CGfenetre=[]
        line=file.readline()[:-1].split("\t")
        while line[0] != "":
            num_fenetre.append(int(line[0]))
            rapportCpG.append(float(line[3].replace(",",".")))
            CGfenetre.append(float(line[1].replace(",",".")))
            if line[3]!="NA":
                if line[4]=="Oui":
                    ilot_CpG=True
                    plt.subplot(222) # Ensemble de commande permettant de faire apparaitre les ilots CpG en rouge sur les graphiques.
                    plt.plot([int(line[0])+1],[float(line[3].replace(",","."))],'.r')
                    plt.subplot(224)
                    plt.plot([int(line[0])+1],[float(line[1].replace(",","."))],'.r')
            else:
                plt_rapportCpG=False
            line=file.readline()[:-1].split("\t")
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
    file.close()


def ecriture_adn(s) :
    nom=s.recv(1024).decode()
    nom_fichier, numero_fichier = creation_fichier(nom)
    s.sendall("OK".encode())
    sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a') # Ouverture du fichier resultat.
    message=s.recv(1024).decode()
    if len(message.split('\n'))>1: #message.split('\n')[1] == "Attention : Execution incomplete du programme.":
        print(message)
        s.sendall("OK".encode())
        size=s.recv(1024).decode()
    else :
        size=message
    s.sendall("OK".encode())
    file=s.recv(int(size)).decode()
    sortie.write(file)  
    sortie.close()
    plot_dispo=analyse_graph(nom_fichier, numero_fichier)
    if plot_dispo :
        analyse_graph_adn(nom_fichier, numero_fichier)
    print ("Results are available in "+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())
    return(nom_fichier, numero_fichier)


def analyse_graph_prot(nom_fichier, numero_fichier):
    file=open(nom_fichier+"(%i).txt" % numero_fichier,'r') # Ouverture du fichier resultat en mode lecture.
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    line=file.readline()[:-1].split("\t")
    if "Fenetres" in line : # Dans ce "if" recuperation et traitement des resultats par fenetre glissante de 9 acide amines.
        num_fenetre=[]
        hydrophobicite=[]
        line=file.readline()[:-1].split("\t")
        while line[0] != "":
            num_fenetre.append(int(line[0]))
            hydrophobicite.append(float(line[1].replace(",",".")))
            line=file.readline()[:-1].split("\t")
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



def ecriture_proteine(s) :
    nom=s.recv(1024).decode()
    nom_fichier, numero_fichier = creation_fichier(nom)
    s.sendall("OK".encode())
    sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a') # Ouverture du fichier resultat.
    message=s.recv(1024).decode()
    if len(message.split('\n'))>1: #message.split('\n')[1] == "Attention : Execution incomplete du programme.":
        print(message)
        s.sendall("OK".encode())
        size=s.recv(1024).decode()
    else :
        size=message
    s.sendall("OK".encode())
    file=s.recv(int(size)).decode()
    sortie.write(file)  
    sortie.close()
    plot_dispo=analyse_graph(nom_fichier, numero_fichier)
    if plot_dispo :
        analyse_graph_prot(nom_fichier, numero_fichier)
    print ("Results are available in "+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())
    return(nom_fichier, numero_fichier)



def envoie_fasta(description,seq) :
    "Cette fonction envoie au serveur des données fasta stockées en local."
    if description=="entree":
        description= description.encode()
        s.sendall(description)
        rep = s.recv(2).decode()
    else:
        description= description.encode()
        seq = seq.encode()
        s.sendall(description)
        rep = s.recv(2).decode() # Le serveur a bien recu la description
        taille=str(len(seq))
        s.sendall(taille.encode())
        rep = s.recv(2).decode() # Le serveur a bien recu la description
        s.sendall(seq)


    
def lecture_fasta_loc(adresse) :
    "Cette fonction permet de recuperer une sequence et sa description dans un fichier place dans le repertoire courant grace a son nom donne en argument (entre guillemets, sans oublier l'extension)."
    try:
        sequence=""
        fasta=open(adresse,"r") # Permet d'ouvrir un fichier existant pour lire les informations qu'il contient.
        ligne=fasta.readline() # Affecte a la variable ligne la premiere ligne de "fasta" sous forme de chaine de caratere.
        while ligne[0] != ">": # Permet de recuperer la description de la sequence qui toujours est precedee de ">" au format fasta.
            ligne=fasta.readline()
        description=ligne[1:].strip()
        while ligne != "": # Permet de recuperer la sequence et de s'arreter lorque la lecture a atteint la findu fichier.
            ligne=fasta.readline().strip()
            sequence+=ligne
        fasta.close() # Permet de refermer le fichier "fasta" ouvert au debut de la fonction. 
    except FileNotFoundError : # Cette erreur remonte si le fichier dont l'adresse est donnee en entree n'existe pas dans l'emplacement du module. 
        print("\n----------------\nAttention :\n\nLe fichier est introuvable. Verifiez qu'il n'y a pas de fautes de frappe.\n")
        print("Attention : Relance du programme\n---------------\n")
        description,sequence="entree",""
    return(description,sequence)


#--------------Mise en reseau-----------------#
def Client():
    #creation de la socket puis connexion
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1",int(sys.argv[1])))
    
    print("Pour fermer cette session, veuillez écrire exit()\n")
    # Créer un argument pour l'adresse ip ?
    print("Connection on {}\n".format(sys.argv[1]))
    
    while 1:  
        data = s.recv(1024).decode()
        sdata=data.split("__") # permet de parser data
        msg="" # initialisation du message qui sera envoyé par le client
        
        if sdata[0]=="ERROR":
            # gestion des erreurs
            print(sdata[1])
            msg="OK"
        elif data=="resultat_prot":
            s.sendall("OK".encode())
            print("\nAnalyse en cours...\n")
            nom_fichier, numero_fichier=ecriture_proteine(s)
        elif data=="resultat_adn":
            s.sendall("OK".encode())
            print("\nAnalyse en cours...\n")
            nom_fichier, numero_fichier=ecriture_adn(s)
        elif data.split(":")[0]=="creation dossier":
            des=data.split(":")[1]
            creation_repertoire(des,s)
            continue
        elif data=="nouvelle analyse":
            os.chdir("./..")
            s.sendall("OK".encode())
            continue
        else :
            print(data)
        
        if msg=="OK":
            # Si on rentre dans ce if c'est qu'on a traité une erreur
            s.sendall(msg.encode())
        else:
            msg = input('>> ')
            # Pour arreter le client python proprement
            if msg=="exit()": # si on initialise pas msg avec raw_input : comme on utilise NC et pas telnet sur les machines BIM il faut mettre if msg=="\n" pour que ca fonctionne 
                # mais la comme on initialise raw_input c'est bon puisque raw_input renvoi une chaine vide quand on tape entree
                break
            elif msg=="":
                s.sendall("WARNING : empty message".encode())
            elif "." in msg:
                print("\nTraitement d'une séquence fasta en locale...\n")
                s.sendall(msg.encode())
                file_name = msg
                description,seq = lecture_fasta_loc(file_name)
                envoie_fasta(description,seq)
            else:        
            # envoi puis reception de la reponse
                s.sendall(msg.encode())
    
    # fermeture de la connexion
    s.close()
    print("fin du client TCP")
#-----------------------------------------#
    

if __name__=="__main__":
    if len(sys.argv)<2:
        print("usage : %s <port>" % (sys.argv[0],))
        sys.exit(-1)
    Client()

