#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Projet Réseaux 4BIM
#                                                             Récupération de sequences fasta
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


import lire_fasta as lf
import urllib.request


def entree(con, addr): # Cette fonction recupere une sequence proteique ou nucleique au format fasta dans un fichier situe dans le meme dossier que ce module ou sur internet. 
    "Cette fonction fait appel au module lire_fasta qui doit etre place dans le meme repertoire courant que ce module (recuperation_sequence_fasta), elle permet une interaction avec l'utilisateur qui peut choisir quel type de sequence il souhaite recupere. Finalement cette fonction permet de recuperer une sequence au format fasta et sa description."
    con.sendall(" \nSi vous souhaitez etudier une sequence proteique tapez 1.\nSi vous souhaitez etudier une sequence nucleique tapez 2.\nPour arreter le programme tapez 4.\nTapez ici votre choix puis appuyez sur 'entree' :\n".encode())
    type_seq=con.recv(1024).decode()
    while type_seq!="1" and type_seq!="2" and type_seq!="4":
        con.sendall("\n----------------\nAttention : Votre choix ne correspond a aucune des options proposees. \nAttention : Relance du programme\n---------------\n\nSi vous souhaitez etudier une sequence proteique tapez 1.\nSi vous souhaitez etudier une sequence nucleique tapez 2.\nPour arreter le programme tapez 4.\nTapez ici votre choix puis appuyez sur 'entree' :\n".encode())
        type_seq=con.recv(1024).decode()
    while type_seq=="1" or type_seq=="2":
        con.sendall(" \nSi votre sequence se trouve dans un fichier fasta tapez son nom avec extention, sans guillemet.\nSi votre sequence se trouve dans une fiche fasta en ligne tapez son identifiant sans guillemet.\nSinon tapez 3.\nTapez ici votre choix puis appuyez sur 'entree' :\n".encode())
        adresse=con.recv(1024).decode()
        if adresse=="3" :
            con.sendall("\n----------------\nAttention : Ce programme est inadapte a votre etude.\n\nCe programme permet d'etudier uniquement des sequences proteiques ou nucleiques\nau format fasta.\nAttention : Relance du programme\n---------------\n\nSi vous souhaitez etudier une sequence proteique tapez 1.\nSi vous souhaitez etudier une sequence nucleique tapez 2\nPour arreter le programme tapez 4.\nTapez ici votre choix puis appuyez sur 'entree' : \n".encode())
            type_seq=con.recv(1024).decode()
            while type_seq!="1" and type_seq!="2" and type_seq!="4":
                con.sendall("\n----------------\nAttention : Votre choix ne correspond a aucune des options proposees. \nAttention : Relance du programme\n---------------\n\nSi vous souhaitez etudier une sequence proteique tapez 1.\nSi vous souhaitez etudier une sequence nucleique tapez 2.\nPour arreter le programme tapez 4.\nTapez ici votre choix puis appuyez sur 'entree' : \n".encode())
                type_seq=con.recv(1024).decode()
            continue # Permet de passer au tour de boucle while suivant.
        if type_seq=="1":
            type_seq="prot"
        elif type_seq=="2" : # type_seq=="2"
            type_seq="nucl"
        if "." in adresse: # On identifie adresse comme etant un nom de fichier
            description = con.recv(1024).decode() # Reception du nom du fichier 
            con.sendall("OK".encode())
            if description!="entree":
                size=con.recv(1024).decode()
                con.sendall("OK".encode())
                sequence = con.recv(int(size)).decode()
            else:
                description,sequence,type_seq=entree(con, addr)
        else : # Si adresse ne contient pas de "." c'est qu'il s'agit d'un identifiant et non d'un nom de fichier
            description,sequence=lf.lire_fasta_web(adresse,type_seq,con)
            if description=="La sequence n'est pas referencee.": # Le lien internet a mene a une page informant que la sequence demandee n'est pas referencee.
                con.sendall("ERROR__\n----------------\nAttention : La sequence n'est pas referencee.\nVerifiez qu'il n'y a pas de faute de frappe dans le nom de la sequence.\nSinon verifiez que l'identifiant correspond bien a une sequence du type : {}eique.\nVeuillez modifiez vos entrees en consequence. \nAttention : Relance du programme\n---------------\n".format(type_seq).encode())
                con.recv(1024).decode() # réception de l'accusé réception du client
                description,sequence,type_seq=entree(con, addr)
            if description=="error": # si il y a eu des erreurs dans lire_fasta_web
                description,sequence,type_seq=entree(con, addr)
        return(description,sequence,type_seq)
    con.sendall("\n---------------\nArret du programme\nVous etes deconnecte du serveur\n---------------\n".encode())
    con.shutdown(1)
    con.close()
    return("","","") # Evite la remontee d'une erreur pour non attribution de variable.

