"""
TODO: Remove Nodes list from Graph class; it is redundant and it can be contained in MQTT Brokers list
"""

from enum import Enum
import math
import random
import string
import time
import paho.mqtt.client as mqtt
from collections import defaultdict

received_message = ''
PORT = 1883

class Broker:
    name = ''

    # Constructor
    def __init__(self, name = None):
        self.name = name

    # client.subscribe("$share/group_one/up/+")

    def on_message(client, userdata, msg):
        print("message received ", str(msg.payload.decode("utf-8")))
        print("message topic=", msg.topic)
        print("message qos=", msg.qos)
        print("message retain flag=", msg.retain)
        message = str(msg.payload.decode("utf-8"))
        client.publish("up/data", message)

class Subscriber:
    name = ''

    # Constructor
    def __init__(self, name = None):
        self.name = name

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # client.subscribe("python/test")
        client.subscribe("$share/group_one/up/+")

    def on_message(client, userdata, msg):
        print("message received ", str(msg.payload.decode("utf-8")))
        print("message topic=", msg.topic)
        print("message qos=", msg.qos)
        print("message retain flag=", msg.retain)
        received_message = str(msg.payload.decode("utf-8"))

class Graph:
    nodes = list()
    brokers = list()
    mqtt_brokers = list()

    subscribers = {}
    mqtt_clients = list()

    edges = list()

    # Constructor
    def __init__(self):
        self.nodes = list()
        self.brokers = list()
        self.mqtt_brokers = list()
        self.subscribers = {}
        self.mqtt_clients = list()
        self.edges = list()

def Broker_Connect(broker):
    client = mqtt.Client(broker.name)

    client.on_connect = On_Connect
    client.connect("localhost", PORT)
    client.on_message = on_message
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()

def On_Connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("python/test")

# Function to print a BFS of graph
def BFS(graph, source_node):
    print("\nBreadth First Search:")

    # Mark all the vertices as not visited
    visited = [False] * (len(graph.nodes))

    # Create a queue for BFS
    queue = list()

    # Mark the source node as visited and enqueue it
    queue.append(source_node)
    visited[source_node] = True

    while queue:
        # Dequeue a vertex from queue and print it
        source_node = queue.pop(0)
        print(source_node, end = " ")

        # Get all adjacent vertices of the
        # dequeued vertex source_node. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        for i in graph.nodes:
            if visited[i] == False:
                queue.append(i)
                visited[i] = True
    print()

def Random_String(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def Print_Graph(graph):
    print("\n***************************Graph***************************\n")
    for node in graph.nodes:
        print(node)
    print()
    for edge in graph.edges:
        print(str(edge[0]) + ' ' + str(edge[1]))
    print()
    for node in graph.subscribers:
        print("Node:\t", node)
        for sub in graph.subscribers[node]:
            print("Subscriber:", sub.name)

def Get_Predefined_Dag():
    sub_count = 1
    nodes = 3
    adjacency = list()
    subscriber_list = list()
    clients = list()

    S1 = Subscriber()
    S2 = Subscriber()
    S3 = Subscriber()
    S4 = Subscriber()
    S5 = Subscriber()
    S6 = Subscriber()

    subscriber_list.append(S1)
    subscriber_list.append(S2)
    subscriber_list.append(S3)
    subscriber_list.append(S4)
    subscriber_list.append(S5)
    subscriber_list.append(S6)

    for sub in subscriber_list:
        sub.name = "S" + str(sub_count)
        sub_count += 1

    # Fill the adjacency list
    adjacency.append((0, 1))
    adjacency.append((1, 2))

    G = Graph()
    # Append nodes
    for i in range(nodes):
        G.nodes.append(i)
    # Append adjacencies
    for i in range(len(adjacency)):
        G.edges.append(adjacency[i])
    # Append subscribers
    G.subscribers = {G.nodes[0]: [S1, S2], G.nodes[1]: [S3, S4, S5], G.nodes[2]: [S6]}
    # Append MQTT clients
    for i in range(len(subscriber_list)):
        client = mqtt.Client(subscriber_list[i].name)
        G.mqtt_clients.append(client)

    for i in range(nodes):
        G.brokers.append(Broker())

    for i in range(nodes):
        G.brokers[i].name = "B" + str(G.nodes[i])
        client = mqtt.Client(G.brokers[i].name)
        G.mqtt_brokers.append(client)

    return G

"""
def Get_Random_Dag():
    # Nodes/Rank: How 'fat' the DAG should be
    MIN_PER_RANK = 1
    MAX_PER_RANK = 2
    # Ranks: How 'tall' the DAG should be
    MIN_RANKS = 6
    MAX_RANKS = 10
    # Chance of having an Edge
    PERCENT = 0.3
    # Max num of subs per node
    MAX_SUBS = 5

    nodes = 0
    adjacency = list()
    sub_count = 1
    subscriber_list = list()
    sub_count = 1

    ranks = random.randint(MIN_RANKS, MAX_RANKS)

    for i in range(ranks):
        # New nodes of 'higher' rank than all nodes generated till now
        new_nodes = random.randint(MIN_PER_RANK, MAX_PER_RANK)
        # Edges from old nodes ('nodes') to new ones ('new_nodes')
        for j in range(nodes):
            for k in range(new_nodes):
                if random.random() < PERCENT:
                    adjacency.append((j, k + nodes))

        nodes += new_nodes

    # Compute transitive graph
    G = Graph()
    # Append nodes
    for i in range(nodes):
        G.nodes.append(i)
    # Append adjacencies
    for i in range(len(adjacency)):
        G.edges.append(adjacency[i])
    # Add subscribers to node
    for i in range(nodes):
        num_of_subs = random.randint(0, MAX_SUBS)
        for j in range(num_of_subs):
            subscriber_list.append(Subscriber())
        G1 = {G.nodes[i]: subscriber_list}
        G.subscribers.update(G1)
        subscriber_list = list()

    for node in G.subscribers:
        for subscriber in G.subscribers[node]:
            subscriber.name = "S" + str(sub_count)
            sub_count += 1

    return G
"""

"""
Main function
"""
if __name__ == "__main__":
    """
    random_graph = Get_Random_Dag()
    Print_Graph(random_graph)

    random_graph.BFS(4)
    """
    predefined_graph = Get_Predefined_Dag()
    Print_Graph(predefined_graph)

    broker = Broker("B1")
    Broker_Connect(broker)

    BFS(predefined_graph, 1)

