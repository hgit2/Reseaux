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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
global plot_dispo 
plot_dispo=False # à gérer PLUS TARD
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



def creation_fichier(nom_fichier) :
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
    print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))


#---ATTENTION ce n'est pas au client de faire print de ca normalement !!!!!!!!---#
    print("\nL'analyse de votre sequence a ete effectuee avec succes. \n \nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n ")


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
    print ("Results are available in {0}({1})".format(nom_fichier, numero_fichier))

#---ATTENTION ce n'est pas au client de faire print de ca normalement !!!!!!!!---#
    print("\nL'analyse de votre sequence a ete effectuee avec succes. \n \nPour relancer le programme sur une nouvelle sequence tapez 1\nPour faire la meme etude pour une sequence de meme composition tapez 2,\nPour faire la meme etude sur une sequence aleatoire tapez 3,\nPour arreter le programme tapez 4 :\n ")

    


#creation de la socket puis connexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",int(sys.argv[1])))

# Créer un argument pour l'adresse ip ?
print("Connection on {}".format(sys.argv[1]))

while 1:  
    data = s.recv(1024).decode()
    if data=="resultat_prot":
        print("Analyse en cours...\n")
        ecriture_proteine(s)

    elif data=="resultat_adn":
        print("Analyse en cours...\n")
        ecriture_adn(s)

            
    else :
        print('if not resultats_prot the variable data is  :  ' ,data) # on affiche la reponse
        
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



