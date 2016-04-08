from debugging.utils import time_this, is_tree
from isomorphism.graph import Graph, Vertex


def get_center(tree):
    """
    Get the center vertex of a given tree, or vertices if there are two possible centers.
    Do a breadth-first search from a random vertex to find the vertex farthest away from that vertex.
    Do a second breadth-first search from that vertex to find the longest path in the tree.
    The vertex in the middle of that path is the center of the tree.
    """
    def find_furthest(start):
        """
        Perform breadth-first search and mark the path.
        """
        p = None
        visited, stack = set(), [[start]]
        while stack:
            p = stack.pop(0)
            vertex = p[-1]
            if vertex not in visited:
                visited.add(vertex)
                ext = vertex.nbs - visited
                stack.extend([p + [v] for v in ext])
        return p
    n1 = tree[0]
    n2 = find_furthest(n1)[-1]
    path = find_furthest(n2)

    if not len(path) % 2:
        return path[len(path) // 2 - 1], path[len(path) // 2]
    else:
        return path[len(path) // 2],


def get_root(tree):
    """
    Get the center vertex of the given tree, or get a newly inserted vertex if there are two center vertices.
    """
    center = get_center(tree)

    if len(center) == 2:
        tree.remove_edge(center[0], center[1])
        n = Vertex(len(g))
        tree.append(n)
        tree.add_edge(center[0], n)
        tree.add_edge(center[1], n)
    else:
        n = center[0]

    return n


def assign_levels(start):
    """
    Set the label of each vertex to the distance to the given start vertex.
    """
    levels = {0: [start]}
    visited = set()
    start.label = 0
    stack = [start]
    while stack:
        cur = stack.pop()
        visited.add(cur)
        for v in cur.nbs - visited:
            v.label = cur.label + 1
            stack.append(v)
            if v.label in levels:
                levels[v.label].append(v)
            else:
                levels[v.label] = [v]

    return levels


@time_this
def tree_isomorphism(t1, t2):
    """
    Assign a level to each vertex based on the distance to the root vertex.
    Start labeling vertices from the bottom level to the top level.
    If the root vertices of the graphs have the same label at the end of the algorithm, the graphs are isomorphic.
    """
    levels_t1 = assign_levels(get_root(t1))
    levels_t2 = assign_levels(get_root(t2))

    if len(levels_t1) != len(levels_t2):
        return False

    for i in range(len(levels_t1) - 1, -1, -1):
        for v in levels_t1[i]:
            if v.deg() == 1:
                v.str = '10'
            else:
                v.str = '1{}0'.format(''.join(sorted([c.str for c in v.nbs if c.label > v.label])))

        for v in levels_t2[i]:
            if v.deg() == 1:
                v.str = '10'
            else:
                v.str = '1{}0'.format(''.join(sorted([c.str for c in v.nbs if c.label > v.label])))

        l1 = sorted((v for v in levels_t1[i]), key=lambda x: x.str)
        l2 = sorted((v for v in levels_t2[i]), key=lambda x: x.str)
        if not l1 == l2:
            return False

    return True


@time_this
def tree_automorphisms(tree):
    """
    Assign a level to each vertex based on the distance to the root vertex.
    Label vertices from the bottom level to the top level.
    Count the number of automorphisms of the tree.
    """
    root = get_root(tree)
    levels = assign_levels(root)

    # From bottom to top, assign a label to each vertex that is given by the subtree with that vertex as the root.
    # After the iteration, all subtrees that have a root vertex with the same label are isomorphic
    for i in range(len(levels) - 1, -1, -1):
        for v in levels[i]:
            if v.deg() == 1:
                v.str = '10'
            else:
                v.str = '1{}0'.format(''.join(sorted([c.str for c in v.nbs if c.label > v.label])))

        levels[i] = sorted([v for v in levels[i]], key=lambda x: x.str)

    # Use breadth-first search starting from the root vertex to count the number of isomorphic subtrees.
    # Add the resulting counts to a list.
    visited = set()
    stack = [root]
    subtree_types = []
    while stack:
        cur = stack.pop(0)
        children = [v.str for v in cur.nbs if v.label > cur.label]
        subtree_types += map(lambda x: children.count(x), set(children))
        visited.add(cur)
        stack.extend(cur.nbs - visited)

    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)

    # Multiply the factorial of each isomorphic subtree count.
    # The result is the amount of automorphisms of this tree.
    count = 1
    for f in map(factorial, subtree_types):
        count *= f

    return count

if __name__ == '__main__':
    graphs = Graph.read_graph('C:\\Development\\PycharmProjects\\GraphIsomorphism\\graphs\\bonusAut2.gr')

    g = graphs[0]
    print(tree_automorphisms(g))
