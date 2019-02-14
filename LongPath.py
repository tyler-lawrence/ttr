import networkx as nx
import ttr

g = nx.Graph()
# g_list = [(1,2), (2,3), (3,4), (4,5), (5,6), (13,7), (7,8), (8,2), (8,3), (3,9), (9,10), (10,11), (11,12), (14,15), (15,16)]

my_tracks = [
              ttr.track('el_paso','dallas','red',4),
              ttr.track('helena','winnipeg','blue',4),
              ttr.track('helena','salt_lake','pink',3),
              ttr.track('helena','denver','green',4),
              ttr.track('salt_lake','denver','red',3),
              ttr.track('denver','kansas_city','orange',4),
              ttr.track('denver','santa_fe','grey',2),
              ttr.track('phoenix','santa_fe','grey',3),
              ttr.track('phoenix','el_paso','grey',3),
              ttr.track('santa_fe','el_paso','grey',2),
              ttr.track('denver','kansas_city','black',4),
             ]


#g.add_edges_from(track_list)
for t in my_tracks:
    g.add_edge(t.city1, t.city2, weight = t.length)

def longest(g, city):
#    print(longest_track, track_length, traversed, city)
    neighbors = [n for n in nx.all_neighbors(g,city)]
    if len(neighbors) == 1:
        edge = (city, neighbors[0])
        longest_path = [city, neighbors[0]]
        longest_path_length = g.edges[edge]['weight']
        g.remove_node(city)
    else:
        longest_path = []
        longest_path_length = 0
        for n in neighbors:
            this_g = g.copy().remove_edge(city, n)
            this_g, this_longest_path, this_longest_path_length = longest(g, n)
            if this_longest_path_length > longest_path_length:
                longest_path_length = this_longest_path_length
                longest_path = this_longest_path
                g = this_g
    return g, longest_path, longest_path_length


for i,city in enumerate(g.nodes):
    if i == 0:
        city2 = next(g.neighbors(city))
        long_track = [city, city2]
        track_length = g.edges[(city,city2)]['weight']
        g, longest_path, longest_path_length =  longest(g, city)
    if this_track_length > track_length:
        long_track = this_track
        
print(long_track)