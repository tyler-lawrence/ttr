# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 12:33:27 2018

@author: jlawr
"""


import socket
import json
import ttr

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    pl = ttr.player()

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    #message = input(" -> ")  # take input
    message = "OK"

    while message.lower().strip() != 'bye':
        server_msg = json.loads(client_socket.recv(1024).decode())  # receive response
        
        #first two items in the list are train cards
        tc1 = server_msg.pop(0)
        tc2 = server_msg.pop(0)
        print("received train cards from deck: %s, %s" % (tc1, tc2))
        pl.store_train_card(tc1)
        pl.store_train_card(tc2)
        print("train card hand:")
        for card, count in pl.train_cards.items(): 
            if count > 0:
                print(card, count)

        #select route cards to keep
        # only route cards in the server_msg list now
        print("\nreceived route cards")
        for i, rc  in enumerate(server_msg):
            print("card %d: %s, %s, %d" % (i+1, rc[0], rc[1],rc[2]))
        
        while True:
            keep = input("enter list of cards to keep (1,2,3), must keep at least 2 : ")
            keep_list= keep.split()
            valid = True
            for k in keep_list:
                if k not in ['1','2','3']:
                    valid = False
            if valid and len(keep_list) >= 2 and len(keep_list) <= 3:
                break

        for i, sm_rc  in enumerate(server_msg): # route card as list, not object
            if str(i+1) in keep_list:
                rc=ttr.route_card(sm_rc[0], sm_rc[1], sm_rc[2]) # convert to object
                pl.store_route_card(rc)
                
        print("\nroute card hand")
        for rc in pl.route_cards:
            print(rc.city1, rc.city2, rc.points, rc.completed)
            
        client_socket.send(json.dumps(keep_list).encode())  # send message
        

        message = input(" -> ")  # again take inp

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
