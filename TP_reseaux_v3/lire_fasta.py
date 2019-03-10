# -*- coding: utf-8 -*-
#!/usr/bin/python3

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Réseaux 4BIM
#                                                        Lecture de fichier fasta et de fiche fasta en ligne
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import urllib.request
import urllib.error 

def lire_fasta(adresse): # Recupere une sequence dans un fichier au format fasta place dans le meme dossier que ce module grace au nom complet du fichier.
    "Cette fonction permet de recuperer une sequence et sa description dans un fichier place dans le repertoire courant grace a son nom donne en argument (entre guillemets, sans oublier l'extension)."
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
    return(description,sequence)


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
        con.sendall("\n----------------\nAttention : Le lien est introuvable\nVerifiez qu'il n'y a pas de faute de frappe\nou que vous n'avez pas oublie l'extention du fichier.\nSinon verifiez que l'identifiant correspond bien a une sequence du type :{}eique.\nVeuillez modifiez vos entrees en consequence. \nAttention : Relance du programme\n---------------\n".format(type_seq).encode())
        print("message envoye")
        return "error", "error"
    except urllib.error.URLError : # Si la connexion internet ne fonctionne pas.
        print("url error")
        con.sendall("\n----------------\nAttention : Impossible d'acceder a la base de donnees en ligne.\nVerifiez que vous avez bien une connnection internet active sur ce poste.\nAttention : Relance du programme\n---------------\n".encode())
        return "error", "error"
    except UnicodeEncodeError : # Si l'identifiant contient des caracteres speciaux non reconnus (accents, guillemets...). 
        print("unicode error")
        con.sendall("\n----------------\nAttention : L'identifiant entre est incorecte\nVerifiez qu'il n'y a pas de faute de frappe,d'espaces\nou que vous n'avez pas oublie l'extention du fichier\nVeuillez modifiez vos entrees en consequence.\nAttention : Relance du programme\n---------------\n".encode())
        return "error", "error"
    else:
        print("else")
        con.sendall("--------------\nAttention : Il y a eu une erreur\nAttention : Relance du programme\n---------------\n".encode())
        return "error", "error"
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
        description="La sequence n'est pas referencee."
    return(description,sequence)

