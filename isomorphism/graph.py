from debugging.utils import connected_components, time_this, is_tree
import ast


class Graph(list):
    def __init__(self, g=(), e=None):
        super(Graph, self).__init__(g)
        if e is None and hasattr(g, 'edges'):
            self.edges = g.edges
        elif e is None:
            self.edges = set()
            if len(g) > 0:
                for v in g:
                    for w in v.nbs:
                        self.add_edge(v, w)
                    v.graph = self
        else:
            self.edges = e
        self._connected_components = None
        self._complete = None
        self._tree = None

    def append(self, p_object):
        p_object.id = len(self)
        super(Graph, self).append(p_object)

    def add_edge(self, v, w):
        v.add_edge(w)
        self.edges.add(tuple(sorted((v, w))))

    def remove_edge(self, v, w):
        v.remove_edge(w)
        if (v, w) in self.edges:
            self.edges.remove((v, w))
        elif (w, v) in self.edges:
            self.edges.remove((w, v))

    def add_vertex(self, label):
        self.append(Vertex(label, graph=self))

    @property
    def connected_components(self):
        if self._connected_components is None:
            self._connected_components = connected_components(self)

        return self._connected_components

    @property
    def complete(self):
        if self._complete is None:
            if (len(self) * (len(self) - 1)) / 2 == len(self.edges):
                self._complete = all(map(lambda v: len(v.nbs) == len(v.graph) - 1, self))
            else:
                self._complete = False

        return self._complete

    @property
    def tree(self):
        if self._tree is None:
            self._tree = is_tree(self)

        return self._tree

    def dot(self, name):
        path = '../output/{:s}.dot'.format(name)
        with open(path, 'w+') as file:
            file.write('Graph {\n')
            for i, v in enumerate(self):
                file.write('\t{:d} [penwidth=3, label="{}"]\n'.format(i, v.label))

            file.write('\n')

            for e in self.edges:
                file.write('\t{}--{} [penwidth=2]\n'.format(e[0].id, e[1].id))

            file.write('}')

    @staticmethod
    def read_graph(path):
        with open(path) as file:
            graphs = []
            cur = Graph()
            for line in file:
                if line[0] != "#" and line[0] != "-" and len(line.strip()) > 0:
                    if not len(cur):
                        for i in range(int(line)):
                            cur.add_vertex(i)
                    else:
                        edge = ast.literal_eval(line)
                        cur.add_edge(cur[edge[0]], cur[edge[1]])
                elif line[0] == "-":
                    graphs.append(cur)
                    cur = Graph()
            graphs.append(cur)
        return graphs

    @classmethod
    def wrap_methods(cls, names):
        def wrap_method_closure(name):
            def inner(self, *args):
                result = getattr(super(cls, self), name)(*args)
                if isinstance(result, list) and not hasattr(result, 'edges'):
                    result = cls(result, e=self.edges)
                return result
            inner.fn_name = name
            setattr(cls, name, inner)
        for name in names:
            wrap_method_closure(name)

    def __str__(self):
        return 'Nodes: {}\nEdges: {}\n'.format(repr(self), self.edges)

Graph.wrap_methods(['__add__', '__reversed__', '__reverse__', '__iadd__', '__radd__', 'copy',])


class Vertex:
    def __init__(self, label=None, nbs=None, graph=None):
        if nbs is None:
            nbs = set()
        self.id = label
        self.label = label
        self.graph = graph
        self.nbs = nbs

    def deg(self):
        return len(self.nbs)

    def add_edge(self, v):
        self.nbs.add(v)
        v.nbs.add(self)

    def remove_edge(self, v):
        if v in self.nbs:
            self.nbs.remove(v)

        if self in v.nbs:
            v.nbs.remove(self)

    def __lt__(self, other):
        return self.label < other.label

    def __repr__(self):
        return str(self.label)

if __name__ == '__main__':
    h = Graph.read_graph('C:\\Development\\PycharmProjects\\GraphIsomorphism\\graphs\\basicAut1.gr')
    print(h[0])