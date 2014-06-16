import os, sys
sys.path.insert(0, os.path.abspath(".."))

import unittest

from graph import Node, Graph, next_letter

class NodeTestCase(unittest.TestCase):
    def setUp(self):
        self.node = Node('A')

    def tearDown(self):
        self.node = None

    def test_add_path(self):
        other = Node('B')
        self.node.add_path(other, 5)
        self.assertEqual(other.distances[self.node], self.node.distances[other], 'Distances are different')

    def test_next_letter(self):
        self.assertEqual(next_letter('C'), 'D', 'next letter properly assigned')


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        self.graph = None
    
    def test_parse_line(self):
        self.graph.parse_line('A', '-1,5,-1')
        self.graph.parse_line('B', '5,-1,3')
        self.graph.parse_line('C', '-1,3,-1')
        self.assertEqual(len(self.graph.nodes), 3, 'have right number of nodes')
        self.assertEqual(self.graph['A'][self.graph['B']],
                         self.graph['B'][self.graph['A']], 
                         'distances are sane')

    def test_find_shortest_path(self):
        nodes = [Node('A'), Node('B'), Node('C')]
        for node in nodes:
            self.graph.add_node(node)
        nodes[0].add_path(nodes[1], 2)
        nodes[1].add_path(nodes[2], 3)
        shortest_path = ''.join([node.name for node in self.graph.find_shortest_path(nodes[0], nodes[2])])
        self.assertEqual('ABC', 
                         shortest_path, 
                         "shortest path wasn't correct, got " + shortest_path)

if __name__ == '__main__':
    unittest.main()
