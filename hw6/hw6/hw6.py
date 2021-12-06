"""
COMP 614
Homework 6: DFS + PageRank
"""

import comp614_module6


def bfs_dfs(graph, start_node, rac_class):
    """
    Performs a breadth-first search on graph starting at the given node.
    Returns a two-element tuple containing a dictionary mapping each visited
    node to its distance from the start node and a dictionary mapping each
    visited node to its parent node.
    """
    if rac_class == comp614_module6.Queue:

        # Initialize all data structures
        queue = comp614_module6.Queue()
        dist = {}
        parent = {}

        # Initialize distances and parents; no nodes have been visited yet
        for node in graph.nodes():
            dist[node] = float("inf")
            parent[node] = None

        # Initialize start node's distance to 0
        dist[start_node] = 0
        queue.push(start_node)

        # Continue as long as there are new reachable nodes
        while queue:
            node = queue.pop()
            nbrs = graph.get_neighbors(node)

            for nbr in nbrs:
                # Only update neighbors that have not been seen before
                if dist[nbr] == float('inf'):
                    dist[nbr] = dist[node] + 1
                    parent[nbr] = node
                    queue.push(nbr)

    else:

        # Initialize all data structures
        stack = comp614_module6.Stack()
        dist = {}
        parent = {}

        # Initialize distances and parents; no nodes have been visited yet
        for node in graph.nodes():
            dist[node] = float("inf")
            parent[node] = None

        # Initialize start node's distance to 0
        dist[start_node] = 0
        stack.push(start_node)

        # Continue as long as there are new reachable nodes
        while stack:
            node = stack.pop()
            nbrs = graph.get_neighbors(node)

            for nbr in nbrs:
                # Only update neighbors that have not been seen before
                if dist[nbr] == float('inf'):
                    dist[nbr] = dist[node] + 1
                    parent[nbr] = node
                    stack.push(nbr)

    return parent


def recursive_dfs(graph, start_node, parent):
    """
    Given a graph, a start node from which to search, and a mapping of nodes to
    their parents, performs a recursive depth-first search on graph from the 
    given start node, populating the parents mapping as it goes.
    """
    parent_1 = bfs_dfs(graph, start_node, rac_class=comp614_module6.Stack())
    for key, val in parent_1.items():
        parent[key] = val


def get_inbound_nbrs(graph):
    """
    Given a directed graph, returns a mapping of each node n in the graph to
    the set of nodes that have edges into n.
    """
    # Initialize all data structures
    neighbors = {}

    queue = comp614_module6.Queue()
    for node in graph.nodes():
        queue.push(node)
        neighbors[node] = set()

    # Initialize distances and parents; no nodes have been visited yet
    for node in graph.nodes():
        nbrs = graph.get_neighbors(node)
        for nbr in nbrs:
            if nbr not in neighbors:
                neighbors[nbr] = {node}
            elif nbr in neighbors and node not in neighbors[nbr]:
                neighbors[nbr].add(node)
            else:
                pass

    # account for nodes with no inbound edges

    return neighbors


def remove_sink_nodes(graph):
    """
    Given a directed graph, returns a new copy of the graph where every node that
    was a sink node in the original graph now has an outbound edge linking it to 
    every other node in the graph (excluding itself).
    """
    graph_copy = graph.copy()
    # neighbors = get_inbound_nbrs(graph_copy)
    # output = {}
    all_nodes = set()
    for node in graph_copy.nodes():
        all_nodes.add(node)

    for node in graph_copy.nodes():
        if len(graph.get_neighbors(node)) == 0:
            for node_n in all_nodes:
                if node_n != node:
                    graph_copy.add_edge(node, node_n)
                else:
                    pass
        else:
            pass

    return graph_copy


def page_rank(graph, damping):
    """
    Given a directed graph and a damping factor, implements the PageRank algorithm
    -- continuing until delta is less than 10^-8 -- and returns a dictionary that 
    maps each node in the graph to its page rank.
    """
    nodes_copy = remove_sink_nodes(graph)

    # output dictionary of page ranks
    nodes = {}

    node_list = []
    # queue = comp614_module6.Queue()
    for node in nodes_copy.nodes():
        node_list.append(node)
    # n_l = len(node_list)

    # initial rank
    for node_n in node_list:
        nodes[node_n] = 1/len(node_list)

    # get all the inbound neighbors of each node
    # inbound_nbrs = get_inbound_nbrs(nodes_copy)

    # find the sets of outbound edges for each of the nodes
    outbound_nbrs = {}
    for n_b in nodes_copy.nodes():
        outbound_nbrs[n_b] = nodes_copy.get_neighbors(n_b)

    # delta = sum(nodes.values())
    delta = float("inf")
    while delta > 10e-8:
        # rank = 0
        # create a new nodes dict to hold previous ranks
        copy_nodes = nodes.copy()

        for node, _ in nodes.items():
            num_ob_nodes = {}
            # set_ib_neighbors = inbound_nbrs[node]
            # set page rank to 0 if node has no inbound neighbors
            if get_inbound_nbrs(nodes_copy)[node] == set():
                nodes[node] = 0
            else:
                # set of inbound neighbors for current node
                # set_ib_neighbors = inbound_nbrs[node]

                # find the number of outbound nodes for the current inbound node
                # num_ob_nodes = {}
                for ib_nbr in get_inbound_nbrs(nodes_copy)[node]:
                    num_out = len(outbound_nbrs[ib_nbr]) # num outbound for each ib nbr
                    num_ob_nodes[ib_nbr] = num_out

                # sum pagerank/outdegree
                sum_ranks = 0
                for node_n, outb in num_ob_nodes.items():
                    sum_ranks += nodes[node_n]/outb

                # pagerank = (1-damping)/len(node_list) + (damping * sum_ranks)
                copy_nodes[node] = (1-damping)/len(node_list) + (damping * sum_ranks)

        # compute delta
        curr_delta = 0
        for (_, v_1), (_, v_2) in zip(nodes.items(), copy_nodes.items()):
            curr_delta += abs(v_1 - v_2)
        delta = curr_delta
        nodes = copy_nodes.copy()
    return nodes

file1 = comp614_module6.file_to_graph("test0.txt")
print(bfs_dfs(file1, "A", comp614_module6.Stack()))
