#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Projet Réseaux 4BIM
#                                                                   Code Serveur 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Imports généraux :
import multiprocessing
import socket
import select
from time import time, ctime
import sys
import signal

#Import de module local :
import analyse_sequence_fasta as asf

# Variable globale :
stopBoolServ = True

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def signal_handler(signal, frame):
    "Fonction qui permet de traiter les arrets par ctrl+C"


    print('\n\nYou pressed Ctrl+C\nSERVER CLOSED\n')
    global stopBoolServ
    stopBoolServ = False
    sys.exit(0)


def handle_com(con, addr):
    """Cette fonction permet de lancer le module d'analyse analyse_sequence_fasta avec le menu principal."""


    print("Process identity %s, %s" %(addr[0],addr[1]))
    try:
        print("Connection information %s at %s, %s\n" %(con, addr[0],addr[1]))
        while True:
            asf.resultats_analyse_seq(con, addr)
    except:
        try:
            con.shutdown(1)
            con.close()
            print("Problem in request ?")
            print("Finally : Closed socket")
        except:
            print("The process %s, %s has been stopped by user"%(addr[0],addr[1]))


class Serveur:
    """Cette fonction gère la connexion d'un serveur. Il reste à l'écoute en attendant la connexion de clients.
    Dès que celle-ci est établi il fait appel à proced. """

    def __init__(self):
        global stopBoolServ 
        stopBoolServ = True
        # Initialisation de la classe """
        self.TAILLE_BLOC=1024 # la taille des blocs 
        # creation de la connection pour le serveur, protocol TCP, domaine internet
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # recuperation du numero de port via la ligne de commande
        sock.bind(("127.0.0.1",int(sys.argv[1])))
        sock.listen(1)
        print("\nListening\n")
        while stopBoolServ:
            con, addr = sock.accept()
            print("Got a new connection")
            self.proced(con,addr)
        sock.shutdown(1)
        sock.close()


    def proced(self,con,addr):
        """Cette fonction permet de gérer les connections multiples. Elle permet ainsi la parallélisation de
        la fonction handle_com()."""

        try:
            process = multiprocessing.Process(target=handle_com, args=(con, addr))
            process.daemon = True
            process.start()
            print("process %s" %process)
        except:
            print("Unexpected exception")
            print("Shutting down")
            for process in multiprocessing.active_children():
                print("Shutting down process %s" %process)
                process.terminate()
                process.join()
	
                

if __name__=="__main__":
	import sys
	if len(sys.argv)<2:
		print("usage : %s <port>" % (sys.argv[0],))
		sys.exit(-1)
	signal.signal(signal.SIGINT, signal_handler)
	Serveur()

