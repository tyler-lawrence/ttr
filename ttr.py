import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# list of valid cities that can be used. Use this to throw errors or suggest cities to enter so it will match how I programmed cities.

valid_cities = [
    'atlanta',
    'boston',
    'calgary',
    'charleston',
    'chicago',
    'dallas',
    'denver',
    'duluth',
    'el_paso',
    'helena',
    'houston',
    'kansas_city',
    'las_vegas',
    'little_rock',
    'los_angeles',
    'miami',
    'montreal',
    'nashville',
    'new_orleans',
    'new_york',
    'oklahoma_city',
    'omaha',
    'phoenix',
    'pittsburgh',
    'portland',
    'raleigh',
    'saint_louis',
    'salt_lake',
    'san_francisco',
    'santa_fe',
    'sault_st_marie',
    'seattle',
    'toronto',
    'vancouver',
    'washington',
    'winnipeg'
]

colors = ['black','blue','white','green','red','orange','yellow','pink']

class track(object):
    def __init__(self,city1, city2, color, length, owner=0):
        try:
            # validate the parameters
            assert city1 in valid_cities, "city 1 is invalid: " + city1
            assert city2 in valid_cities, "city 2 is invalid: " + city2
            #assert color in colors, "color is invalid"
            assert length in range(1,7), "length is invalid: " + length
            # assert owner in range (0, number_of_plaers), "owner is invalid"
            
            self.city1 = city1
            self.city2 = city2
            self.color = color
            self.length = length
            self.owner = owner
        except AssertionError as e:
            print(e)
            
track_list = [track('vancouver','seattle','grey',1),
              track('vancouver','seattle','grey',1),
              track('vancouver','calgary','grey',3),
              track('calgary','seattle','grey',4),
              track('calgary','helena','grey',4),
              track('seattle','helena','yellow',6),
              track('helena','salt_lake','pink',3),
              track('portland','salt_lake','blue',6),
              track('portland','seattle','grey',1),
              track('portland','seattle','grey',1),
              track('portland','san_francisco','green',5),
              track('portland','san_francisco','pink',5),
              track('portland','salt_lake','blue',6),
              track('san_francisco','salt_lake','orange',5),
              track('san_francisco','salt_lake','white',5),
              track('san_francisco','los_angeles','yellow',3),
              track('san_francisco','los_angeles','pink',3),
              track('salt_lake','las_vegas','orange',3),
              track('las_vegas','los_angeles','grey',2),
              track('los_angeles','phoenix','grey',3),
              track('los_angeles','el_paso','black',6),
              track('phoenix','el_paso','grey',3),
              track('phoenix','denver','white',5),
              track('salt_lake','denver','red',3),
              track('salt_lake','denver','yellow',3),
              track('salt_lake','helena','pink',3),
              track('calgary','winnipeg','white',6),
              track('helena','duluth','orange',6),
              track('helena','omaha','red',5),
              track('helena','denver','green',4),
              track('denver','omaha','pink',4),
              track('denver','kansas_city','orange',4),
              track('denver','kansas_city','black',4),
              track('denver','oklahoma_city','red',4),
              track('denver','santa_fe','grey',2),
              track('santa_fe','el_paso','grey',2),
              track('santa_fe','oklahoma_city','blue',3),
              track('el_paso','oklahoma_city','yellow',5),
              track('el_paso','dallas','red',4),
              track('el_paso','houston','green',6),
              track('winnipeg','duluth','black',6),
              track('winnipeg','sault_st_marie','grey',6),
              track('duluth','sault_st_marie','grey',3),
              track('duluth','omaha','grey',2),
              track('duluth','omaha','grey',2),
              track('kansas_city','omaha','grey',1),
              track('kansas_city','omaha','grey',1),
              track('kansas_city','oklahoma_city','grey',2),
              track('kansas_city','oklahoma_city','grey',2),
              track('oklahoma_city','dallas','grey',2),
              track('oklahoma_city','dallas','grey',2),
              track('dallas','houston','grey',1),
              track('dallas','houston','grey',1),
              track('houston','new_orleans','grey',2),
              track('dallas','little_rock','grey',2),
              track('oklahoma_city','little_rock','grey',2),
              track('kansas_city','saint_louis','blue',2),
              track('kansas_city','saint_louis','pink',2),
              track('omaha','chicago','blue',2),
              track('duluth','chicago','red',3),
              track('duluth','toronto','pink',6),
              track('sault_st_marie','toronto','grey',2),
              track('sault_st_marie','montreal','black',5),
              track('chicago','toronto','white',4),
              track('chicago','pittsburgh','orange',3),
              track('chicago','pittsburgh','black',3),
              track('chicago','saint_louis','white',2),
              track('chicago','saint_louis','green',2),
              track('saint_louis','little_rock','grey',2),
              track('little_rock','new_orleans','green',3),
              track('saint_louis','pittsburgh','green',5),
              track('little_rock','nashville','white',3),
              track('new_orleans','atlanta','yellow',4),
              track('new_orleans','atlanta','orange',4),
              track('atlanta','nashville','grey',1),
              track('nashville','raleigh','black',3),
              track('nashville','pittsburgh','yellow',4),
              track('pittsburgh','toronto','grey',2),
              track('toronto','montreal','grey',3),
              track('pittsburgh','new_york','white',2),
              track('pittsburgh','new_york','green',2),
              track('montreal','new_york','blue',3),
              track('montreal','boston','grey',2),
              track('montreal','boston','grey',2),
              track('boston','new_york','yellow',2),
              track('boston','new_york','red',2),
              track('new_york','washington','black',2),
              track('new_york','washington','orange',2),
              track('washington','pittsburgh','grey',2),
              track('pittsburgh','raleigh','grey',2),
              track('washington','raleigh','grey',2),
              track('washington','raleigh','grey',2),
              track('atlanta','raleigh','grey',2),
              track('atlanta','raleigh','grey',2),
              track('raleigh','charleston','grey',2),
              track('atlanta','charleston','grey',2),
              track('charleston','miami','pink',2),
              track('miami','atlanta','blue',5),
              track('miami','new_orleans','red',6)
             ]

