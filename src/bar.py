#%%
import pandas as pd
import numpy as np
import os
import re
from networkx.algorithms import bipartite
import networkx as nx
import matplotlib.pyplot as plt
import json 


# %%



# %%
# create graph


# %%
class Bar:
    def __init__(self, graph, cocktails, ingredients):
        self.graph = graph
        self.cocktails = cocktails
        self.ingredients = ingredients

    @classmethod
    def from_json(cls, path):
        with open(path) as f: # open file
            data = json.load(f) 
        
        cocktails = [] #
        edges = []
        ingredients = []

        for cock in data:
            cocktails.append(cock['name'])
            for i in cock['ingredients']:
                ingredients.append(i['ingredient'])
                edges.append((cock['name'], i['ingredient']))


        gg = nx.DiGraph()

        gg.add_nodes_from(cocktails, bipartite = 0)
        gg.add_edges_from(edges)

        # adding the edges the ingredients nodes are created, 
        # so we set the bipartite attribure and the stock which is 1 if you have that ingredient 0 otherwise
        for i in gg.nodes:
            if 'bipartite' not in gg.nodes[i]:
                gg.nodes[i]['bipartite'] = 1
                gg.nodes[i]['stock'] = 1

        return cls(gg, cocktails, ingredients)


    def plot_graph(self):
        g = self.graph
        color = [0 if g.nodes[i]['bipartite']==0 else 1 for i in g.nodes]
        pos = nx.bipartite_layout(g,self.cocktails)
        #pos = nx.spring_layout(gg, k = 0.07)
        #pos = nx.multipartite_layout(g, subset_key='bipartite')
        nx.draw(g, with_labels=False, pos = pos, node_size = 10, node_color = color, width = 1)
        plt.show()

    def check_availability(self):
        g = self.graph
        for n in g.nodes():
            if(g.nodes[n]['bipartite'] == 0):
                total = 1
                for e in g.edges(n):
                    total = total * g.nodes[e[1]]['stock']
                if total == 1:
                    print(n)

    def get_ingredients(self, cocktails):
        nodes_to_include = set(cocktails)

        for ingredient in cocktails:
            if ingredient in self.graph:
                nodes_to_include.update(self.graph.neighbors(ingredient))
        
        return nodes_to_include
# %%
