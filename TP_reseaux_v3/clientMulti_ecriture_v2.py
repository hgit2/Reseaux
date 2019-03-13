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
global plot_dispo 
plot_dispo=False # à gérer PLUS TARD
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
   # print("Premier analyse : %s"%premiere_analyse)
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
    #print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))
    print ("Results are available in "+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())



def ecriture_proteine(s) :
    nom=s.recv(1024).decode()
    print("nom:%s"%nom)
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
    #print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))
    print ("Results are available in "+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())



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
        #print("TAILLE BIEN RECU ")
        s.sendall(seq)


    
def lecture_fasta_loc(adresse) :
    "Cette fonction permet de recuperer une sequence et sa description dans un fichier place dans le repertoire courant grace a son nom donne en argument (entre guillemets, sans oublier l'extension)."
    try:
        sequence=""
        fasta=open(adresse,"r") # Permet d'ouvrir un fichier existant pour lire les informations qu'il contient.
        ligne=fasta.readline() # Affecte a la variable ligne la premiere ligne de "fasta" sous forme de chaine de caratere.
        print(ligne)
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
            print("Analyse en cours...\n")
            ecriture_proteine(s)

        elif data=="resultat_adn":
            s.sendall("OK".encode())
            print("Analyse en cours...\n")
            ecriture_adn(s)
            
        elif data.split(":")[0]=="creation dossier":
            des=data.split(":")[1]
            creation_repertoire(des,s)
            continue
        
        elif data=="nouvelle analyse":
            os.chdir("./..")
            s.sendall("OK".encode())
            continue
        
        else :
            #print('if not resultats_prot the variable data is  :  ' ,data) # on affiche la reponse
            print(data)
        
        if msg=="OK":
            # alors on a traité une erreur
            s.sendall(msg.encode())
            print("OK envoye")
        else:
            msg = input('>> ')
        
            # test pour arreter le client python proprement
            if msg=="exit()": # si on initialise pas msg avec raw_input : comme on utilise NC et pas telnet sur les machines BIM il faut mettre if msg=="\n" pour que ca fonctionne 
                # mais la comme on initialise raw_input c'est bon puisque raw_input renvoi une chaine vide quand on tape entree
                break
            elif msg=="":
                s.sendall("WARNING : empty message".encode())    

            elif "." in msg:
                print("Traitement d'une séquence fasta en locale...")
                s.sendall(msg.encode())
                file_name = msg
                description,seq = lecture_fasta_loc(file_name)
                envoie_fasta(description,seq)
            else:        
            # envoi puis reception de la reponse
                s.sendall(msg.encode())
            print("after sendall")
    # fermeture de la connexion
    s.close()
    print("fin du client TCP")




if __name__=="__main__":
    if len(sys.argv)<2:
        print("usage : %s <port>" % (sys.argv[0],))
        sys.exit(-1)
    Client()

    


