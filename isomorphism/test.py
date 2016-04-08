from isomorphism.graph import Graph
from debugging.utils import time_this, connected_components, is_tree

if __name__ == '__main__':
    graphs = Graph.read_graph('C:\\Development\\PycharmProjects\\GraphIsomorphism\\graphs\\bonusGI5.grl')

    for i, g in enumerate(graphs):
        print(is_tree(g), len(g), len(g.edges))
        for c in g.connected_components:
            print(is_tree(Graph(c)), len(c), c)

        print()
        g.dot('test{}'.format(i))
