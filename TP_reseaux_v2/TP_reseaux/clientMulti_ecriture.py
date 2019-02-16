#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Projet Réseaux 4BIM
#                                                             Récupération de sequences fasta
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


import socket 
import select
import time
import sys

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
global plot_dispo 
plot_dispo=False # à gérer PLUS TARD
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




#creation de la socket puis connexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",int(sys.argv[1])))


while 1:
    print("before data")  
    
    data = s.recv(1024).decode()
    
    if data=="resultat_prot":
        print("ecriture!")
        des=s.recv(1024).decode()
        print(des)
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
        sortie.write("\taa hydrophobes\taa charges (%)\tcharge net") # Redaction du tableau de resultat de l'etude sur la sequence entiere (sur cette ligne et les 5 suivantes).
        keys=s.recv(1024).decode()
        for ele in keys:
            sortie.write("\t"+str(ele))
        
    print(data) # on affiche la reponse
    
    msg = input('>> ')
    
    # test pour arreter le client python proprement
    if msg=="exit()": # si on initialise pas msg avec raw_input : comme on utilise NC et pas telnet sur les machines BIM il faut mettre if msg=="\n" pour que ca fonctionne 
        # mais la comme on initialise raw_input c'est bon puisque raw_input renvoi une chaine vide quand on tape entree
        break
    elif msg=="":
        s.send("WARNING : empty message".encode())    
        
    # envoi puis reception de la reponse
    s.sendall(msg.encode())
    print("after sendall")

# fermeture de la connexion
s.close()
print("fin du client TCP")
