# -*- coding: utf-8 -*-
#!/usr/bin/python3

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Python L3 BIM 2017
#                                                        Lecture de fichier fasta et de fiche fasta en ligne
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import urllib.request

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


def lire_fasta_web(adresse,type_seq): # Recupere une sequence fasta sur internet grace a son identifiant entre guillemets et au type de la sequence ("prot" ou "nucl").
    "Cette fonction permet de recuperer une sequence et sa decription dans une fiche fasta en ligne grace a son identifiant donne en premier argument et au type de sequence donne en deuxieme argument ('prot' ou 'nucl')."
    adresse=adresse.upper()
    if type_seq=="prot":
        url="http://www.uniprot.org/uniprot/"+adresse+".fasta"
    else:
        url="http://www.ebi.ac.uk/ena/data/view/"+adresse+"&display=fasta"
    u=urllib.request.urlopen(url) # Ouvre la page internet correspondant a l'url determine ci-dessus.
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

#Main:

if __name__=="__main__":
    print(" -> GSELL Louise")
    print(" -> Projet L3 BIM 2017, Module : Lecture de fichier fasta et de fiche fasta en ligne")
    print("\n")
    print(" -> exemples d'applications des fonctions de ce module\n")

    # Pour tester la fonction "lire_fasta" :
    
    fichier_existe=True # Variable permettant de verifier que le fichier qu'on va creer n'en ecrase pas un preexistant.
    nom="test"
    while fichier_existe: # Tant que le fichier nom.py existe le nom change.
        try: # Test si le fichier "nom.py" existe.
            fichier=open(nom+".py","r") 
        except FileNotFoundError :
            fichier_existe=False
        else: # Si il existe on change de nom pour ne pas l'ecraser.
            nom+="bis"
    fichier=open(nom+".py","w") # Pour ecrire un fichier permettant de tester la fonction "lire_fasta".
    fichier.write("> Sequence test pour lire fasta\nTEST_RUSSI")
    fichier.close()
    des,seq=lire_fasta(nom+".py")
    print(des+"\n"+seq)
    print("\n")

    # Pour tester la fonction "lire_fasta_web" :
    
    try : # Pour tester si la connexion internet est operationnelle.
        des,seq=lire_fasta_web("P69464","prot") 
    except urllib.error.URLError : # Si la connexion internet ne fonctionne pas.
        print("\n----------------\nAttention : Impossible d'acceder a la base de donnees en ligne.\n")
        print("Verifiez que vous avez bien une connnection internet active sur ce poste.\n")
        print("Attention : Le test de lire_fasta_web n'a pas pu etre mene a bien.\n---------------\n")
        des,seq,type_seq="","",""
    print(des+"\n"+seq)
