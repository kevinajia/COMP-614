"""
COMP 614
Homework 4: Graphs
"""

import comp614_module4


def file_to_graph(filename):
    """
    Given the name of a file, reads the contents of that file and uses it to
    build a graph. Assumes that each line will contain the name of a single node.
    If the line does not start with a tab, it contains the name of a new node to
    be added to the graph. If the line starts with a tab, it contains the name of
    a node that is a neighbor of the most recently added node.

    For example, imagine that the file is structured as follows:
    node1
        node2
        node3
    node2
        node1
    node3

    In this case, the graph has three nodes: node1, node2, and node3. node1 has
    outbound edges to node2 and node3. node2 has an outbound edge to node1. node3
    has no outbound edges.
    """
    file_f = open(filename, "r")
    lines = file_f.readlines()

    list_text = []
    for line in lines:
        if line != "\n":
            list_text.append(line)

    graph_g = comp614_module4.DiGraph()
    parent_node = ''
    for node in list_text:
        clean_node = node.strip("\n")
        if clean_node.startswith('\t'):
            graph_g.add_edge(parent_node, clean_node.strip())
        else:
            graph_g.add_node(clean_node.strip())
            parent_node = clean_node

    return graph_g


class Queue:
    """
    A representation of a FIFO queue.
    """

    def __init__(self):
        """
        Constructs a new empty queue.
        """
        self._queue = []

    def __len__(self):
        """
        Returns an integer representing the number of items in the queue.
        """
        return len(self._queue)

    def __str__(self):
        """
        Returns a string representation of the queue.
        """
        return str(self._queue)

    def push(self, item):
        """
        Adds the given item to the queue.
        """
        self._queue.append(item)

    def pop(self):
        """
        Removes and returns the least recently added item from the queue.
        Assumes that there is at least one element in the queue.
        """
        return self._queue.pop(0)

    def clear(self):
        """
        Removes all items from the queue.
        """
        self._queue.clear()


def bfs(graph, start_node):
    """
    Performs a breadth-first search on the given graph starting at the given
    node. Returns a two-element tuple containing a dictionary mapping each
    node to its distance from the start node and a dictionary mapping each
    node to its parent in the search.
    """
    queue = Queue()
    dist = {}
    parent = {}
    for node in graph.nodes():
        dist[node] = float('inf')
        parent[node] = None
    dist[start_node] = 0
    queue.push(start_node)
    while queue:
        node = queue.pop()
        neighbors_node = graph.get_neighbors(node)
        for neighbor in neighbors_node:
            if dist.get(neighbor) == float('inf'):
                dist[neighbor] = dist.get(node) + 1
                parent[neighbor] = node
                queue.push(neighbor)
    return dist, parent


def connected_components(graph):
    """
    Finds all weakly connected components in the graph. Returns these components
    in the form  of a set of components, where each component is represented as a
    frozen set of nodes. Should not mutate the input graph.
    """
    new_graph = graph.copy()

    for node in new_graph.nodes():

        neighbors_set = new_graph.get_neighbors(node)
        for node_n in neighbors_set:
            new_graph.add_edge(node, node_n)
            new_graph.add_edge(node_n, node)

    weakly_connected = set()

    for node in new_graph.nodes():
        curr_fr_set = set()
        dist, _ = bfs(new_graph, node)
        for key, distance in dist.items():
            if distance != float('inf'):
                if key not in curr_fr_set:
                    curr_fr_set.add(key)
                else:
                    pass

        weakly_connected.add(frozenset(curr_fr_set))

    return weakly_connected






# print(file_to_graph("test0.txt"))
# print(file_to_graph("test0.txt").nodes())
# print(file_to_graph("test2.txt"))
# print(file_to_graph("test2.txt").nodes())
# graph = file_to_graph("test6.txt")
# graph12 = (file_to_graph("test12.txt"))
wikipedia_articles = file_to_graph("wikipedia_articles.txt")
# print(bfs(wikipedia_articles, 'rice university')[0])
# print(bfs(wikipedia_articles, 'university of florida')[0])
# print(bfs(graph12, 'B'))
# print(bfs(graph9, 'C'))
# print(bfs(graph9, 'D'))

# graph9 = (file_to_graph("test9.txt"))
print(connected_components(wikipedia_articles))
