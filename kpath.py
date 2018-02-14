# Algorithm to calculate K-shortest paths

import networkx as nx

class KPath():
    @staticmethod
    def find_next_hops_to_remove(candidate_paths, root_path):
        """
        compare each candidate path with the root path, if overlapped, the next hop node is returned
        :param candidate_paths: [(cost, path), (cost, path), ...]
        :param root_path: a root path
        :return: a list of nodes [a, b, c, ...]
        """
        next_hops = []
        root_len = len(root_path)
        for cost, path in candidate_paths:
            overlapped = True
            for i in range(root_len):
                if path[i] != root_path[i]:
                    overlapped = False
                    break
            if overlapped:
                next_hops.append(path[root_len])

        return next_hops

    @staticmethod
    def path_cost(network, path):
        """
        Calc the total cost of the path
        :param network: networkx instance
        :param path: list of node as path
        :return: total cost of path
        """
        cost = 0
        for i in range(len(path)-1):
            cost += network[path[i], path[i+1]]['weight']
        return cost

    @staticmethod
    def kpath(network, src, dst, k):
        """
        calculate K shortest paths

        :param network: networkx instance
        :param src: src node
        :param dst: dst node
        :param k: number of paths to return
        :return: list of shortest paths sorted from short to long
        """
        network = nx.Graph()
        assert network.has_node(src)
        assert network.has_node(dst)
        for edge in network.edges:
            assert 'weight' in edge

        shortest_path = nx.dijkstra_path(network, src, dst)

        kpath= [shortest_path]
        candidate_paths = [] #[[cost1, path1], [cost2, path2] ...]

        for i in range(k):
            # take the newly found path and use each node except dst as spur node
            path = kpath[i]
            for j in range(len(path) - 1):
                spur_node = path[j]
                root_path = path[:j+1]
                next_hops = KPath.find_next_hops_to_remove(candidate_paths, root_path)
                # save the complete edge attributes so that they can be added later
                edges_saved = [(spur_node, b, network.edges[spur_node, b]) for b in next_hops]
                network.remove_edges_from(edges_saved)

                try:
                    spur_path = nx.dijkstra_path(network, spur_node, dst)
                    root_path.extend(spur_path)
                    candidate_paths.append((KPath.path_cost(root_path), root_path))
                except nx.NetworkXNoPath:
                    # no spur path found
                    pass

                # restore the previously removed edges
                network.add_edges_from(edges_saved)

            # From the candidate paths, find the min cost one and add it to the kpath list
            min_cost = -1
            best_idx = None
            for idx in range(len(candidate_paths)):
                cost = candidate_paths[idx][0]
                if cost > 0 and (min_cost < 0 or cost < min_cost):
                    min_cost = cost
                    best_idx = idx

            if best_idx:
                kpath.append(candidate_paths[idx][1])
                # set the cost to -1 instead of removing from the list to save time
                candidate_paths[idx][0] = -1
            else:
                break
        return kpath





