# -*- coding: utf-8 -*-
#!/usr/bin/python3

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python L3 BIM 2017
#                                                            Recuperation de la séquence de l’utilisateur
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import lire_fasta as lf
import urllib.request

def entree(): # Cette fonction recupere une sequence proteique ou nucleique au format fasta dans un fichier situe dans le meme dossier que ce module ou sur internet. 
    "Cette fonction fait appel au module lire_fasta qui doit etre place dans le meme repertoire courant que ce module (recuperation_sequence_fasta), elle permet une interaction avec l'utilisateur qui peut choisir quel type de sequence il souhaite recupere. Finalement cette fonction permet de recuperer une sequence au format fasta et sa description."
    print(" \nSi vous souhaitez etudier une sequence proteique tapez 1.")
    print("Si vous souhaitez etudier une sequence nucleique tapez 2.")
    print("ADRESSEEEE")
    print("Pour arreter le programme tapez 4.") 
    type_seq=input("Tapez ici votre choix puis appuyez sur 'entree' : ")
    while type_seq!="1" and type_seq!="2" and type_seq!="4":
        print("\n----------------\nAttention : Votre choix ne correspond a aucune des options proposees. \n")
        print("Attention : Relance du programme\n---------------\n")
        print(" \nSi vous souhaitez etudier une sequence proteique tapez 1.")
        print("Si vous souhaitez etudier une sequence nucleique tapez 2.")
        print("Pour arreter le programme tapez 4.")   
        type_seq=input("Tapez ici votre choix puis appuyez sur 'entree' : ")
    while type_seq=="1" or type_seq=="2":
        print(" \nSi votre sequence se trouve dans un fichier fasta tapez son nom avec extention, sans guillemet.")
        print("Si votre sequence se trouve dans une fiche fasta en ligne tapez son identifiant sans guillemet.")
        print("Sinon tapez 3.")
        adresse=input("Tapez ici votre choix puis appuyez sur 'entree' : ")
        print("ADRESSE",adresse)
        if adresse=="3" :
            print("\n----------------\nAttention : Ce programme est inadapte a votre etude.\n\n")
            print("Ce programme permet d'etudier uniquement des sequences proteiques ou nucleiques\nau format fasta.\n")
            print("Attention : Relance du programme\n---------------\n")
            print(" \nSi vous souhaitez etudier une sequence proteique tapez 1.")
            print("Si vous souhaitez etudier une sequence nucleique tapez 2.")
            print("Pour arreter le programme tapez 4.")
            type_seq=input("Tapez ici votre choix puis appuyez sur 'entree' : ")
            while type_seq!="1" and type_seq!="2" and type_seq!="4":
                print("\n----------------\nAttention : Votre choix ne correspond a aucune des options proposees. \n")
                print("Attention : Relance du programme\n---------------\n")
                print(" \nSi vous souhaitez etudier une sequence proteique tapez 1.")
                print("Si vous souhaitez etudier une sequence nucleique tapez 2.")
                print("Pour arreter le programme tapez 4.")
                type_seq=input("Tapez ici votre choix puis appuyez sur 'entree' : ")
            continue # Permet de passer au tour de boucle while suivant.
        if type_seq=="1":
            type_seq="prot"
        elif type_seq=="2" : # type_seq=="2"
            type_seq="nucl"
        if "." in adresse: # On identifie adresse comme etant un nom de fichier
            try:
                description,sequence=lf.lire_fasta(adresse)
            except FileNotFoundError : # Cette erreur remonte si le fichier dont l'adresse est donnee en entree n'existe pas dans l'emplacement du module. 
                print("\n----------------\nAttention :\n\nLe fichier est introuvable verifiez qu'il n'y a pas de fautes de frappe.\n")
                print("Attention : Relance du programme\n---------------\n")
                description,sequence,type_seq=entree() # Permet de redemander les entree a l'utilisateur.
        else : # Si adresse ne contient pas de "." c'est qu'il s'agit d'un identifiant et non d'un nom de fichier
            try:
                description,sequence=lf.lire_fasta_web(adresse,type_seq)
            except urllib.error.HTTPError : # Si le lien internet n'existe pas.
                print("\n----------------\nAttention : Le lien est introuvable\n")
                print("Verifiez qu'il n'y a pas de faute de frappe\nou que vous n'avez pas oublie l'extention du fichier.")
                print("Sinon verifiez que l'identifiant correspond bien a une sequence du type : "+ type_seq +"eique.")
                print("Veuillez modifiez vos entrees en consequence. \n")
                print("Attention : Relance du programme\n---------------\n")
                description,sequence,type_seq=entree() 
            except urllib.error.URLError : # Si la connexion internet ne fonctionne pas.
                print("\n----------------\nAttention : Impossible d'acceder a la base de donnees en ligne.\n")
                print("Verifiez que vous avez bien une connnection internet active sur ce poste.\n")
                print("Attention : Relance du programme\n---------------\n")
                description,sequence,type_seq=entree()
            except UnicodeEncodeError : # Si l'identifiant contient des caracteres speciaux non reconnus (accents, guillemets...). 
                print("\n----------------\nAttention : L'identifiant entre est incorecte\n")
                print("Verifiez qu'il n'y a pas de faute de frappe,d'espaces\nou que vous n'avez pas oublie l'extention du fichier")
                print("Veuillez modifiez vos entrees en consequence.")
                print("Attention : Relance du programme\n---------------\n")
                description,sequence,type_seq=entree()
            else:
                if description=="La sequence n'est pas referencee.": # Le lien internet a mene a une page informant que la sequence demandee n'est pas referencee.
                    print("\n----------------\nAttention : La sequence n'est pas referencee.\n")
                    print("Verifiez qu'il n'y a pas de faute de frappe dans le nom de la sequence.")
                    print("Sinon verifiez que l'identifiant correspond bien a une sequence du type : "+ type_seq + "eique.")
                    print("Veuillez modifiez vos entrees en consequence. \n")
                    print("Attention : Relance du programme\n---------------\n")
                    description,sequence,type_seq=entree()
        return(description,sequence,type_seq)
    print("\n---------------\nArret du programme\n---------------\n")
    return("","","") # Evite la remontee d'une erreur pour non attribution de variable.
        

#Main:

if __name__=="__main__":
    print(" -> GSELL Louise")
    print(" -> Projet L3 BIM 2017, Module : Recuperation de la sequence de l'utilisateur")
    print("\n")

    # Pour tester la fonction "entree" :
    
    des,seq,type_seq=entree()
    print(des)
    print("\n"+seq)
    
