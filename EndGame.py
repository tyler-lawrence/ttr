import networkx as nx
import ttr

players = []
tc = ttr.train_card()

number_of_players = 3
for i in range(number_of_players):
    players.append(ttr.player(i))
track = 
players[0].buy_track(tc, ttr.track('san_francisco','salt_lake','orange',5), “orange”)


def EndGame():
    print("\n================================")
    print("========   end of game =========")
    print("================================\n")
    players_longest_trains = []
    players_longest_paths = []
    longest_train = 0
    
    # create a list of each players longest trains
    for player in players:
        longest_path, longest_path_length = player.longest_track()
        players_longest_trains.append(longest_path_length)
        players_longest_paths.append(longest_path)
        if longest_path_length > longest_train:
            longest_train = longest_path_length

    # see if there were any ties for longest train
    if players_longest_trains.count(longest_train) > 1:
        print("players tied for longest train, length " + str(longest_train))
        for i, length in enumerate(players_longest_trains):
            if length == longest_train:
                print("player {0:d}".format(i))
                print(players_longest_paths[i])
    else:
        for i, length  in enumerate(players_longest_trains):
            if length == longest_train:
                print ("player {0:d} had the longest train, length {1:d}".format( i, longest_train))
                print (players_longest_paths[i])
                break
    
    high_score = 0
    player_scores = []
    
    # calculate each players score
    for player in players:
        score = player.points
        completed_route_cards = 0
        print("\nplayer {0:d} scored {1:d} for track segments owned".format(player.index, player.points))
        if players_longest_trains[player.index] == longest_train:
            print("player {0:d} scored 10 points for longest train".format(player.index))
            score += 10 # bonus for longest train
        for rc in player.route_cards:
            if player.route_completed(rc):
                print("player {0:d} completed route {1:s} {2:s} for {3:d} points".format(player.index, rc.city1, rc.city2, rc.points))
                score += rc.points
                completed_route_cards += 1
            else:
                print("player {0:d}  did not complete route {1:s} {2:s} -{3:d} points".format(player.index, rc.city1, rc.city2, rc.points))
                score -= rc.points
        player_scores.append((player.index, score, completed_route_cards))
        
    # TODO: report winner, final score
    # is there a tie
    player_scores.sort(key = lambda score: score[1], reverse = True)
    high_score = player_scores[0][1]
    ties = list(filter(lambda player_scores : player_scores[1] == high_score, player_scores  ))
    if len(ties) == 1 :
        # print winner
        pass
    else:
        ties.sort(key = lambda completed : ties[2], reverse = True)
        most_completed = ties[0][2]
        ties = list(filter(lambda ties : ties[2] == most_completed, ties))
        if ties.count() == 1:
            #print winner
            pass
        else:
            ties.sort(key = lambda longest_track : ties[3], reverse = True)
            longest_track = ties[0][3]
            ties = list(filter(lambda ties : ties[3] == longest_track, ties))
            if ties.count() == 1:
                #print winner
                pass
            else:
                #print winners
                pass

            # player with the most completed route cards breaks the tie
            # still tied, player with longest train is the tie breaker
EndGame()
