from enum import Enum
import math
import random
import string
import time
import paho.mqtt.client as mqtt
import threading
# import networkx as nx
from collections import defaultdict

brokerList = []
clientList = []
threadList = []
threadCList = []


class ClientMoj(mqtt.Client):
    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        print("klijent dobija poruku", mqttc)
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed client: " + str(mid) + " " + str(granted_qos))

    def runClient(self):
        print("pre connect client")
        self.connect("localhost", 1883)
        print("pre subscribe client")
        self.subscribe("$share/group_one/up/+")
        print("subsribovao se klijent")
        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


class BrokerFirst(mqtt.Client):
    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        print("broker dobija poruku", mqttc)
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = str(msg.payload.decode("utf-8"))
        mqttc.publish("up/data", message)

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def run(self):
        print("pre connect broker")
        self.connect("localhost", 1883)
        print("pre subscribe broker")
        self.subscribe("python/test")

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


class BrokerOther(mqtt.Client):
    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        print("broker dobija porukuuuu", mqttc)
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = str(msg.payload.decode("utf-8"))
        # mqttc.publish("up/data", message)

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def runOther(self):
        print("Connect other broker")
        self.connect("localhost", 1883)
        self.subscribe("$share/group_one/up/+")

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


class Graph:
    nodes = list()
    edges = list()
    subscribers = {}

    # Constructor
    def __init__(self):
        self.nodes = list()
        self.edges = list()
        self.subscribers = {}

    # Function to print a BFS of graph
    def BFS(self, s):

        print("\nBreadth First Search:")

        # Mark all the vertices as not visited
        visited = [False] * (len(self.nodes))

        # Create a queue for BFS
        queue = list()

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        while queue:
            # Dequeue a vertex from queue and print it
            s = queue.pop(0)
            print(s, end=" ")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.nodes:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        print()


def Random_String(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def Print_Graph(graph):
    print("\n***************************Print Graph***************************\n")
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

    return G


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
    # brokerList.append(Broker("BrokerFirst"))
    for i in range(nodes):
        print("USAO SAM U FOR, VREDNOST I JE: ", i)
        # num_of_subs = random.randint(0, MAX_SUBS)
        # num_of_subs = 5
        # for j in range(num_of_subs):
        # subscriber_list.append(Subscriber())
        brokerList.append(BrokerOther("Broker" + str(i)))
        print("Apendovao brokera: ", i)
        # for n in range(2):
        #    clientList.append(ClientMoj("Broker"+str(i)+"Client"+str(n)))
        G1 = {G.nodes[i]: subscriber_list}
        G.subscribers.update(G1)
        subscriber_list = list()

    return G


"""
    for node in G.subscribers:
        for subscriber in G.subscribers[node]:
            subscriber.name = "S" + str(sub_count)
            sub_count += 1
"""
# return G

"""
Main function
"""
if __name__ == "__main__":

    random_graph = Get_Random_Dag()
    # Print_Graph(random_graph)

    random_graph.BFS(4)

    # predefined_graph = Get_Predefined_Dag()
    # Print_Graph(predefined_graph)

    # predefined_graph.BFS(1)
    BrokerFirst = BrokerFirst("BrokerFirst")
    t1 = threading.Thread(target=BrokerFirst.run)
    # t1.start()
    # t1.join()
    print("Duzina liste je: ", len(brokerList))

    for i in range(len(brokerList)):
        print("POKRECEM NITI ZA BROKERE")
        threadList.append(threading.Thread(target=brokerList[i].runOther))
        # for j in range(2):
        #    threadCList.append(threading.Thread(target=clientList[j+(2*i)].runClient))

    print("Duzina thread liste je: ", len(threadList))
    print("Duzina cthread liste je: ", len(threadCList))
    # r = 0
    t1.start()
    for i in range(len(threadList)):
        print("Starting broker: ", i)
        threadList[i].start()
        # for j in range(2):
        # print("RRRRR je sada: ", r)
        #    threadCList[j+(2*i)].start()
        # r += 1

    # r = 0
    t1.join()
    for i in range(len(threadList)):
        threadList[i].join()
        # for j in range(2):
        # print("RRRRRR Je sada: ", r)
        #    threadCList[j+(2*i)].join()
        # r += 1