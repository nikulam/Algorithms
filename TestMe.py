#%%
import numpy as np
from node import Node
from message import Message
from q import MessageQueue, ShortestQueue, WidestQueue
from link import Link
import sys
from node import Swp
import pandas as pd
import matplotlib.pyplot as plt
from proj import simulate


mode = 'swp'
network = 'net.csv'
df = pd.read_csv(network, header=None, delimiter=',')
df = pd.DataFrame({'tail': df[0], 'head': df[1], 'width': df[2], 'length': df[3]})

#Get each unique node and append to a list of all node id's
node_ids = []
for i, row in df.iterrows():
    if len(row) == 4:
        if str(row['tail']) not in node_ids:
            node_ids.append(str(row['tail']))

        if str(row['head']) not in node_ids:
            node_ids.append(str(row['head']))

    else: raise Exception('Input in wrong format')

#Create Node objects from identifiers
nodes = [Node(n) for n in node_ids]

#Add in-neighbors for each node and create link objects
links = []
for i, row in df.iterrows():
    u = str(row['tail'])
    v = str(row['head'])
    width = float(row['width'])
    length = float(row['length'])
    tail = [n for n in nodes if n.id == u][0]
    head = [n for n in nodes if n.id == v][0]
  
    head.add_ins(tail, width, length)
    links.append(Link(v + ',' + u, head, tail))


nodes = simulate('x', mode)
print(nodes)
#%%