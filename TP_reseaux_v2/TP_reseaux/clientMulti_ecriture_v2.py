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

def creation_repertoire(des):
    try:
        os.mkdir("Analyse_"+des) # Permet de tester si le dossier '"Analyse_"+des' existe.
    except FileExistsError:
        premiere_analyse=False # Si le dossier existe deja alors l'analyse de la sequence entree existe deja, on ne souhaite pas la refaire inutilement.
        print(" \nL'analyse de cette sequence a deja ete effectuee, vous pouvez \napprofondir cette analyse ou effectuer une annalyse sur une nouvelle sequence. \n")
    os.chdir("./Analyse_"+des) # Si le dossier existe deja il n'est pas cree et on rentre simplement dedans, sinon il a deja ete creer dans le 'try' et donc on rentre dedans.


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

    size=s.recv(1024).decode()
    s.sendall("OK".encode())
    file=s.recv(int(size)).decode()
    sortie.write(file)  
    sortie.close()
    #print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))
    print ("Results are available in"+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())

def ecriture_proteine(s) :
    nom=s.recv(1024).decode()
    print("nom:%s"%nom)
    nom_fichier, numero_fichier = creation_fichier(nom)
    s.sendall("OK".encode())
    
    sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a') # Ouverture du fichier resultat.
    print("creation du fichier")
    size=s.recv(1024).decode()
    print("size=%s"%size)
    s.sendall("OK".encode())
    print("Ok envoye au serveur")
    file=s.recv(int(size)).decode()
    sortie.write(file)  
    sortie.close()
    #print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))
    print ("Results are available in"+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())
    

def seq_mm_compo(s) :
    print('\n')
    nom_fichier=s.recv(1024).decode()
    nom_fichier, numero_fichier = creation_fichier(nom_fichier)
    s.sendall("OK".encode())
    sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a') # Ouverture du fichier resultat.
    size=s.recv(1024).decode()
    s.sendall("OK".encode())
    file=s.recv(int(size)).decode()
    sortie.write(file)  
    sortie.close()
    #print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))
    print ("Results are available in : "+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())

def seq_aleatoire(s) :    
    print('\n')
    nom_fichier=s.recv(1024).decode()
    nom_fichier, numero_fichier = creation_fichier(nom_fichier)
    s.sendall("OK".encode())
    sortie=open(nom_fichier+"(%i).txt" % numero_fichier,'a') # Ouverture du fichier resultat.
    size=s.recv(1024).decode()
    s.sendall("OK".encode())
    file=s.recv(int(size)).decode()
    sortie.write(file)  
    sortie.close()
    print ("Results are available in : "+nom_fichier+"(%i).txt"% numero_fichier)
    print(s.recv(1024).decode())



#creation de la socket puis connexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",int(sys.argv[1])))

# Créer un argument pour l'adresse ip ?
print("Connection on {}".format(sys.argv[1]))

while 1:  
    data = s.recv(1024).decode()
    if data=="resultat_prot":
        s.sendall("OK".encode())
        print("Analyse en cours...\n")
        ecriture_proteine(s)

    elif data=="resultat_adn":
        s.sendall("OK".encode())
        print("Analyse en cours...\n")
        ecriture_adn(s)    
        
    elif data.split(":")[0]=="creation dossier":
        des=data.split(":")[1]
        creation_repertoire(des)
        s.sendall("OK".encode())
        continue

    elif data=="seq_mm_compo":
        s.sendall("OK".encode())
        print("Analyse en cours...\n")
        seq_mm_compo(s)

    elif data=="seq_aleatoire":
        s.sendall("OK".encode())
        print("Analyse en cours...\n")
        seq_aleatoire(s)


    elif data=="nouvelle analyse":
        os.chdir("./..")
        s.sendall("OK".encode())
        continue
    
    else :
        #print('if not resultats_prot the variable data is  :  ' ,data) # on affiche la reponse
        print(data)
        
    msg = input('>> ')
    
    # test pour arreter le client python proprement
    if msg=="exit()": # si on initialise pas msg avec raw_input : comme on utilise NC et pas telnet sur les machines BIM il faut mettre if msg=="\n" pour que ca fonctionne 
        # mais la comme on initialise raw_input c'est bon puisque raw_input renvoi une chaine vide quand on tape entree
        break
    elif msg=="":
        s.sendall("WARNING : empty message".encode())    
        
    else:        
    # envoi puis reception de la reponse
        s.sendall(msg.encode())
    print("after sendall")

# fermeture de la connexion
s.close()
print("fin du client TCP")

if __name__=="__main__":
    creation_fichier("Titoun_et_Lou")


