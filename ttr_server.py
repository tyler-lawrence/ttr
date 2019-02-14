# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 12:30:45 2018

@author: jlawr
"""


import socket
import random
import ttr
import jsonpickle


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    tc = ttr.train_card()
    rcd = ttr.route_card_deck()
    players = []
    connection_list = []

    # when test is true simulate network communications by accepting client responses
    # from the local console
    test = True

    def pick_route_cards(player, min_cards_to_keep):
        #create list of 3 route cards
        route_card_option = [ rcd.get_route_card() for i in range(3)]

        if not test:
            connection_list[player.index].send(jsonpickle.dumps(route_card_option).encode())  # send data to the client
            keep = connection_list[player.index].recv(1024).decode() # get OK response from client
        else:
            #keep = input(jsonpickle.dumps(route_card_option))
            for rc in route_card_option:
                print(rc)
            while True:
                try:
                    keep = input('type the integers of the route cards you wish to keep.'
                                 'you must keep at least '  + str(min_cards_to_keep) + '. ex: [1 2 3] if you want to keep all: ')
                    keep = set(keep.split())
                    keep_i = [int(k) for k in keep]
                    if len(keep) < min_cards_to_keep :
                        raise Exception("you must keep at least " + str(min_cards_to_keep) + " cards")
                    for i in keep_i:
                        if i not in range(1,4):
                            raise Exception("indexes must be 1, 2 or 3")
                    break
                except ValueError as e:
                    print(e)
                except Exception as e:
                    print (e)
                    
        # keep track of players route card selections
        for j, rc in enumerate(route_card_option):
            if j + 1 in keep_i:
                player.store_route_card(rc)
            else:
                rcd.discard(rc)

    def pick_from_deck(player):
        card = tc.get_train_card_from_deck()
        player.store_train_card(card)
        print(card)
    
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
            
    for i in range(number_of_players):
        players.append(ttr.player(i))
    
    
    if not test:
        server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
        server_socket.listen(number_of_players)
    
    for player in range (number_of_players):
        print("waiting for player %d to connect" % player)
        if not test:
            conn, address = server_socket.accept()  # accept new connection
            connection_list.append(conn)
            print("Connection from: " + str(address))

    print("All players are connected, ready to start game\n")

    # start the game by dealing 2 train cards and three route cards
    for i in range(number_of_players):
        print("player %d" %i)
        #deal train cards
        for j in range(2):
            card = tc.get_train_card_from_deck()
            players[i].store_train_card(card)
            print(card)
        #deal route cards
        pick_route_cards(players[i], min_cards_to_keep = 2)

    # randomly pick first player to start the game
    player = random.randint(0, number_of_players - 1)
    last_play_of_game = False
    last_player = 0

    # main loop to transmit history and accept player moves
    while True:
        # TODO: send transaction history to client
        
        if not test:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = "enter play ->"
            connection_list[player].send(data.encode())  # send data to the client
            play = connection_list[player].recv(1024).decode()
            if not play:
                # if data is not received break
                break
            #print("from connected user: %d" % (player))
            #print(" : " + str(data))
        else:
            print("********************")
            print("player %d " % player)
            print("points %d " % players[player].points)
            print(players[player].train_cards)
            print(tc.get_face_up_pile())
            print("")
            play = input('enter play -> ')
        play = play.split()

        # loop until a valid transaction is completed
        while True:
            try:
                # pd - pick from deck
                # pfu - pick from face up pile
                # rc - pick route cards
                # bt - buy track
                if play[0] not in {"pd", "pfu", "rc", "bt"} :
                    raise Exception("valid plays are : pd, pfu, rc, bt")
                #####################################################################
                # pick from deck
                #####################################################################
                if play[0] == "pd":
                    pick_from_deck(players[player])
                    
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
                        pick_from_deck(players[player])
                        break
                    else:
                        #player chose to pick from face up pile
                        if play[1] in tc.get_face_up_pile():
                            players[player].store_train_card(tc.get_train_card_from_face_up_pile(play[1]))
                        else:
                            print("%s is not in the face up pile, stop trying to cheat!" % play[1])
                        break
                #####################################################################
                # pick from face up pile
                #####################################################################
                elif play[0] == "pfu":
                    # play[1] should contain a color of a card in the face up pile
                    try:
                        # if play[1] not in tc.get_face_up_pile():
                            # raise Exception(play[1] + " is not in face up pile")
                        players[player].store_train_card(tc.get_train_card_from_face_up_pile(play[1]))
                        if play[1] == 'wild' :
                            # first pick was wild, no second pick
                            break
                        print(players[player].train_cards)
                        print(tc.get_face_up_pile())
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
                            pick_from_deck(players[player])
                        else:
                            players[player].store_train_card(tc.get_train_card_from_face_up_pile(play[1]))
                        break
                    except Exception as e:
                        print (e)
                        raise e
                            

                #####################################################################
                # pick route cards
                #####################################################################
                elif play[0] == "rc":
                    pick_route_cards(players[player], min_cards_to_keep = 1) 
                    break

                #####################################################################
                # buy track
                # bt city1 city2 color
                #####################################################################
                else:
                    try:
                        if len(play) < 3:
                            raise Exception("format: bt city1 city2 color")
                        if play[1] in ttr.valid_cities:
                            city1 = play[1]
                        else:
                            raise Exception(play[1] + " is not a valid city")
                        if play[2] in ttr.valid_cities:
                            city2 = play[2]
                        else:
                            raise Exception(play[2] + " is not a valid city")
                        if play[3] in ttr.colors or play[3] == "wild":
                            color = play[3]
                        else:
                            raise Exception(play[3] + " is not a valid track color")
                        
                        # validate track exists
                        tracks_exist = []
                        for track in ttr.track_list:
                            if((track.city1 == city1 and track.city2 == city2) or
                               (track.city1 == city2 and track.city2 == city1)):
                               tracks_exist.append(track)
                        if not tracks_exist:
                            raise Exception( play[1] + " " + play[2] + " is not a valid track")

                        # check if all are owned
                        tracks_available = []
                        for track in tracks_exist:
                            if track.owner == -1:
                                tracks_available.append(track)
                        if not tracks_available:
                            raise Exception( play[1] + " " + play[2] + " is owned")
                        
                        # does the player have the cards needed to buy the track
                        found_track = False
                        for track in tracks_available:
                            if (track.color == color or track.color == 'grey') and players[player].can_afford(track, color):
                                players[player].buy_track(track, color)
                                found_track = True
                                break
                        if not found_track:
                            raise Exception("you do not have enough " + color + " cards to buy the track")
                        break
                    except Exception as e:
                        raise e
            except Exception as e:
                print (e)
                play = input('enter play -> ')
                play = play.split()

        

        if last_play_of_game and player == last_player:
            # TODO: report winner, final score
            break
        
        if players[player].get_train_count() <= 2:
            last_play_of_game = True
            last_player = player
            
        if player < number_of_players - 1 :
            player += 1
        else:
            player = 0
         
    if not test:
        for player in range(number_of_players):
            connection_list[player].close()  # close the connection


if __name__ == '__main__':
    server_program()
