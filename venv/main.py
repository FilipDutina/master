from enum import Enum
import math
import random
import string
import time
import paho.mqtt.client as mqtt
import networkx as nx

class VertexColor(Enum):
    BLACK = 0
    GRAY = 127
    WHITE = 255

class Publisher:
    message = ''
    topic = ''
    def __init__(self, message = None, topic = None):
        self.message = message
        self.topic = topic

class Subscriber:
    message = ''
    topic = ''
    def __init__(self, message = None, topic = None):
        self.message = message
        self.topic = topic

class Vertex:
    """
    Graph vertex: A graph vertex (node)
    """
    def __init__(self, name = None, color = None, parent = None):
        """
        Vertex constructor
        """
        self.name = name
        self.color = color
        self.parent = parent
        self.edgeList = list()
        self.subscribers = list()

class Edge:
    def __init__(self, source = None, destination = None, weight = None):
        self.source = source
        self.destination = destination
        self.weight = weight

def Breadth_First_Search(graph, current_vertex):
    for vertex in graph:
        vertex.color = VertexColor.WHITE
        vertex.parent = None

    current_vertex.color = VertexColor.GRAY
    current_vertex.parent = None
    Queue = list()
    Queue.append(current_vertex)
    while len(Queue) is not 0:
        vertex_parent = Queue.pop(0)
        for v in graph:
            if (v.color == VertexColor.WHITE):
                v.color = VertexColor.GRAY
                v.parent = vertex_parent
                Queue.append(v)
                print(v.name)

        current_vertex.color = VertexColor.BLACK

def Random_String(stringLength = 5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def Print_Vertex(vertex):
    for i in vertex:
        print(i.name)
    print()
    for j in i.edgeList:
        print(j.destination.name)


def Get_Random_Dag():
    MIN_PER_RANK = 1    # Nodes/Rank: How 'fat' the DAG should be
    MAX_PER_RANK = 2
    MIN_RANKS = 6   # Ranks: How 'tall' the DAG should be
    MAX_RANKS = 10
    PERCENT = 0.3  # Chance of having an Edge
    nodes = 0

    ranks = random.randint(MIN_RANKS, MAX_RANKS)

    vertex_list = []
    for i in range(ranks):
        # New nodes of 'higher' rank than all nodes generated till now
        new_nodes = random.randint(MIN_PER_RANK, MAX_PER_RANK)

        # Edges from old nodes ('nodes') to new ones ('new_nodes')
        for j in range(nodes):
            for k in range(new_nodes):
                if random.random() < PERCENT:
                    #sredi ovo!!!!!!
                    vertex_list.append(Vertex(edgeList.append = (j, k + nodes)))

        nodes += new_nodes
    print(ranks)

    return vertex_list

"""
Main function
"""
if __name__ == "__main__":
    vertex_list = list()

    B1 = Vertex(name='B1')
    B2 = Vertex(name='B2')
    B3 = Vertex(name='B3')

    #edges
    B1.edgeList.append(Edge(B1, B2, 1))
    B2.edgeList.append(Edge(B2, B3, 1))

    #subscribers
    B1.subscribers.append(Subscriber('', 'Topic1'))
    B1.subscribers.append(Subscriber('', 'Topic2'))

    B2.subscribers.append(Subscriber('', 'Topic1'))
    B2.subscribers.append(Subscriber('', 'Topic2'))
    B2.subscribers.append(Subscriber('', 'Topic3'))

    B3.subscribers.append(Subscriber('', 'Topic1'))

    vertex_list.append(B1)
    vertex_list.append(B2)
    vertex_list.append(B3)

    #Generate_Random_Graph()
    #Print_Vertex(vertex_list)
    vertex_list = Get_Random_Dag()
    #Print_Vertex(vertex_list)
    """ print("\n\n****************************************first print***********************************************")
    Print_Vertex(vertex_list)
    print("\n\n****************************************second print***********************************************")
    Breadth_First_Search(vertex_list, B1)
    print("\n\n****************************************Generate_Random_Graph()***********************************************")
    vertex_list = Generate_Random_Graph()
    Print_Vertex(vertex_list)
    print("\n------------------------------------------> BFS \n")
    Breadth_First_Search(vertex_list, vertex_list[0])"""
