# -*- coding: utf-8 -*-
#!/usr/bin/python3

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Réseaux 4BIM
#                                                        Lecture de fichier fasta et de fiche fasta en ligne
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import urllib.request
import urllib.error 


def lire_fasta_web(adresse,type_seq,con): # Recupere une sequence fasta sur internet grace a son identifiant entre guillemets et au type de la sequence ("prot" ou "nucl").
    "Cette fonction permet de recuperer une sequence et sa decription dans une fiche fasta en ligne grace a son identifiant donne en premier argument et au type de sequence donne en deuxieme argument ('prot' ou 'nucl')."
    adresse=adresse.upper()
    if type_seq=="prot":
        url="http://www.uniprot.org/uniprot/"+adresse+".fasta"
    else:
        url="http://www.ebi.ac.uk/ena/data/view/"+adresse+"&display=fasta"
    try:
        u=urllib.request.urlopen(url) # Ouvre la page internet correspondant a l'url determine ci-dessus.
    except urllib.error.HTTPError : # Si le lien internet n'existe pas.
        print("http error")
        con.sendall("ERROR__\n----------------\nAttention : Le lien est introuvable\nVerifiez qu'il n'y a pas de faute de frappe\nou que vous n'avez pas oublie l'extention du fichier.\nSinon verifiez que l'identifiant correspond bien a une sequence du type : {}eique.\nVeuillez modifiez vos entrees en consequence. \nAttention : Relance du programme\n---------------\n".format(type_seq).encode())
        ok=con.recv(1024).decode() # réception de l'accusé réception du client
        print(ok)
        return "error", "error"
    except urllib.error.URLError : # Si la connexion internet ne fonctionne pas.
        print("url error")
        con.sendall("ERROR__\n----------------\nAttention : Impossible d'acceder a la base de donnees en ligne.\nVerifiez que vous avez bien une connnection internet active sur ce poste.\nAttention : Relance du programme\n---------------\n".encode())
        ok=con.recv(1024).decode() # réception de l'accusé réception du client
        print(ok)
        return "error", "error"
    except UnicodeEncodeError : # Si l'identifiant contient des caracteres speciaux non reconnus (accents, guillemets...). 
        print("unicode error")
        con.sendall("ERROR__\n----------------\nAttention : L'identifiant entre est incorecte\nVerifiez qu'il n'y a pas de faute de frappe,d'espaces\nou que vous n'avez pas oublie l'extention du fichier\nVeuillez modifiez vos entrees en consequence.\nAttention : Relance du programme\n---------------\n".encode())
        ok=con.recv(1024).decode() # réception de l'accusé réception du client
        print(ok)
        return "error", "error"
##    else:
##        print("else")
##        con.sendall("--------------\nAttention : Il y a eu une erreur\nAttention : Relance du programme\n---------------\n".encode())
##        con.recv(1024).decode()
##        return "error", "error"
    sequence=""
    ligne=u.readline().strip().decode("utf8") # Enleve les eventuels espaces en debut et fin de chaine de caractere et decode la ligne internet qui est codee en "utf8".
    if ligne != "Entry: %s display type is either not supported or entry is not found." %adresse and ligne!="": 
        while ligne[0] != ">": 
            ligne=u.readline().strip().decode("utf8")             
        description=ligne[1:]
        while ligne != "":
            ligne=u.readline().strip().decode("utf8") 
            sequence=sequence+ligne
        u.close() # Referme la page internet ouverte. 
    else : # La page touvee indique que la sequence demandee n'est pas referencee ou introuvable.
        print("seq introuvable")
        description="La sequence n'est pas referencee."
    return(description,sequence)