#create route cards
class route_card(object):
    '''
    class to store all route cards. in the face-up pile, face-down in the deck, or in the discard pile
    '''
    def __init__(self,city1, city2, points, owner=0, completed=False):
        try:
            assert city1 in valid_cities, "city 1 is invalid: " + city1
            assert city2 in valid_cities, "city 2 is invalid: " + city2
            self.city1 = city1
            self.city2 = city2
            self.points = points
            self.owner = owner
            self.completed = completed
        except AssertionError as e:
            print(e)
            
    def __str__(self):
        return "%s, %s, %d" % (self.city1, self.city2, self.points)

    def __repr__(self):
        return "%s, %s, %d" % (self.city1, self.city2, self.points)

route_card_list=[
    route_card('portland','phoenix',10),
    route_card('san_francisco','atlanta',17),
    route_card('montreal','atlanta',17),
    route_card('montreal','new_orleans',13),
    route_card('duluth','houston',8),
    route_card('vancouver','santa_fe',13),
    route_card('boston','miami',12),
    route_card('winnipeg','little_rock',11),
    route_card('seattle','los_angeles',9),
    route_card('dallas','new_york',11),
    route_card('los_angeles','miami',20),
    route_card('new_york','atlanta',6),
    route_card('sault_st_marie','oklahoma_city','9'),
    route_card('sault_st_marie','nashville',8),
    route_card('toronto','miami',10),
    route_card('winnipeg','houston',12),
    route_card('chicago','new_orleans',7),
    route_card('calgary','phoenix',13),
    route_card('calgary','salt_lake',7),
    route_card('los_angeles','new_york',21),
    route_card('duluth','el_paso',10),
    route_card('portland','nashville',17),
    route_card('seattle','new_york',22),
    route_card('denver','pittsburgh',11),
    route_card('vancouver','montreal',20),
    route_card('helena','los_angeles',8),
    route_card('kansas_city','houston',5),
    route_card('chicago','santa_fe',9),
    route_card('los_angeles','chicago',16),
    route_card('denver','el_paso',4)
]

def get_route_card():
    return route_card_list.pop(0)
