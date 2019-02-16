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
    finally: # "Nettoyage" si exception leave
        print("Shutting down")
        for process in multiprocessing.active_children():
            print("Shutting down process %r", process)
            process.terminate()
            process.join()
        socket.close()
    print("END")
