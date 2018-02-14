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
        k = 3
        kpaths = kpath.KPath.kpath(network, 'C', 'H', k)
        print(kpaths)
        self.assertEqual(k, len(kpath))