#train cards
class train_card(object):
    '''
    class to store all train cards. in the face-up pile, face-down in the deck, or in the discard pile
    '''

    def __init__(self):      
        # builds initial deck of train cards
        self.deck = []
        self.face_up_pile = []
        self.discard_pile = []

        # create the train deck
        for i in range(12):
            for j in colors:
                self.deck.append(j)
        
        for i in range(14):
            self.deck.append('wild')
            
        random.shuffle(self.deck)

        #create the face up pile of train cards players can choose from
        for i in range(5):
            self.face_up_pile.append(self.get_train_card_from_deck())
        self.three_wild_check()
    
    #check to see if there are three wild cards in the face up pile. If yes, discard the face up pile and make a new face up pile       
    def three_wild_check(self):
        count = self.face_up_pile.count('wild')
        while count >= 3:
            self.discard_pile.append(self.face_up_pile)
            self.face_up_pile.clear()
            for i in range(5):
                self.face_up_pile.append(self.get_train_card_from_deck())
            count = self.face_up_pile.count('wild')

    def get_train_card_from_deck(self):
        card = self.deck.pop()
        if not self.deck:
            random.shuffle(self.discard_pile)
            self.deck = self.discard_pile.copy()
            self.discard_pile.clear()
        return card
    
    def get_face_up_pile(self):
        return self.face_up_pile
    
    def get_train_card_from_face_up_pile(self, pick):
        try:
            assert pick in self.face_up_pile, "not in face up pile: " + pick
            card = self.face_up_pile.pop(self.face_up_pile.index(pick))
            #replace the card that was just drawn
            self.face_up_pile.append(self.get_train_card_from_deck())
            self.three_wild_check()
            return card
        except AssertionError as e:
            print(e)
            
    
#distributes the intial starting cards. each person gets two cards
#print('cards in starting deck:',len(deck))
#n_p = 4 # number of players in the game
#hands = {}
#for i in range(n_p):
#    hands['player_{0}'.format(i+1)] = []
#    for j in range(2):
#        hands['player_{0}'.format(i+1)].append(deck[j])
#        deck.pop(j)
#print(hands)

class player(object):
    ''' 
    container for player state info
    '''
    def __init__(self):      
        # TODO: private variables should be named __name
        self.route_cards = []
        self.train_cards = dict({'black' : 0,'blue' : 0,'white' : 0,
                                 'green' : 0,'red' : 0,'orange' : 0,
                                 'yellow' : 0,'pink' : 0, 'wild' : 0})
        self.train_count = 0
        self.points = 0
            
    def store_route_card(self, route_card):
        self.route_cards.append(route_card)

    def store_train_card(self, train_card):
        self.train_cards[train_card] += 1
        
    def get_train_count(self):
        return self.train_count

#player_routes = {}
#for i in range(n_p):
#    player_routes['player_{0}_routes'.format(i+1)]=[]
#    for j in range(3):
#        rc =  route_card_list.pop(0)
#        player_routes['player_{0}_routes'.format(i+1)].append(rc)
#    print (player_routes)
       

# def discard(player_num):
    # print('player',player_num)
    # for i,val in enumerate(player_routes['player_{0}_routes'.format(player_num)]):
        # print(i,':',val.city1,val.city2,val.points)
    # discard_input = input('enter the numbers of the cards you wish to discard (i.e, if you wish to discard cards 0 and 1, type 0 1)')
    # discard_indices = discard_input.split()
    # discard_indices_2 = [int(i) for i in discard_indices]
    # discard_indices_2.sort(reverse=True)
    # print(discard_indices_2)
    
    # # NEED  TO RAISE AN ERROR IF USER INPUTS MORE THAN 2 CARDS OR INDICES THAT ARE OUT OF BOUNDS
    
    # for i in discard_indices_2:
        # player_routes['player_{0}_routes'.format(player_num)].pop(i)
    
    # for i,val in enumerate(player_routes['player_{0}_routes'.format(player_num)]):
        # print(i,':',val.city1,val.city2,val.points)


# def initial_hands(self, num_players):
    # hands = {} #dictionary to store cards a player is holding 
    # for i in range(n_p):
        # hands['player_{0}'.format(i+1)] = []
    # for j in range(2):
        # hands['player_{0}'.format(i+1)].append(self.deck[j])
        # self.deck.pop(j)
        
    # return hands

#for i in player_routes.keys():
    #print('*'*5,i,'*'*5)
    #for j in player_routes[i]:
     #   print(j.city1,j.city2,j.points)
    #print('--'*50)

#g = nx.MultiGraph()
#for i in track_list:
#    g.add_edge(i.city1,i.city2,i.length)
#
#plt.figure(1,figsize=(18,8))
#nx.draw_networkx(g,with_labels=True)
#
##nx.shortest_path(g,'vancouver','miami')
#
#g2 = nx.MultiGraph()
#for i in route_card_list:
#    g2.add_edge(i.city1,i.city2)
#    
#plt.figure(1,figsize=(18,8))
#nx.draw_networkx(g2,with_labels=True)

