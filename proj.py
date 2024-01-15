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


#TO TEST THE SIMULATOR:
#Modify test_dest, test_source and network
#The network should have four columns
#Run the file and it prints in order:
#Wsp: Width, Lenght, Path
#Swp: Width, Length, Path
test_dest = '1'
test_source = '8'
network = 'Abilene.csv'

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


def simulate(destination, mode):
    mode = mode
    dest = destination
    #Remove paths from all nodes
    for n in nodes:
        n.nullify()
    for l in links:
        l.nullify()

    #Initialize destination
    dest_node = [n for n in nodes if n.id == dest][0]
    dest_node.wsp['length'] = 0
    dest_node.wsp['width'] = np.inf
    dest_node.wsp['path'] = dest
    dest_node.naive_swp['length'] = 0
    dest_node.naive_swp['width'] = np.inf
    dest_node.naive_swp['path'] = dest
    dest_node.swp = Swp(dest, np.inf, 0)
    dest_node.swps = [dest_node.swp]
    dest_node.stab_time = 0
    #Initialize the queue (=calendar)
    q = MessageQueue()
    for n in dest_node.ins.items():
        head = dest_node
        tail = n[0]
        link = [x for x in links if x.id == head.id + ',' + tail.id][0]
        send_time = 0
        travel_time = 1 + np.random.uniform(0,2)
        tail.stab_time = send_time + travel_time
        link.update(send_time + travel_time)
        #print(link.id, send_time, link.last_arrived)
        q.insert(Message(dest_node, n[0], n[1][0], n[1][1], send_time, travel_time, link))

    #While messages to be processed
    while not q.isEmpty():
        msg = q.pop()
        u = msg.tail
        if mode == 'wsp':
            u.compare_wsp(msg.head, msg.width, msg.length)
        elif mode == 'naive_swp':
            u.compare_naive_swp(msg.head, msg.width, msg.length)
        elif mode == 'swp':
            u.compare_swp(msg.head, msg.width, msg.length)

        if u.updated:
            for n in u.ins.items():
                head = u
                tail = n[0]
                link = [x for x in links if x.id == head.id + ',' + tail.id][0]
                send_time = msg.time
                travel_time = 1 + np.random.uniform(0,2)
                link.update(send_time + travel_time)
                tail.stab_time = link.last_arrived
                #print(link.id, send_time, link.last_arrived)
                q.insert(Message(head, tail, n[1][0], n[1][1], send_time, travel_time, link))


    #Return a list of nodes with updated paths and stabilization times
    return nodes


#A general Dijkstra's algorithm implemented with priority queue.
#Pass as a parameter one of the following: 'wsp', 'naive_swp', 'swp'
def algorithm(destination, mode):
    mode = mode
    dest = destination
    #Initialize the priority queue
    if mode == 'wsp':
        q = ShortestQueue()
    elif mode == 'naive_swp' or mode == 'swp':
        q = WidestQueue()

    #Remove each node's paths into previous destinations and insert into the queue
    for n in nodes:
        n.nullify()
        q.insert(n)
    #Manually initialize the destination node
    #Sets every order's best paths to be the optimal path
    dest_node = [n for n in nodes if n.id == dest][0]
    dest_node.wsp['length'] = 0
    dest_node.wsp['width'] = np.inf
    dest_node.wsp['path'] = dest
    dest_node.naive_swp['length'] = 0
    dest_node.naive_swp['width'] = np.inf
    dest_node.naive_swp['path'] = dest
    dest_node.swp = Swp(dest, np.inf, 0)
    dest_node.swps = [dest_node.swp]
    #While queue not empty
    while not q.isEmpty():
        v = q.pop()
        for u in v.ins.items():
            if mode == 'wsp':
                u[0].compare_wsp(v, u[1][0], u[1][1])
            elif mode == 'naive_swp':
                u[0].compare_naive_swp(v, u[1][0], u[1][1])
            elif mode == 'swp': 
                print(u)
                u[0].compare_swp(v, u[1][0], u[1][1])

    #Retun nodes with updated paths
    return nodes


