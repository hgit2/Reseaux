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


#creation de la socket puis connexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",int(sys.argv[1])))


while 1:
  print("before data")  
  data = s.recv(1024).decode()
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
 # s.sendall(b"%" %msg.encode())
  print("after sendall")

# fermeture de la connexion
s.close()
print("fin du client TCP")
