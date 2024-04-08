from flask import Flask

#%%
from bar import Bar
import os 
from networkx.algorithms import bipartite
import networkx as nx
import matplotlib.pyplot as plt

# print current folder 
print(os.getcwd())

path = '/Users/alessiogandelli/dev/cantiere/personal-bar/data/drink.json'

bar = Bar.from_json(path)



#%%
cocktails = ['Black Russian']


nodes_to_include = set(cocktails)

for ingredient in cocktails:
    if ingredient in bar.graph:
        nodes_to_include.update(bar.graph.neighbors(ingredient))

subgraph = bar.graph.subgraph(nodes_to_include)



# %%
def plot_graph(g):
    
    color = [0 if g.nodes[i]['bipartite']==0 else 1 for i in g.nodes]
    #pos = nx.bipartite_layout(g, g.cocktails)
    #pos = nx.spring_layout(g, k = 0.07)
    pos = nx.multipartite_layout(g, subset_key='bipartite')
    nx.draw(g, with_labels=True, pos=pos, node_size=10, node_color=color, width=0.5, font_size=8)    
    plt.show()
# %%

plot_graph(subgraph)
# sort nodes by indegree

# %%
sorted(subgraph.nodes, key = lambda x: subgraph.in_degree(x), reverse = True)

# Get the bipartite sets
bipartite_sets = bar.graph.nodes(data=True)

# Separate the nodes into two lists based on their bipartite set
set1_nodes = [node for node, data in bipartite_sets if data['bipartite'] == 0]
set2_nodes = [node for node, data in bipartite_sets if data['bipartite'] == 1]

# Sort each set by degree in descending order, including the degree value
sorted_set1_nodes = sorted([(node, bar.graph.degree(node)) for node in set1_nodes], key=lambda x: x[1], reverse=True)
sorted_set2_nodes = sorted([(node, bar.graph.degree(node)) for node in set2_nodes], key=lambda x: x[1], reverse=True)

# Now, 'sorted_set1_nodes' and 'sorted_set2_nodes' contain tuples of nodes and their degrees, sorted by degree in descending order.