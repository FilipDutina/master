from enum import Enum
import math
import random
import string
import time

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
    Graph vertex: A graph vertex (node) with data
    """
    def __init__(self, color = None, parent = None, data = None):
        """
        Vertex constructor
        @param color, parent, auxilary data1, auxilary data2
        """
        self.color = color
        self.parent = parent
        self.data = data
        self.edgeList = list()
        self.subscribers = list()

class Edge:
    def __init__(self, source = None, destination = None, weight = None):
        self.source = source
        self.destination = destination
        self.weight = weight

def randomString(stringLength = 5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def print_vertex(vertex):
    for i in vertex:
        print("\n\n -------------->", "Node: ", i.data)
        for j in i.edgeList:
            print(j.destination.data, "weight:", j.weight)
        print("")
        for subscriber in i.subscribers:
            print("Message:", subscriber.message, ", Topic:", subscriber.topic)

def generate_random_graph():
    #variable for storing recurring destination vertices
    seen_numbers = list()
    number_of_vertices = random.randint(3, 50)
    vertex_list = []
    rand_num = 0
    seen_numbers.append(0)
    for i in range(1, number_of_vertices + 1):
        #print("Adding vertices to list!")
        vertex_list.append(Vertex(data = i))
    for vertex in vertex_list:
       # print("Adding edges to each vertex!")
        number_of_edges = random.randint(0, number_of_vertices)
        for i in range(0, number_of_edges):
            #print("Adding source, destination and weight to each edge!")
            same_num_flag = False
            while(True):
                rand_num = random.randint(0, number_of_vertices - 1)
                for iter in seen_numbers:
                    if (iter == rand_num):
                        same_num_flag = True
                if(same_num_flag == False):
                    break
                same_num_flag = False
            seen_numbers.append(rand_num)
            vertex.edgeList.append(Edge(source = vertex, destination = vertex_list[rand_num], weight = random.randint(0, 20)))
        seen_numbers.clear()
    return vertex_list

"""
Main function
"""
if __name__ == "__main__":
    vertex_list = list()

    B1 = Vertex(data='B1')
    B2 = Vertex(data='B2')
    B3 = Vertex(data='B3')

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

    print_vertex(vertex_list)

    p = Publisher()
    p.message = 'Hello world'
    p.topic = 'Topic1'
    print(p.message)

    for broker in vertex_list:
        for subs in broker.subscribers:
            if(subs.topic == p.topic):
                subs.message = p.message

    print("\n\n****************************************second print***********************************************")
    print_vertex(vertex_list)
