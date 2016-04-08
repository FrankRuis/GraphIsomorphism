from isomorphism.graph import Graph
from debugging.utils import time_this, connected_components, is_tree, time
from isomorphism.color_refinement import count_isomorphisms, disjoint_union


@time_this
def test():
    graphs = Graph.read_graph('C:\\Development\\PycharmProjects\\GraphIsomorphism\\graphs\\torus144.grl')

    for i, g in enumerate(graphs):
        for c in g.connected_components:
            h = Graph(c)
            print(h)
            h.dot('color')
        #
        # print()
        # g.dot('test{}'.format(i))
        # print(count_isomorphisms(disjoint_union(g, g)))

        break

if __name__ == '__main__':
    test()
