#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Projet Réseaux 4BIM
#                                                             Récupération de sequences fasta
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


import analyse_seq_fasta as asf
import multiprocessing
import socket
import sys

import signal


stopBoolServ = True # Variable globale

#exemple de function pour traiter les arrets par ctrl+C
def signal_handler(signal, frame):
	global stopBoolServ
	stopBoolServ = False
	print ('You pressed Ctrl+C! : stopBoolServ = %s'%str(stopBoolServ))

 
def handle_com(con, addr):
    print("process identity %s" %(addr,))
    try:
        print("connection information %s at %s" %(con, addr))
        while True:
            print("before asf")
            asf.resultats_analyse_seq(con, addr)
            print("after asf")
#            data = con.recv(1024).decode()
#            if data == "":
#                print("Socket closed by client ?")
#                break
#            print("Received data %s" %data)
#            con.sendall(data.encode())
#            print("Sent data %s" %data)
    except:
        print("Problem in request ?")
    finally:
        print("finally : Closed socket")
        con.shutdown(1)
        con.close()
 
 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("OK")
    while stopBoolServ :
        try: # Premiere etape
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.bind(("0.0.0.0",int(sys.argv[1])))
            socket.listen(1)
            print("Listening")
            while True: 
                con, addr = socket.accept()
                print("Got a new connection")
                process = multiprocessing.Process(target=handle_com, args=(con, addr))
                process.daemon = True
                process.start()
                print("process %s" %process)

        except:
            print("Unexpected exception")
        finally: # "Nettoyage" si exception levee
            print("Shutting down")
            for process in multiprocessing.active_children():
                print("Shutting down process %r", process)
                process.terminate()
                process.join()
            socket.close()

    print("Shutting down")
    for process in multiprocessing.active_children():
        print("Shutting down process %r", process)
        process.terminate()
        process.join()
    socket.close()

<<<<<<< HEAD
=======
    except:
        print("Unexpected exception")
    finally: # "Nettoyage" si exception leave
        print("Shutting down")
        for process in multiprocessing.active_children():
            print("Shutting down process %r", process)
            process.terminate()
            process.join()
        socket.close()
>>>>>>> e999d4ec16750e70a9741f4af69bdaaa88d2f6f6
    print("END")
