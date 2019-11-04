from enum import Enum
import math
import random
import string
import time
import paho.mqtt.client as mqtt
import networkx as nx
from collections import defaultdict

class Graph:
    nodes = list()
    edges = list()

    # Constructor
    def __init__(self):
        self.nodes = list()
        self.edges = list()

    # Function to print a BFS of graph
    def BFS(self, s):
        print("\nFollowing is Breadth First Search:")

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

def Random_String(stringLength = 5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def Print_Vertex(graph):
    print("\n***************************Graph***************************\n")
    for i in graph.nodes:
        print(i)
    print()
    for value in graph.edges:
        print(str(value[0]) + ' ' + str(value[1]))

def Get_Predefined_Dag():
    nodes = 3
    adjacency = list()

    adjacency.append((0, 1))
    adjacency.append((1, 2))

    G = Graph()
    # Append nodes
    for i in range(nodes):
        G.nodes.append(i)
    # Append adjacencies
    for i in range(len(adjacency)):
        G.edges.append(adjacency[i])

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
    nodes = 0
    adjacency = list()

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

    return G

"""
Main function
"""
if __name__ == "__main__":

    random_graph = Get_Random_Dag()
    Print_Vertex(random_graph)

    predefined_graph = Get_Predefined_Dag()
    Print_Vertex(predefined_graph)

    random_graph.BFS(0)

