# Algorithm to calculate K-shortest paths

import networkx as nx

def find_next_hops_to_remove(existing_paths, root_path):
    """
    compare each existing path with the root path, if overlapped, the next hop node is returned
    :param existing_paths: [path1, path2, ...]
    :param root_path: a root path
    :return: a set of nodes (a, b, c, ...)
    """
    next_hops = set([])
    root_len = len(root_path)
    for path in existing_paths:
        if len(path) <= root_len:
            continue

        overlapped = True
        for i in range(root_len):
            if path[i] != root_path[i]:
                overlapped = False
                break
        if overlapped:
            next_hops.add(path[root_len])

    return next_hops

def path_cost(network, path):
    """
    Calc the total cost of the path
    :param network: networkx instance
    :param path: list of node as path
    :return: total cost of path
    """
    cost = len(path) * 1e-10    # tie breaker, prefer the path with fewer nodes
    for i in range(len(path)-1):
        cost += network[path[i]][path[i+1]]['weight']
    return cost

def kpath(network, src, dst, k):
    """
    calculate K shortest paths

    :param network: networkx instance
    :param src: src node
    :param dst: dst node
    :param k: number of paths to return
    :return: list of shortest paths sorted from short to long
    """
    assert k > 0
    assert network.has_node(src)
    assert network.has_node(dst)
    for a, b in network.edges:
        assert 'weight' in network[a][b]

    shortest_path = nx.dijkstra_path(network, src, dst)

    kpath = [tuple(shortest_path)]
    candidate_paths = {}    # {path1: cost1, path2: cost2...}

    for i in range(k-1):
        # take the newly found path and use each node except dst as spur node
        path = kpath[i]
        for j in range(len(path) - 1):
            spur_node = path[j]
            root_path = list(path[:j+1])
            next_hops = find_next_hops_to_remove(kpath, root_path)
            # save the complete edge attributes so that they can be added later
            edges_saved = [(spur_node, b, network.edges[spur_node, b]) for b in next_hops]
            network.remove_edges_from(edges_saved)

            try:
                spur_path = nx.dijkstra_path(network, spur_node, dst)
                root_path.extend(spur_path[1:])
                candidate_paths[tuple(root_path)] = path_cost(network, root_path)
            except nx.NetworkXNoPath:
                # no spur path found
                pass

            # restore the previously removed edges
            network.add_edges_from(edges_saved)

        if candidate_paths:
            # candidate is not empty
            min_cost = -1
            new_path = None
            for p, cost in candidate_paths.items():
                if min_cost < 0 or min_cost > cost:
                    new_path = p
                    min_cost = cost

            # move new_path to kpath
            kpath.append(new_path)
            candidate_paths.pop(new_path)
        else:
            break

    return kpath