algorithm('1', 'swp')
for node in nodes:
    #print(node.naive_swp['path'], node.naive_swp['length'], node.naive_swp['width'])
    #print(node.wsp['path'], node.wsp['length'], node.wsp['width'])
    print(node.swp.path, node.swp.length, node.swp.width)


'''
#To test the simulator
sim1 = simulate(test_dest, 'wsp')
s1 = [n for n in sim1 if n.id == test_source][0]
w1, l1, p1 = s1.wsp['width'], s1.wsp['length'], s1.wsp['path'][::-1]
sim2 = simulate(test_dest, 'naive_swp')
s2 = [n for n in sim2 if n.id == test_source][0]
w2, l2, p2 = s2.naive_swp['width'], s2.naive_swp['length'], s2.naive_swp['path'][::-1]
print('wsp:', w1, l1, p1)
print('swp:', w2, l2, p2)


#Alg
sim1 = algorithm(test_dest, 'wsp')
s1 = [n for n in sim1 if n.id == test_source][0]
w1, l1, p1 = s1.wsp['width'], s1.wsp['length'], s1.wsp['path'][::-1]
sim2 = algorithm(test_dest, 'swp')
s2 = [n for n in sim2 if n.id == test_source][0]
w2, l2, p2 = s2.swp.width, s2.swp.length, s2.swp.path[::-1]
print('wsp:', w1, l1, p1)
print('swp:', w2, l2, p2)
'''


#%%
#Run simulator or algorithm to find a path for each source-destination pairs
#Parameters of simulate() are ('wsp' or 'naive_swp') as a string
#Parameters of algorithm() are ('wsp' or 'naive_swp' or 'swp') as a string
'''
data1 = []


for dest_id in node_ids:
    print('sim dest:, ', dest_id)
    mode = 'swp'
    nodes = algorithm(dest_id, mode)
    for n in nodes:
        if mode == 'wsp':
            data1.append((n.stab_time, n.wsp['width'], n.wsp['length']))
        elif mode == 'naive_swp':
            data1.append((n.stab_time, n.naive_swp['width'], n.naive_swp['length'], n.naive_swp['path']))
        elif mode == 'swp':
            data1.append((n.stab_time, n.swp.width, n.swp.length))
        #sim.append((n.wsp['path'], n.wsp['width'], n.wsp['length']))
        #if n.wsp['width'] == 20:
        print(n.wsp['path'], n.wsp['width'], n.wsp['length'])
        #print(n.naive_swp['path'], n.naive_swp['width'], n.naive_swp['length'])
        #print(n.swp.path, n.swp.width, n.swp.length)

'''
'''
#Plot CCDF
times1 = list(sorted([x[0] for x in data1]))
widths1 = list(sorted([x[1] for x in data1]))
lengths1 = list(sorted([x[2] for x in data1]))

#times2 = list(sorted([x[0] for x in data2]))
#widths2 = list(sorted([x[1] for x in data2]))
#lengths2 = list(sorted([x[2] for x in data2]))

y = 1 * np.arange(len(data1)) / (len(data1) - 1)


#%%
plt.plot(times1, y[::-1], label='wsp', c='green')
#plt.plot(times2, y[::-1], label='swp')
plt.legend()
plt.title('CCDF of stabilization times')
plt.xlabel('Time')
plt.ylabel('Proportion of all values')

plt.show()

#%%
plt.plot(widths1, y[::-1], label='AS1239', c='green')
#plt.plot(widths2, y[::-1], label='Abilene', c='red')
#plt.legend()
plt.title('CCDF of widths')
plt.xlabel('Width')
plt.ylabel('Proportion of all values')
#%%
plt.plot(lengths1, y[::-1], label='AS1239', c='green')
#plt.plot(lengths2, y[::-1], label='Abilene', c='red')
#plt.legend()
plt.title('CCDF of lengths')
plt.xlabel('Length')
plt.ylabel('Proportion of all values')
'''