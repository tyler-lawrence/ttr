# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 12:30:45 2018

@author: jlawr
"""


import socket
import random
import ttr
import json


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    tc = ttr.train_card()
    
    # when test is true simulate network communications by accepting client responses
    # from the local console
    test = True

    while True:
        response = input("enter number of players: ")
        try:
            number_of_players = int(response)
            assert number_of_players in range(2,6), "number of players must be 2 to 5"
            break
        except ValueError as e:
            print(e)
        except AssertionError as e:
            print(e)
            
    players = []
    for i in range(number_of_players):
        players.append(ttr.player())
    connection_list = []
    
    
    if not test:
        server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    if not test:
        server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    if not test:
        server_socket.listen(number_of_players)
    
    for player in range (number_of_players):
        print("waiting for player %d to connect" % player)
        if not test:
            conn, address = server_socket.accept()  # accept new connection
            connection_list.append(conn)
            print("Connection from: " + str(address))

    print("All players are connected, ready to start game")

    # start the game by dealing 2 train cards and three route cards
    for i in range(number_of_players):
        initial_cards = []
        route_card_option = []
        
        #deal train cards
        for j in range(2):
            card = tc.get_train_card_from_deck()
            initial_cards.append(card)
            players[i].store_train_card(card)
        #deal route cards
        for j in range(3):
            card = ttr.get_route_card()
            route_card_option.append(card)
            initial_cards.append([card.city1, card.city2, card.points]) 
            # had to break down card into list, json can't handle user defined ojbject

        if not test:
            connection_list[i].send(json.dumps(initial_cards).encode())  # send data to the client

            keep = connection_list[i].recv(1024).decode() # get OK response from client
        else:
            keep = input(json.dumps(initial_cards))
        #print("from player %d : %s" % (i, keep))

        if not keep:
            # if data is not received break
            break

        # TODO: client response should be validated
        
        # keep track of players route card selections
        for j, rc in enumerate(route_card_option):
            if str(j) in keep.split():
                players[i].store_route_card(rc)
            else:
                ttr.route_card_list.append(rc)
                # TODO: client programs should not have access to route card list
                # should be private to server
                
    # randomly pick first player to start the game
    player = random.randint(0, number_of_players - 1)
    last_play_of_game = False
    last_player = 0

    # main loop to transmit history and accept player moves
    while True:
        # TODO: send transaction history to client
        
        while True:
            if not test:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                connection_list[player].send(data.encode())  # send data to the client
                play = connection_list[player].recv(1024).decode()
                if not data:
                    # if data is not received break
                    break
                #print("from connected user: %d" % (player))
                #print(" : " + str(data))
            else:
                print("********************")
                print("player %d " % player)
                print(players[player].train_cards)
                print(tc.get_face_up_pile())
                print("")
                play = input('enter play -> ')
            play = play.split()

            # pd - pick from deck
            # pfu - pick from face up pile
            # rc - pick route cards
            # bt - buy track
            if play[0] in {"pd", "pfu", "rc", "bt"} :
                break
            else:
                print("valid plays are : pd, pfu, rc, bt")
        
        #####################################################################
        # pick from deck
        #####################################################################
        if play[0] == "pd":
            card = tc.get_train_card_from_deck()
            players[player].store_train_card(card)
            print(card)
            
            #player gets to pick another card from either deck
            while True:
                if not test:
                    # receive data stream. it won't accept data packet greater than 1024 bytes
                    connection_list[player].send(data.encode())  # send data to the client
                    play = connection_list[player].recv(1024).decode()
                    if not data:
                        # if data is not received break
                        break
                    #print("from connected user: %d" % (player))
                    #print(" : " + str(data))
                else:
                    play = input('pick from deck or face up pile -> ')
                play = play.split()

                if play[0] in  ["pd", "pfu"] :
                    if play[0] == "pd" :
                        break
                    # play is pfu, can't pick wild now
                    elif play[1] != "wild":
                        break
                    else :
                        print("can't pick wild card as second choice")
                else:
                    print("valid plays are : pd, pfu")
            if play[0] == "pd" :
                card = tc.get_train_card_from_deck()
                players[player].store_train_card(card)
                print(card)
            else:
                #player chose to pick from face up pile
                if play[1] in tc.get_face_up_pile():
                    players[player].store_train_card(tc.get_train_card_from_face_up_pile(play[1]))
                else:
                    print("%s is not in the face up pile, stop trying to cheat!" % play[1])
        #####################################################################
        # pick from face up pile
        #####################################################################
        elif play[0] == "pfu":
            pass

        #####################################################################
        # pick route cards
        #####################################################################
        elif play[0] == "rc":
            rc_options = [] # = [ttr.get_route_card()]*3
            for i in range(3):
                card = ttr.get_route_card()
                rc_options.append([card.city1, card.city2, card.points])
                print(i+1,": ",rc_options[i])
            #while True:
            if not test:
                    # receive data stream. it won't accept data packet greater than 1024 bytes
                connection_list[player].send(data.encode())  # send data to the client
                play = connection_list[player].recv(1024).decode()
                if not data:
                # if data is not received break
                    break
              #print("from connected user: %d" % (player))
              #print(" : " + str(data))
            else:
              while True:
                play = input('type the integers of the route cards you wish to keep.'
                             'you must keep at least one. ex: [1 2 3] if you want to keep all: ')
                play = play.split()
                play = [int(i) for i in play]
                
                if len(play) !=0:
                  break
                
            rc_keepers = [] #initialize list to store route cards a player chose to keep
            for i in play[::-1]:
                k = rc_options.pop(i-1)
                rc_keepers.append(k)
                
            #############################
            #############################
            # not sure how to store cards in a player's hand. should it be as a list of the attributes
            # or the actual return of ttr.get_route_card() 
            #############################
            #############################
                
                
            for i in rc_keepers: 
                players[player].store_route_card(i) #store cards in player's hand
                  

        #####################################################################
        # buy track
        #####################################################################
        else:
            pass

        if last_play_of_game and player == last_player:
            # TODO: report winner, final score
            break
        
        if players[player].get_train_count() <= 2:
            last_play_of_game = True
            last_player = player
            
        if player < number_of_players - 1 :
            player += 1;
        else:
            player = 0;
         
    if not test:
        for player in range(number_of_players):
            connection_list[player].close()  # close the connection


if __name__ == '__main__':
    server_program()
