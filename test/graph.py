import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from uti.utility import read_json

f = open('graph100.txt', 'r')
l = []
l = [line.split() for line in f]
x = 30
A = np.array(l).astype(np.float)
user = read_json("dict_100.json")
labels = {}
for key, value in user.items():
    labels[value] = key
edge_list = []

#admin = ["Vladimir", "Danil L", "Timo", "Guitar"]
admin = ["Guitar"]
samll_A = A[0:x, 0:x]
sumin = np.sum(samll_A, axis=0)
sumout = np.sum(samll_A, axis=1)

G = nx.DiGraph()
for i in range(x):
    for j in range(x):
        G.add_edge(labels[i], labels[j], weight=float(l[i][j]))
        if float(l[i][j]) > 0.2:
            edge_list.append(([(labels[i], labels[j])], float(l[i][j])))
nodesize = sumin[0:x]*50
nodes = G.nodes
adminnodes = []
adminnodessize= []
normalnodes = []
normlanodessize= []
index = 0
for node in nodes:
    if node in admin:
        adminnodes.append(node)
        adminnodessize.append(nodesize[index])
    else:
        normalnodes.append(node)
        normlanodessize.append(nodesize[index])
    index += 1
#3542587
seed = 3254
pos = nx.random_layout(G, seed = seed)
nodesize = sumin[0:x]*15
node_sizes = [nodesize]

# nodes
nx.draw_networkx_nodes(G, pos, nodelist=adminnodes, node_size= adminnodessize, node_color="red")
nx.draw_networkx_nodes(G, pos, nodelist=normalnodes, node_size= normlanodessize, node_color="green")
# edges

for edge in edge_list:
    li = edge[0]
    weight = edge[1]
    if weight > 3:
        weight /= 2
    nx.draw_networkx_edges(
    G, pos, edgelist=li, width=weight *2, alpha= 0.8, edge_color="black"
)
# labels
nx.draw_networkx_labels(G, pos, font_size=7, font_color="black", font_family="sans-serif")

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()
