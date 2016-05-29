class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []


class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

# Vertices
alice = Vertex("Alice")
bob = Vertex("Bob")

# Edges
alice.outbound_edges.append(Edge(alice, bob))

# Graph
vertices = [alice, bob]
edges = []
for vertex in vertices:
    edges.extend(vertex.outbound_edges)

graph = Graph(vertices, edges)
