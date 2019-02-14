#!/usr/bin/python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Projet Réseaux 4BIM 
#                                                                  Creation de séquences aleatoires
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


import random as rdm
import time

def composition(seq): # Renvoie la composition d'une chaine de caractere. Fonctionne pour les sequence proteique ou nucleotidique.
    "Cette fonction donne la composition en chaque element d'une sequence donnee en entree sous forme de chaine de caracteres."
    seq=seq.strip()
    dico={}
    for ele in seq:
        if ele in dico: # Si la cle "ele" existe deja on rajoute 1 a sa valeur.
            dico[ele]+=1
        else: # Si la cle "ele" n'existe pas on la cree et on lui associe la valeur 1.
            dico[ele]=1 
    return(dico)

def seq_aleatoire(seq,compo=-1): # Cree une sequence aleatoire de meme longeur et de meme type que seq (nucleotidique ou proteique).
    "Cette fonction permet de cree une sequence aleatoire de meme longeur et de meme type qu'un sequence donnee en premier argument (nucleotidique ou proteique, sous forme de chaine de catacteres),la composition de la sequence peut egalement etre entree en deuxieme argument sous la forme dictionnaire ce qui evite que la fonction la recalcule et accelere ainsi le temps d'execution."
    aleatoire=""
    comp=[]
    if compo==-1:
        dico=composition(seq)
    else:
        dico=compo
    if len(dico.keys())==5 and "A" in dico.keys() and "C" in dico.keys() and "T" in dico.keys() and "G" in dico.keys(): # Pour traiter le cas des "N" présents dans les sequence ADN
        del dico["N"]
    for cle in dico: # Cette boucle permet de recuperer la liste des caracteres constituant la sequence donnee en entree.
        comp.append(cle)
    for ele in seq: # Permet de creer une sequence de meme longueur que "seq".
        aleatoire+=rdm.choice(comp) # Simule un tirage aleatoire avec remise dans comp.
    return (aleatoire)
    
def seq_meme_compo(seq): # Cree une sequence de meme composition et donc de meme longueur que la sequence donnee en argument.
    "Cette fonction permet de cree une sequence de meme composition et donc de meme longueur que la sequence donnee en argument (nucleotidique ou proteique, sous forme de chaine de catacteres)."
    return (''.join(rdm.sample(seq,len(seq)))) # Methode permettant de "melanger" les carartere d'une chaine de caractere preexistante pour en creer une nouvelle.

