from enum import Enum
import math
import random
import string

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
        #This list will be used for storing information about edges
        self.list = list()

class Edge:
    def __init__(self, source = None, destination = None, weight = None):
        self.source = source
        self.destination = destination
        self.weight = weight

def print_vertex(vertex):
    for i in vertex:
        print(" --------->", "Node: ", i.data)
        for j in i.list:
            print(j.destination.data, " weight:", j.weight)

def destination_differentiation(number_list, number_of_vertices):
    number_found_flag = True
    random_number = random.randint(0, number_of_vertices - 1)
    for i in number_list:
        if (i == random_number):
            number_found_flag = True
        else:
            number_found_flag = False

    if(number_found_flag):
        destination_differentiation(number_list, number_of_vertices)
    else:
        return random_number

def generate_random_graph():
    #variable for storing recurring destination vertices
    seen_numbers = list()
    number_of_vertices = random.randint(3, 5)
    vertex_list = []
    rand_num = 0
    for i in range(1, number_of_vertices + 1):
        #print("Adding vertices to list!")
        vertex_list.append(Vertex(data = i))
    for vertex in vertex_list:
       # print("Adding edges to each vertex!")
        number_of_edges = random.randint(0, number_of_vertices)
        for i in range(0, number_of_edges):
            #print("Adding source, destination and weight to each edge!")
            rand_num = destination_differentiation(seen_numbers, number_of_vertices)
            seen_numbers.append(rand_num)
            vertex.list.append(Edge(source = vertex, destination = vertex_list[rand_num], weight = random.randint(0, 20)))
    return vertex_list


if __name__ == "__main__":
    vertex_list = list()
    s = Vertex(data = 's')
    t = Vertex(data = 't')
    x = Vertex(data = 'x')
    y = Vertex(data = 'y')
    z = Vertex(data = 'z')

    s.list.append(Edge(s, t, 10))
    s.list.append(Edge(s, y, 5))

    t.list.append(Edge(t, x, 1))
    t.list.append(Edge(t, y, 2))

    x.list.append(Edge(x, z, 4))

    y.list.append(Edge(y, t, 3))
    y.list.append(Edge(y, x, 9))
    y.list.append(Edge(y, z, 2))

    z.list.append(Edge(z, s, 7))
    z.list.append(Edge(z, x, 6))

    vertex_list.append(s)
    vertex_list.append(t)
    vertex_list.append(x)
    vertex_list.append(y)
    vertex_list.append(z)

    print("\n---------first print----------\n")
    print_vertex(vertex_list)

    print("\n---------generate random graph----------\n")
    vertex_list_rand = generate_random_graph()

    print("\n---------second print----------\n")
    print_vertex(vertex_list_rand)
