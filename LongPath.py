import networkx as nx
import ttr
import matplotlib.pyplot as plt

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
             ]

# my_tracks = [
              # ttr.track('omaha','chicago','blue',2),
              # ttr.track('chicago','pittsburgh','orange',3),
              # ttr.track('kansas_city','saint_louis','blue',2),
              # ttr.track('saint_louis','pittsburgh','green',5),
              # ttr.track('oklahoma_city','little_rock','grey',2),
              # ttr.track('little_rock','nashville','white',3),
              # ttr.track('nashville','raleigh','black',3),
              # ttr.track('pittsburgh','raleigh','grey',2),
             # ]

def longest(g, path_length, path, city):
    neighbor_list = [n for n in nx.neighbors(g,city)]
    longest_path = []
    longest_path_length = 0

    if neighbor_list:
        for n in neighbor_list:
            this_g = g.copy()
            edge = (city,n)
            this_edge_length = g.edges[edge]['weight']
            this_g.remove_edge(city, n)
            this_g, this_longest_path, this_longest_path_length = longest(this_g, this_edge_length, [edge], n)
            if this_longest_path_length > longest_path_length:
                longest_path_length = this_longest_path_length
                longest_path = this_longest_path
                longest_g = this_g
    else:
        return g, path, path_length
    path_length += longest_path_length
    path.extend(longest_path)
    return longest_g, path, path_length

print("libs loaded")
gbase = nx.Graph()
gmap = nx.Graph()

for t in ttr.track_list:
    gmap.add_edge(t.city1, t.city2, weight = t.length)

for t in my_tracks:
    gbase.add_edge(t.city1, t.city2, weight = t.length)

longest_track_length = 0;
longest_path = []

for city in gbase.nodes():
    g = gbase.copy()
    g, path, track_length = longest(g, 0, [], city)
    if track_length > longest_track_length:
        longest_track_length = track_length
        longest_path = path

        
plt.figure(1,figsize=(10,6))
plt.gca().invert_yaxis()
nx.draw_networkx(gmap,pos=ttr.valid_cities,with_labels=True, style='dashed')
nx.draw_networkx(gbase,pos=ttr.valid_cities,with_labels=True, edge_color='blue', style='dashed', width = 3.0)
nx.draw_networkx_edges(gbase,pos=ttr.valid_cities, edgelist=longest_path, edge_color='blue',width = 4.0, with_labels=True)
plt.show()
print(longest_path, longest_track_length)