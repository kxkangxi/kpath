from unittest import TestCase
import networkx as nx
import kpath


class TestKPath(TestCase):
    def setUp(self):
        pass

    def test_kpath(self):
        network = nx.DiGraph()
        edges = [('C', 'D', 3),
                 ('C', 'E', 2),
                 ('D', 'F', 4),
                 ('E', 'D', 1),
                 ('E', 'F', 2),
                 ('E', 'G', 3),
                 ('F', 'G', 2),
                 ('F', 'H', 1),
                 ('G', 'H', 2)
                 ]
        network.add_weighted_edges_from(edges)
        k = 8
        path_list = kpath.kpath(network, 'C', 'H', k)
        results = [('C', 'E', 'F', 'H'), ('C', 'E', 'G', 'H'), ('C', 'D', 'F', 'H'), ('C', 'E', 'F', 'G', 'H'),
         ('C', 'E', 'D', 'F', 'H'), ('C', 'D', 'F', 'G', 'H'), ('C', 'E', 'D', 'F', 'G', 'H')]

        self.assertListEqual(path_list, results)

